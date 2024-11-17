import customtkinter as ctk
from tkinter import messagebox
from components.table_widget import CTkTable
from components.tooltip_widget import CTkToolTip
from utils.json_utils import cargar_datos, eliminar_operaciones
from utils.git_utils import generar_gif_desde_json
import threading

class ReportesTab:
    def __init__(self, tabview):
        self.tab = tabview.add("Reportes")
        
        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Crear la tabla con columnas: Método, Función, Seleccionar
        self.tabla = CTkTable(self.tab, columns=["Método", "Función", "Seleccionar"])
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para cargar operaciones
        self.btn_cargar_operaciones = ctk.CTkButton(self.tab, text="Cargar Operaciones", command=self.cargar_operaciones)
        self.btn_cargar_operaciones.pack(pady=10)

        # Botón para generar GIFs
        self.btn_generar_gifs = ctk.CTkButton(self.tab, text="Generar GIFs Seleccionados", command=self.generar_gifs_seleccionados)
        self.btn_generar_gifs.pack(pady=10)

        # Botón para eliminar filas seleccionadas
        self.btn_eliminar = ctk.CTkButton(self.tab, text="🗑", width=50, command=self.eliminar_seleccionados)
        self.btn_eliminar.pack(pady=10)

        # Tooltip para el botón de eliminar
        CTkToolTip(self.btn_eliminar, message="Elimina las filas seleccionadas de la tabla.", delay=500)

    def cargar_operaciones(self):
        try:
            # Cargar operaciones desde el archivo JSON
            self.operaciones = cargar_datos()

            # Validar que el JSON cargado sea un diccionario y contenga listas de funciones para cada método
            if not isinstance(self.operaciones, dict):
                raise ValueError("Formato del JSON incorrecto. Se esperaba un diccionario con listas de funciones.")

            # Limpiar datos previos
            self.tabla.clear_data()
            self.check_vars = []  # Lista para almacenar variables de selección

            # Recorrer cada método y sus funciones
            for metodo, contenido in self.operaciones.items():
                if "funciones" in contenido and isinstance(contenido["funciones"], list):
                    for funcion in contenido["funciones"]:
                        # Insertar fila en la tabla
                        self.tabla.tree.insert(
                            "", "end",
                            values=(metodo, funcion["funcion"], "No seleccionado")
                        )
                else:
                    raise ValueError("Formato del JSON incorrecto. Cada método debe contener una lista de funciones.")

            # Añadir funcionalidad para cambiar el estado de selección al hacer clic en la columna "Seleccionar"
            self.tabla.tree.bind("<Button-1>", self.toggle_selection)

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo JSON no se encontró en la ruta especificada.")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado al cargar operaciones: {e}")

    def toggle_selection(self, event):
        # Obtener el elemento seleccionado
        item_id = self.tabla.tree.identify_row(event.y)
        column = self.tabla.tree.identify_column(event.x)

        # Verificar si se seleccionó la columna "Seleccionar" (la tercera columna)
        if item_id and column == '#3':
            # Alternar el estado de selección
            current_value = self.tabla.tree.item(item_id, "values")[2]
            new_value = "Seleccionado" if current_value == "No seleccionado" else "No seleccionado"
            self.tabla.tree.item(item_id, values=(self.tabla.tree.item(item_id, "values")[0], self.tabla.tree.item(item_id, "values")[1], new_value))

    def generar_gifs_seleccionados(self):
        try:
            # Obtener los métodos seleccionados
            seleccionados = []
            for i, item in enumerate(self.tabla.tree.get_children()):
                # Verificar si la columna "Seleccionar" tiene el valor "Seleccionado"
                if self.tabla.tree.item(item, "values")[2] == "Seleccionado":
                    metodo = self.tabla.tree.item(item, "values")[0]
                    funcion = self.tabla.tree.item(item, "values")[1]
                    seleccionados.append((metodo, funcion))

            if not seleccionados:
                messagebox.showinfo("Información", "No se seleccionaron operaciones para generar GIFs.")
                return

            # Generar GIFs en hilos separados
            for metodo, funcion in seleccionados:
                indice = next(
                    (i for i, op in enumerate(self.operaciones[metodo]["funciones"]) if op["funcion"] == funcion),
                    None
                )
                if indice is not None:
                    hilo_gif = threading.Thread(target=self.generar_gif_thread, args=(metodo, indice))
                    hilo_gif.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar GIFs: {e}")

    def generar_gif_thread(self, metodo, indice):
        try:
            # Generar el GIF desde el JSON con la operación seleccionada
            generar_gif_desde_json(metodo, indice)
        except Exception as e:
            messagebox.showerror("Error", f"Error en la generación del GIF: {e}")

    def eliminar_seleccionados(self):
        """
        Elimina las filas seleccionadas de la tabla y del archivo JSON.
        """
        try:
            seleccionados = []  # Lista para almacenar índices de operaciones a eliminar
            filas_a_eliminar = []

            # Recorrer todas las filas de la tabla
            for item in self.tabla.tree.get_children():
                values = self.tabla.tree.item(item, "values")
                if values[2] == "Seleccionado":
                    metodo = values[0]
                    funcion = values[1]
                    
                    # Obtener el índice correspondiente en el JSON
                    indice = next(
                        (i for i, op in enumerate(self.operaciones[metodo]["funciones"]) if op["funcion"] == funcion),
                        None
                    )
                    if indice is not None:
                        seleccionados.append((metodo, indice))
                        filas_a_eliminar.append(item)  # Marcar fila para eliminar

            # Eliminar las filas seleccionadas de la tabla
            for fila in filas_a_eliminar:
                self.tabla.tree.delete(fila)

            # Eliminar las operaciones seleccionadas del archivo JSON
            for metodo, indices in self.agrupar_por_metodo(seleccionados).items():
                eliminar_operaciones(metodo, indices)

            messagebox.showinfo("Operación completada", "Operaciones eliminadas correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar operaciones: {e}")

    def agrupar_por_metodo(self, seleccionados):
        """
        Agrupa los índices seleccionados por método.
        - seleccionados: Lista de tuplas (metodo, indice).
        Retorna un diccionario {metodo: [indices]}.
        """
        agrupados = {}
        for metodo, indice in seleccionados:
            if metodo not in agrupados:
                agrupados[metodo] = []
            agrupados[metodo].append(indice)
        return agrupados



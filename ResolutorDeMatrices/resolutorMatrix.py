import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from funcionesMatrices.pivoteo import *
from funcionesMatrices.matrixValidator import *
from funcionesMatrices.reemplazar import rotar_matriz_90
from pylatex import Document, Section, Math, Matrix
from pylatex.utils import NoEscape
from datetime import datetime
import sys

# Lista para almacenar las matricesSuma ingresadas en la pestaña de Suma Matrices
matricesSuma = []
matricesMult = []
consola_visible = True
consola_matrices_visible = True
consola_pasos_determinante_visible = True
matriz_suma_global = None  # Variable global para almacenar la matriz sumada
global_font_size = 12


def calcular_determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada.
    """
    # Caso base para una matriz 2x2
    if len(matriz) == 2 and len(matriz[0]) == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    # Recursión para matrices de mayor tamaño
    determinante_total = 0
    for columna in range(len(matriz)):
        # Crear la submatriz excluyendo la primera fila y la columna actual
        submatriz = [fila[:columna] + fila[columna+1:] for fila in matriz[1:]]
        cofactor = ((-1) ** columna) * matriz[0][columna] * calcular_determinante(submatriz)
        determinante_total += cofactor
    
    return determinante_total


def reemplazar_columna(matriz, columna, valores):
    """
    Reemplaza una columna en la matriz por los valores del vector.
    """
    matriz_modificada = [fila[:] for fila in matriz]  # Hacer una copia profunda de la matriz
    for i in range(len(matriz)):
        matriz_modificada[i][columna] = valores[i]
    return matriz_modificada


def resolver_sistema_cramer(coeficientes, resultados):
    """
    Resuelve un sistema de ecuaciones lineales utilizando la regla de Cramer.
    
    Parámetros:
        coeficientes (list of lists): Matriz de coeficientes del sistema.
        resultados (list): Vector de resultados independientes.
    
    Retorna:
        tuple: Vector de soluciones y los pasos realizados.
    """
    # Calcular el determinante de la matriz de coeficientes
    det_principal = calcular_determinante(coeficientes)
    
    # Verificar si el sistema tiene solución única (det != 0)
    if det_principal == 0:
        return None, "El sistema no tiene solución única (determinante es 0)."
    
    # Calcular los determinantes de las matrices modificadas y encontrar las soluciones
    soluciones = []
    pasos = "Pasos realizados:\n"
    pasos += f"Determinante de la matriz de coeficientes: {det_principal}\n"
    
    for i in range(len(resultados)):
        # Reemplazar la columna i con los resultados independientes
        matriz_modificada = reemplazar_columna(coeficientes, i, resultados)
        det_modificado = calcular_determinante(matriz_modificada)
        solucion = det_modificado / det_principal
        soluciones.append(solucion)

        # Añadir detalles a los pasos
        pasos += f"Determinante con columna {i+1} reemplazada: {det_modificado}\n"
        pasos += f"Solución {i+1}: x{i+1} = {solucion}\n"

    return soluciones, pasos


def resolver_por_cramer_interface():
    try:
        # Obtener el texto de la matriz de coeficientes y el vector de resultados ingresados
        coeficientes_str = matriz_input_cramer.get("1.0", ctk.END).strip()
        resultados_str = vector_resultados_input.get("1.0", ctk.END).strip()

        # Convertir las entradas en listas de listas (para coeficientes) y listas simples (para resultados)
        coeficientes = [list(map(float, fila.split())) for fila in coeficientes_str.split("\n")]
        resultados = list(map(float, resultados_str.split()))

        # Resolver el sistema usando la regla de Cramer
        soluciones, pasos = resolver_sistema_cramer(coeficientes, resultados)

        # Mostrar el resultado en la consola
        consola_cramer.delete("1.0", ctk.END)
        if soluciones:
            consola_cramer.insert(ctk.END, f"Soluciones: {soluciones}\n")
        else:
            consola_cramer.insert(ctk.END, pasos)

        # Mostrar los pasos realizados
        consola_pasos_cramer.delete("1.0", ctk.END)
        consola_pasos_cramer.insert(ctk.END, pasos)

    except Exception as e:
        consola_cramer.delete("1.0", ctk.END)
        consola_cramer.insert(ctk.END, f"Error: {str(e)}")


# Función que usa la interfaz tkinter para generar la matriz y calcular el determinante
def calcular_determinante_tab():
    try:
        # Obtener el texto de la matriz ingresada
        matriz_str = matriz_input_determinante.get("1.0", ctk.END).strip()
        matriz = validar_entrada_matriz(matriz_str)
        
        # Calcular determinante
        det, pasos = determinante(matriz)
        
        # Mostrar resultado en la consola
        consola_pasos_determinante.delete("1.0", ctk.END)
        consola_determinante.insert(ctk.END, f"Determinante: {det}\n")
        consola_pasos_determinante.insert(ctk.END, pasos)
        
    except ValueError as e:
        consola_pasos_determinante.delete("1.0", ctk.END)
        consola_determinante.insert(ctk.END, f"Error: {str(e)}")
        
def matriz_a_latex(matriz):
    filas = [" & ".join(map(str, fila)) for fila in matriz]
    return "\\begin{bmatrix} " + " \\\\ ".join(filas) + " \\end{bmatrix}"

class OperationLogger:
    def __init__(self):
        self.operations = []
        
    def log(self, operation, matriz=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.operations.append((timestamp, operation, matriz))
        
    def generate_pdf_report(self):
        doc = Document()
        with doc.create(Section('Registro de Operaciones')):
            for timestamp, operation, matriz in self.operations:
                # Inserta la descripción de la operación
                doc.append(f"{timestamp}: {operation}\n")
                # Si hay una matriz asociada, convertirla a formato LaTeX manualmente
                if matriz is not None:
                    matriz_latex = matriz_a_latex(matriz)
                    with doc.create(Math()):
                        doc.append(NoEscape(matriz_latex))
        doc.generate_pdf('operation_log', clean_tex=False)


logger=OperationLogger()

# Función para redirigir la salida de consola a un widget de texto
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert("end", string)
        self.widget.see("end")  # Desplaza automáticamente hacia abajo

    def flush(self):
        pass  # Necesario para que funcione con algunos sistemas
    
def ajustar_tamano_fuente(valor):
    global global_font_size
    global_font_size = int(valor)

    # Actualizar el tamaño de fuente de los widgets que tengan texto
    widgets = [consola_textbox,consola_suma,consola_matrices_listadas, consola_distributiva, consola_transpuesta]
    for widget in widgets:
        widget.configure(font=("Courier", global_font_size))

def ajustar_altura_consolas(valor):
    altura = int(valor)
    widgets = [consola_textbox, consola_matrices_listadas, consola_distributiva, consola_transpuesta]
    for widget in widgets:
        widget.configure(height=altura)

def ajustar_ancho_consolas(valor):
    ancho = int(valor)
    widgets = [consola_textbox, consola_matrices_listadas, consola_distributiva, consola_transpuesta]
    for widget in widgets:
        widget.configure(width=ancho)
        
def abrir_popup_ajustes():
    # Crear una ventana emergente (popup) con pestañas
    popup = ctk.CTkToplevel(root)
    popup.title("Ajustes de Configuración")
    popup.geometry("500x400")

    # Crear el Notebook (pestañas) dentro del popup
    tabview = ctk.CTkTabview(popup)
    tabview.pack(expand=True, fill="both")

    # Pestaña para ajustar el tamaño de la fuente
    tabview.add("Tamaño de Fuente")
    tab_fuente = tabview.tab("Tamaño de Fuente")
    
    label_popup_fuente = ctk.CTkLabel(tab_fuente, text="Ajustar Tamaño de Fuente Global")
    label_popup_fuente.pack(pady=20)
    
    slider_fuente_popup = ctk.CTkSlider(tab_fuente, from_=8, to=24, command=ajustar_tamano_fuente)
    slider_fuente_popup.pack(pady=20)
    slider_fuente_popup.set(global_font_size)  # Valor inicial

    # Pestaña para ajustar el tamaño de las consolas
    tabview.add("Tamaño de Consolas")
    tab_consola = tabview.tab("Tamaño de Consolas")

    label_popup_consola = ctk.CTkLabel(tab_consola, text="Ajustar Tamaño de Consolas")
    label_popup_consola.pack(pady=20)

    # Slider para ajustar la altura de las consolas
    label_altura = ctk.CTkLabel(tab_consola, text="Altura de Consolas")
    label_altura.pack(pady=5)
    slider_altura = ctk.CTkSlider(tab_consola, from_=100, to=500, command=ajustar_altura_consolas)
    slider_altura.pack(pady=10)
    slider_altura.set(300)  # Valor inicial

    # Slider para ajustar el ancho de las consolas
    label_ancho = ctk.CTkLabel(tab_consola, text="Ancho de Consolas")
    label_ancho.pack(pady=5)
    slider_ancho = ctk.CTkSlider(tab_consola, from_=200, to=1200, command=ajustar_ancho_consolas)
    slider_ancho.pack(pady=10)
    slider_ancho.set(500)  # Valor inicial


def toggle_consola():
    global consola_matrices_visible
    global consola_pasos_determinante_visible
    
    if consola_matrices_visible or consola_pasos_determinante_visible:
        consola_matrices_listadas.pack_forget()
        consola_pasos_determinante.pack_forget()
        btn_toggle_consola1.configure(text="Mostrar Consolas")# Oculta el TextBox de matricesSuma
        btn_toggle_consola2.configure(text="Mostrar Consolas")
    else:
        consola_matrices_listadas.pack(pady=10, padx=20, before=btn_toggle_consola1) 
        consola_pasos_determinante.pack(pady=10, padx=20, before=btn_toggle_consola2)
        consola_matrices_listadas.pack_propagate(0)  # Desactiva la propagación del tamaño para evitar el ajuste del espacio
        consola_pasos_determinante.pack_propagate(0)
        btn_toggle_consola1.configure(text="Ocultar Consolas")# Muestra el TextBox de matricesSuma
        btn_toggle_consola2.configure(text="Ocultar Consolas")

    consola_matrices_visible = not consola_matrices_visible
    consola_pasos_determinante_visible= not consola_pasos_determinante_visible


def agregar_matriz():
    input_text = matriz_input_suma.get("1.0", "end-1c")
    matriz = validar_entrada_matriz(input_text)
    if matriz is not None and input_text:
        matricesSuma.append(matriz)
        logger.log("Matriz agregada", matriz)
        matriz_input_suma.delete("1.0", "end")
    else:
        consola_suma.insert("end", "Error: Asegúrate de que la matriz contiene solo números.\n")
        
def mostrar_matrices_en_consola():
    consola_suma.delete("1.0", "end")  # Limpiar la consola principal
    consola_matrices_listadas.delete("1.0", "end")  # Limpiar la consola para matricesSuma listadas

    if not matricesSuma:
        consola_matrices_listadas.insert("end", "No hay matricesSuma almacenadas.\n")
        return

    consola_matrices_listadas.insert("end", "Matrices almacenadas:\n")

    for idx, matriz in enumerate(matricesSuma):
        consola_matrices_listadas.insert("end", f"Matriz {idx + 1}:\n")

        for fila in matriz:
            # Imprimir cada fila de la matriz en formato monoespaciado
            consola_matrices_listadas.insert("end", " ".join(f"{elem:8.2f}" for elem in fila) + "\n")

        consola_matrices_listadas.insert("end", "\n")

def obtener_y_resolver_matriz(matriz_input, consola_textbox):
    consola_textbox.delete("1.0", "end")  # Limpiar el contenido anterior en la consola
    input_text = matriz_input.get("1.0", "end-1c")  # Obtener texto desde el widget de texto
    matriz = validar_entrada_matriz(input_text)
    
    if matriz is not None:
        print("Matriz inicial:")
        printMatrix(matriz)

        pivoteoMax(matriz)

        print("Matriz después del pivoteo:")
        printMatrix(matriz)

        print("Resultados finales:")
        printResult(matriz)
    else:
        consola_textbox.insert("end", "Error: Asegúrate de que la matriz contiene solo números.\n")
        
def validar_dimensiones_matrices(matricesSuma):
    if len(matricesSuma) < 2:
        return False  


    filas_primera_matriz = len(matricesSuma[0])
    columnas_primera_matriz = len(matricesSuma[0][0])


    for matriz in matricesSuma[1:]:
        if len(matriz) != filas_primera_matriz or len(matriz[0]) != columnas_primera_matriz:
            return False  

    return True 

def resolver_matrices():
    global matriz_suma_global 
    consola_suma.delete("1.0", "end")
    if len(matricesSuma) < 2:
        consola_suma.insert("end", "Error: Debes agregar al menos dos matricesSuma para sumarlas.\n")
        return
    
    try:
        if validar_dimensiones_matrices(matricesSuma):
            matriz_suma_global = [[sum(filas) for filas in zip(*mat)] for mat in zip(*matricesSuma)]
            consola_suma.insert("end", "Resultado de la suma de matricesSuma:\n")
            for fila in matriz_suma_global:
                consola_suma.insert("end", f"{fila}\n")
            logger.log("Suma de matricesSuma resultante", matriz_suma_global)
        else:
            consola_suma.insert("end", "Error: Las dimensiones de las matricesSuma no son compatibles.\n")
    except Exception as e:
        consola_suma.insert("end", f"Error al sumar matricesSuma: {str(e)}\n")

def copiar_matriz_suma_formato_excel():
    if matriz_suma_global is None:
        consola_suma.insert("end", "Error: No hay matriz sumada para copiar.\n")
        return
    
    copiar_formato_excel(matriz_suma_global, root)
    consola_suma.insert("end", "Matriz sumada copiada en formato Excel.\n")
    
def copiar_formato_excel(matriz, root):
    formato_excel = "\n".join(["\t".join(map(str, fila)) for fila in matriz])
    root.clipboard_clear()
    root.clipboard_append(formato_excel)
    root.update()  # Mantener el portapapeles actualizado

matriz_transpuesta = None

def transponer_matriz():
    global matriz_transpuesta
    consola_transpuesta.delete("1.0", "end")
    input_text = matriz_input_transpuesta.get("1.0", "end-1c")
    if input_text:
        try:
            filas = input_text.strip().split("\n")
            matriz = [list(map(float, fila.split())) for fila in filas]
            matriz_transpuesta = rotar_matriz_90(matriz)
            consola_transpuesta.insert("end", "Matriz transpuesta:\n")
            for fila in matriz_transpuesta:
                consola_transpuesta.insert("end", " ".join(f"{elem:8.2f}" for elem in fila) + "\n")
            logger.log("Matriz transpuesta", matriz_transpuesta)
        except ValueError:
            consola_transpuesta.insert("end", "Error: Asegúrate de que la matriz contiene solo números.\n")
            
            
def copiar_matriz_formato_excel():
    global matriz_transpuesta
    if matriz_transpuesta:
        copiar_formato_excel(matriz_transpuesta,root)  # Copiar al portapapeles
    else:
        consola_transpuesta.insert("end", "No hay matriz transpuesta para copiar.\n")
def calcular_distributiva():
    consola_distributiva.delete("1.0", "end")  # Limpiar la consola
    matriz_text = matriz_input_distributiva.get("1.0", "end-1c")  # Obtener matriz
    vector_u_text = vector_u_input.get("1.0", "end-1c")  # Obtener vector u
    vector_v_text = vector_v_input.get("1.0", "end-1c")  # Obtener vector v

    try:
        # Convertir texto a listas de números
        matriz = [list(map(float, fila.split())) for fila in matriz_text.strip().split("\n")]
        vector_u = list(map(float, vector_u_text.strip().split()))
        vector_v = list(map(float, vector_v_text.strip().split()))

        # Validar las dimensiones antes de calcular
        validar_matriz_vectores(matriz, vector_u, vector_v)

        resultado = calcular(matriz, vector_u, vector_v)

        consola_distributiva.insert("end", resultado)

    except ValueError as e:
        consola_distributiva.insert("end", f"Error: {str(e)}\n")
        
def generar_reporte():
    logger.generate_pdf_report()
    consola_suma.insert("end", "Reporte de operaciones generado.\n")

# Lista para almacenar las celdas generadas (una lista de listas)
celdas_generadas = []

def generar_hoja():
    global frame_hoja, celdas_generadas
    celdas_generadas.clear()  # Limpiar cualquier celda anterior
    
    # Eliminar celdas anteriores si existen
    for widget in frame_hoja.winfo_children():
        widget.destroy()

    try:
        # Obtener el número de filas y columnas desde los cuadros de entrada
        num_filas = int(entry_filas.get())
        num_columnas = int(entry_columnas.get())

        # Crear la nueva matriz de celdas y almacenarlas en celdas_generadas
        for fila in range(num_filas):
            fila_celdas = []  # Lista para almacenar las celdas de la fila actual
            for columna in range(num_columnas):
                celda = ctk.CTkEntry(frame_hoja, width=100)
                celda.grid(row=fila, column=columna, padx=5, pady=5)
                fila_celdas.append(celda)
            celdas_generadas.append(fila_celdas)

    except ValueError:
        label_error.configure(text="Error: Ingresa números válidos para las dimensiones.", text_color="red")

def copiar_hoja_formato_excel():
    try:
        matriz_copia = []

        # Recorrer la lista de listas (celdas_generadas) para obtener los valores
        for fila_celdas in celdas_generadas:
            fila_datos = [celda.get() for celda in fila_celdas]  # Obtener los valores de la fila
            matriz_copia.append("\t".join(fila_datos))  # Unir los valores con tabulaciones

        # Unir todas las filas con saltos de línea
        formato_excel = "\n".join(matriz_copia)

        # Copiar al portapapeles
        root.clipboard_clear()
        root.clipboard_append(formato_excel)
        root.update()  # Mantener el portapapeles actualizado
        
        label_error.configure(text="Hoja copiada en formato Excel.", text_color="green")
        
    except Exception as e:
        label_error.configure(text=f"Error al copiar la hoja: {str(e)}", text_color="red")


# Función para limpiar el mensaje de error
def limpiar_error(event):
    label_error.configure(text="")
# Función para inicializar la interfaz
def iniciar_interfaz():
    # Inicializar customtkinter
    ctk.set_appearance_mode("dark")  # Modo oscuro (opcional)
    ctk.set_default_color_theme("blue")  # Tema de color

    # Crear la ventana principal
    global root
    root = ctk.CTk()
    root.title("MATRIXCALC")
    root.geometry("800x600")

    # Crear el widget Notebook (pestañas)
    notebook = ctk.CTkTabview(root)
    notebook.pack(expand=True, fill="both")

    # Crear pestañas
    notebook.add("Resolutor Matriz")
    notebook.add("Suma Matrices")
    notebook.add("Vectores 1")
    notebook.add("Distributiva")
    notebook.add("Transpuesta")
    notebook.add("Determinante")
    notebook.add("Reportes")
    notebook.add("Excel View")
    notebook.add("Configuraciones")
    tab_cramer = notebook.add("Regla de Cramer")

    # Etiquetas para la matriz de coeficientes y el vector de resultados
    label_coeficientes = ctk.CTkLabel(tab_cramer, text="Matriz de coeficientes (copiar desde Excel):")
    label_coeficientes.pack(pady=10)

    global matriz_input_cramer
    matriz_input_cramer = ctk.CTkTextbox(tab_cramer, height=100)
    matriz_input_cramer.pack(pady=10, padx=20)

    label_resultados = ctk.CTkLabel(tab_cramer, text="Vector de resultados:")
    label_resultados.pack(pady=10)

    global vector_resultados_input
    vector_resultados_input = ctk.CTkTextbox(tab_cramer, height=50)
    vector_resultados_input.pack(pady=10, padx=20)

    # Botón para resolver la matriz
    btn_resolver_cramer = ctk.CTkButton(tab_cramer, text="Resolver con Cramer", command=resolver_por_cramer_interface)
    btn_resolver_cramer.pack(pady=10)

    # Consola para mostrar el resultado
    global consola_cramer
    consola_cramer = ctk.CTkTextbox(tab_cramer, height=100, font=("Courier", global_font_size))
    consola_cramer.pack(pady=10, padx=20)

    # Consola para mostrar los pasos
    global consola_pasos_cramer
    consola_pasos_cramer = ctk.CTkTextbox(tab_cramer, height=200, font=("Courier", global_font_size))
    consola_pasos_cramer.pack(pady=10, padx=20)

    

    # Pestaña "Resolutor Matriz"
    tab_resolutor = notebook.tab("Resolutor Matriz")
    label_resolutor = ctk.CTkLabel(tab_resolutor, text="Ingresa la matriz copiada desde Excel:")
    label_resolutor.pack(pady=10)

    # Crear widget de texto para ingresar la matriz
    global matriz_input
    matriz_input = ctk.CTkTextbox(tab_resolutor, height=100)
    matriz_input.pack(pady=10, padx=20)

    # Consola de salida: aquí se mostrarán los resultados
    global consola_textbox
    consola_textbox = ctk.CTkTextbox(tab_resolutor, height=300, width=250, font=("Courier", global_font_size))
    consola_textbox.pack(pady=10, padx=20)

    # Botón para resolver la matriz
    btn_resolver = ctk.CTkButton(tab_resolutor, text="Resolver Matriz", 
                                 command=lambda: obtener_y_resolver_matriz(matriz_input, consola_textbox))
    btn_resolver.pack(pady=10)

    # Redirigir la salida estándar (stdout) a la "consola" de la interfaz
    sys.stdout = TextRedirector(consola_textbox)

    # Pestaña "Suma Matrices"
    tab_suma = notebook.tab("Suma Matrices")
    label_suma = ctk.CTkLabel(tab_suma, text="Ingresa una matriz copiada desde Excel (formato de tabla):")
    label_suma.pack(pady=10)

    # Entrada de texto para las matricesSuma
    global matriz_input_suma
    matriz_input_suma = ctk.CTkTextbox(tab_suma, height=100)
    matriz_input_suma.pack(pady=10, padx=20)

    # Frame para los botones
    btn_frame = ctk.CTkFrame(tab_suma)
    btn_frame.pack(pady=5)

    # Botón para agregar la matriz a la lista
    btn_agregar = ctk.CTkButton(btn_frame, text="Agregar Matriz", command=agregar_matriz)
    btn_agregar.pack(side="left", padx=5)

    # Botón para resolver la suma de matricesSuma
    btn_resolver_suma = ctk.CTkButton(btn_frame, text="Resolver", command=resolver_matrices)
    btn_resolver_suma.pack(side="left", padx=5)
    
    btn_copiar_matriz_suma = ctk.CTkButton(btn_frame, text="Copiar Formato Excel", command=copiar_matriz_suma_formato_excel)
    btn_copiar_matriz_suma.pack(side="left", padx=5)

    # Consola para la salida en Suma Matrices
    global consola_suma
    consola_suma = ctk.CTkTextbox(tab_suma, height=200, width=500, font=("Courier", global_font_size))
    consola_suma.pack(pady=10, padx=20)
    btn_mostrar_matrices = ctk.CTkButton(tab_suma, text="Mostrar Matrices", command=mostrar_matrices_en_consola)
    btn_mostrar_matrices.pack(pady=5)
    
    global consola_matrices_listadas
    consola_matrices_listadas = ctk.CTkTextbox(tab_suma, height=200, width=500, font=("Courier", global_font_size))
    consola_matrices_listadas.pack(pady=10, padx=20)
    
    global btn_toggle_consola1
    btn_toggle_consola1 = ctk.CTkButton(tab_suma, text="Ocultar Consolas", command=toggle_consola)
    btn_toggle_consola1.pack(pady=10)
    

    # Crear un frame para la visualización de las matricesSuma
    global frame_matriz_visual
    frame_matriz_visual = ctk.CTkFrame(tab_suma)
    frame_matriz_visual.pack(expand=True, fill="both", padx=10, pady=10)

    # Pestaña "Vectores 1"
    tab_vectores1 = notebook.tab("Vectores 1")
    label_vectores1 = ctk.CTkLabel(tab_vectores1, text="Operaciones con Vectores 1 (pendiente)")
    label_vectores1.pack(pady=10)

    # Pestaña "Distributiva"
    tab_distributiva = notebook.tab("Distributiva")
    label_distributiva = ctk.CTkLabel(tab_distributiva, text="Comprobación de la Propiedad Distributiva")
    label_distributiva.pack(pady=10)

    # Entrada para la matriz A
    global matriz_input_distributiva, vector_u_input, vector_v_input
    label_matriz = ctk.CTkLabel(tab_distributiva, text="Matriz A (copiar desde Excel):")
    label_matriz.pack(pady=5)
    matriz_input_distributiva = ctk.CTkTextbox(tab_distributiva, height=100)
    matriz_input_distributiva.pack(pady=10, padx=20)

    # Frame para alinear los inputs de los vectores en la misma fila
    frame_vectores = ctk.CTkFrame(tab_distributiva)
    frame_vectores.pack(pady=10)

    # Etiqueta y entrada para el vector u
    label_vector_u = ctk.CTkLabel(frame_vectores, text="Vector u:")
    label_vector_u.grid(row=0, column=0, padx=10)
    vector_u_input = ctk.CTkTextbox(frame_vectores, height=50, width=200)
    vector_u_input.grid(row=0, column=1, padx=10)

    # Etiqueta y entrada para el vector v
    label_vector_v = ctk.CTkLabel(frame_vectores, text="Vector v:")
    label_vector_v.grid(row=0, column=2, padx=10)
    vector_v_input = ctk.CTkTextbox(frame_vectores, height=50, width=200)
    vector_v_input.grid(row=0, column=3, padx=10)

    # Botón para calcular la propiedad distributiva
    btn_calcular_distributiva = ctk.CTkButton(tab_distributiva, text="Comprobar Distributiva", command=calcular_distributiva)
    btn_calcular_distributiva.pack(pady=10)

    # Consola de salida
    global consola_distributiva
    consola_distributiva = ctk.CTkTextbox(tab_distributiva, height=300, width=500, font=("Courier", global_font_size))
    consola_distributiva.pack(pady=10, padx=20)

    # Pestaña "Transpuesta"
    tab_Transpuesta = notebook.tab("Transpuesta")
    label_Transpuesta = ctk.CTkLabel(tab_Transpuesta, text="Transpuesta de una matriz o vector")
    label_Transpuesta.pack(pady=10)

    # Cuadro de texto para ingresar la matriz
    global matriz_input_transpuesta
    matriz_input_transpuesta = ctk.CTkTextbox(tab_Transpuesta, height=100)
    matriz_input_transpuesta.pack(pady=10, padx=20)

    # Consola para mostrar el resultado de la transposición
    global consola_transpuesta
    consola_transpuesta = ctk.CTkTextbox(tab_Transpuesta, height=200, width=500, font=("Courier", global_font_size))
    consola_transpuesta.pack(pady=10, padx=20)
    # Botón para transponer la matriz
    btn_transponer = ctk.CTkButton(tab_Transpuesta, text="Transponer Matriz", command=transponer_matriz)
    btn_transponer.pack(pady=5)
    # Botón para copiar la matriz en formato Excel
    btn_copiar = ctk.CTkButton(tab_Transpuesta, text="Copiar Formato Excel", command=copiar_matriz_formato_excel)
    btn_copiar.pack(pady=5)
    
    # Pestaña para cálculo de determinante
    tab_determinante = notebook.tab("Determinante")
    
    label_determinante = ctk.CTkLabel(tab_determinante, text="Determinante de una matriz")
    label_determinante.pack(pady=10)

    # Cuadro de texto para ingresar la matriz
    global matriz_input_determinante
    matriz_input_determinante = ctk.CTkTextbox(tab_determinante, height=100)
    matriz_input_determinante.pack(pady=10, padx=20)

        # Botón para calcular el determinante
    btn_calcular_det = ctk.CTkButton(tab_determinante, text="Calcular Determinante", command=calcular_determinante_tab)
    btn_calcular_det.pack(pady=5)
    
    # Consola para mostrar el resultado del determinante
    global consola_determinante
    consola_determinante = ctk.CTkTextbox(tab_determinante, height=200, width=500, font=("Courier", global_font_size))
    consola_determinante.pack(pady=10, padx=20)
    
    global consola_pasos_determinante
    consola_pasos_determinante = ctk.CTkTextbox(tab_determinante, height=200, width=500, font=("Courier", global_font_size))
    consola_pasos_determinante.pack(pady=10, padx=20)
    global btn_toggle_consola2
    btn_toggle_consola2 = ctk.CTkButton(tab_determinante, text="Ocultar Consolas", command=toggle_consola)
    btn_toggle_consola2.pack(pady=10)

    
    #Pestaña "Excel View"
    tab_excel = notebook.tab("Excel View")
        # Label para mostrar errores
    global label_error
    global frame_hoja
    label_error = ctk.CTkLabel(root, text="", text_color="red")
    label_error.pack(pady=5,in_=tab_excel)
    frame_hoja = ctk.CTkFrame(root)
    frame_hoja.pack(expand=True, fill="both", padx=10, pady=10,in_=tab_excel)
        # Crear entradas para filas y columnas
    label_filas = ctk.CTkLabel(tab_excel, text="Número de Filas:")
    label_filas.pack(pady=5)

    global entry_filas
    global entry_columnas
    entry_filas = ctk.CTkEntry(tab_excel, width=50)
    entry_filas.pack(pady=5)
    entry_filas.bind("<KeyRelease>", limpiar_error)

    label_columnas = ctk.CTkLabel(tab_excel, text="Número de Columnas:")
    label_columnas.pack(pady=5)

    entry_columnas = ctk.CTkEntry(tab_excel, width=50)
    entry_columnas.pack(pady=5)
    entry_columnas.bind("<KeyRelease>", limpiar_error)  # Limpiar error al escribir

    # Botón para generar la hoja de cálculo
    btn_generar = ctk.CTkButton(tab_excel,text="Generar Hoja", command=generar_hoja)
    btn_generar.pack(pady=10)
    # Botón para copiar la hoja en formato Excel
    btn_copiar_hoja = ctk.CTkButton(tab_excel, text="Copiar Hoja Formato Excel", command=copiar_hoja_formato_excel)
    btn_copiar_hoja.pack(pady=10)

    # Pestaña "Configuraciones" con botones para abrir popups
    tab_configuraciones = notebook.tab("Configuraciones")
    label_configuraciones = ctk.CTkLabel(tab_configuraciones, text="Ajustes de Configuración")
    label_configuraciones.pack(pady=10)

    # Botón para abrir el popup con pestañas de configuraciones
    btn_ajustar = ctk.CTkButton(tab_configuraciones, text="Ajustar Tamaños", command=abrir_popup_ajustes)
    btn_ajustar.pack(pady=10)

    tab_reportes = notebook.tab("Reportes")
    label_reportes = ctk.CTkLabel(tab_reportes, text="Generador de reportes LATEX")
    label_reportes.pack(pady=10)
    btn_generar_reporte = ctk.CTkButton(tab_reportes, text="Generar Reporte de Operaciones", command=generar_reporte)
    btn_generar_reporte.pack(pady=10)

    # Iniciar la aplicación
    root.mainloop()

# Verificar si el archivo se está ejecutando directamente y no como módulo importado
if __name__ == "__main__":
    iniciar_interfaz()


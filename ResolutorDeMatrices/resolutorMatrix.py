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
from io import StringIO

# Lista para almacenar las matricesSuma ingresadas en la pestaña de Suma Matrices
matricesSuma = []
matricesGlobal=[]
matricesMult = []
consola_visible = True
consola_matrices_visible = True
consola_pasos_determinante_visible = True
consola_pasos_inversa_visible=True
current_tab = None
matriz_suma_global = None  # Variable global para almacenar la matriz sumada
matriz_inversa_global= None
global_font_size = 12
# Inicializar las variables globales para la barra lateral
sidebar_width = 50  
sidebar_expanded_width = 200  
sidebar_visible = False  
buttons = []  

    
def imprimir_matriz_monoespaciada(consola, matriz):
    """
    Imprime una matriz en formato monoespaciado en la consola dada.
    
    :param consola: Widget de consola (por ejemplo, un CTkTextbox) donde se imprimirá la matriz.
    :param matriz: Lista de listas que representa la matriz a imprimir.
    """
    
    matriz_str = ""
    for fila in matriz:
        fila_str = " ".join(f"{elem:8.2f}" for elem in fila)  
        matriz_str += fila_str + "\n"  


    consola.insert("end", matriz_str)
    consola.see("end")  
    consola.configure(font=("Courier", global_font_size)) 

def resolver_Inversa():
    limpiar_consolas(consola_inversa, consola_inversa_pasos)
    matriz_str = matriz_input_inversa.get("1.0", ctk.END).strip()
    try:
        matriz = validar_entrada_matriz(matriz_str)
        if Validar_matriz_cuadrada(matriz):
            det,pasos=determinante(matriz)
            if det !=0:
                matriz = matriz_aumentada_con_identidad(matriz)
                pivoteoMax(matriz,True)

                consola_inversa.insert(ctk.END, "Inversa:\n")
                imprimir_matriz_monoespaciada(consola_inversa, obtener_segunda_mitad(matriz))
            else:
                consola_inversa.insert(ctk.END, "No existe Inversa de una matriz con un determinante igual a 0\n------ErrorType: det=0")
        else:
            consola_inversa.insert(ctk.END, "Error: La matriz debe ser cuadrada para tener inversa.\n")
    except ValueError as e:
        consola_inversa.insert("end", f"Error: {str(e)}\n")
    
def resolver_cramer():
    limpiar_consolas(consola_cramer,consola_cramer_pasos)  # Limpiar el contenido anterior en la consola
    matriz_str = matriz_input_cramer.get("1.0", ctk.END).strip()
    vector_str = vector_input_cramer.get("1.0", ctk.END).strip()
    
    try:
        matriz = validar_entrada_matriz(matriz_str)
        vector = [float(v) for v in vector_str.split()]
        
        if len(matriz) != len(vector):
            raise ValueError("La cantidad de filas de la matriz debe coincidir con la cantidad de elementos en el vector.")
        
        soluciones, pasos = cramer(matriz, vector)
        
        consola_cramer.insert(ctk.END, f"Soluciones: {soluciones}\n")
        consola_cramer_pasos.insert(ctk.END, pasos)
        
    except ValueError as e:
        consola_cramer.insert(ctk.END, f"Error: {str(e)}")
def copiar_y_pegar_matriz_en_consolas_seleccionadas(consolas_destino):
    try:
        matriz_copia = []

        # Recorrer la lista de listas (celdas_generadas) para obtener los valores
        for fila_celdas in celdas_generadas:
            fila_datos = [celda.get() for celda in fila_celdas]  # Obtener los valores de la fila
            matriz_copia.append("\t".join(fila_datos))  # Unir los valores con tabulaciones

        # Unir todas las filas con saltos de línea
        formato_excel = "\n".join(matriz_copia)

        # Pegar la matriz en las consolas seleccionadas
        for consola in consolas_destino:
            consola.delete("1.0", "end")
            consola.insert("end", formato_excel)

        label_error.configure(text="Matriz pegada en las consolas seleccionadas.", text_color="green")
        
    except Exception as e:
        label_error.configure(text=f"Error al copiar la matriz: {str(e)}", text_color="red")


def crear_seleccionador_consolas():
    # Ventana emergente para seleccionar consolas
    popup = ctk.CTkToplevel(root)
    popup.title("Seleccionar Consolas")
    popup.geometry("300x300")

    # Diccionario para almacenar los estados de los checkboxes
    consolas_seleccionadas = {}

    # Checkboxes para seleccionar las consolas donde se copiará la matriz
    check_suma = ctk.CTkCheckBox(popup, text="Suma Matrices", command=lambda: consolas_seleccionadas.update({"suma": matriz_input_suma}))
    check_suma.pack(pady=10)
    
    check_resolutor = ctk.CTkCheckBox(popup, text="Resolutor Matriz", command=lambda: consolas_seleccionadas.update({"resolutor": matriz_input}))
    check_resolutor.pack(pady=10)

    check_transpuesta = ctk.CTkCheckBox(popup, text="Transpuesta", command=lambda: consolas_seleccionadas.update({"transpuesta": matriz_input_transpuesta}))
    check_transpuesta.pack(pady=10)

    check_determinante = ctk.CTkCheckBox(popup, text="Determinante", command=lambda: consolas_seleccionadas.update({"determinante": matriz_input_determinante}))
    check_determinante.pack(pady=10)
    check_cramer = ctk.CTkCheckBox(popup, text="Cramer", command=lambda: consolas_seleccionadas.update({"determinante": matriz_input_cramer}))
    check_cramer.pack(pady=10)

    # Botón para aplicar la selección
    btn_aplicar = ctk.CTkButton(popup, text="Copiar a Consolas Seleccionadas",
                                command=lambda: copiar_y_pegar_matriz_en_consolas_seleccionadas(consolas_seleccionadas.values()))
    btn_aplicar.pack(pady=10)
    
# Función que usa la interfaz tkinter para generar la matriz y calcular el determinante
def calcular_determinante_tab():
    try:
        limpiar_consolas(consola_determinante,consola_pasos_determinante)
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
        pass


def verificar_cambio_pestana():
    global current_tab
    nueva_tab = notebook.get()

    if nueva_tab != current_tab:
        current_tab = nueva_tab
        redirigir_consola()  # Redirigir la consola cuando se detecte un cambio de pestaña
    
    # Llamar a esta función periódicamente
    root.after(100, verificar_cambio_pestana)  # Cada 100 ms se verifica si la pestaña cambió

def redirigir_consola():
    # Obtener el nombre de la pestaña seleccionada
    tab_actual = notebook.get()
    
    if tab_actual == "Suma Matrices":
        sys.stdout = TextRedirector(consola_suma)
    elif tab_actual == "Inversa":
        sys.stdout = TextRedirector(consola_inversa_pasos)
    elif tab_actual == "Determinante":
        sys.stdout = TextRedirector(consola_pasos_determinante)
    elif tab_actual == "Resolutor Matriz":
        sys.stdout = TextRedirector(consola_textbox)
    elif tab_actual == "Cramer":
        sys.stdout = TextRedirector(consola_cramer)
    elif tab_actual == "Transpuesta":
        sys.stdout = TextRedirector(consola_transpuesta)
    elif tab_actual == "Distributiva":
        sys.stdout = TextRedirector(consola_distributiva)

    else:
        sys.stdout = None  # O redirigir a otro lugar si ninguna coincide

def ajustar_tamano_fuente(valor):
    global global_font_size
    global_font_size = int(valor)

    # Actualizar el tamaño de fuente de los widgets que tengan texto
    widgets = [consola_textbox,consola_suma,consola_matrices_listadas, consola_distributiva, consola_transpuesta,consola_pasos_determinante]
    for widget in widgets:
        widget.configure(font=("Courier", global_font_size))
def ajustar_tamano_texto(consola,event=None):
    contenido = consola.get("1.0", "end-1c")
    num_filas = contenido.count("\n") + 1
    # Ajustar la altura dinámica
    nueva_altura = min(max(100, num_filas * 20), 400)
    # Calcular la longitud de la fila más larga
    filas = contenido.split("\n")
    max_ancho_fila = max(len(fila) for fila in filas) if filas else 0
    # Ajustar el ancho dinámico
    nueva_anchura = min(max(200, max_ancho_fila * 10), 600)
    # Configurar la nueva altura y ancho del widget
    consola.configure(height=nueva_altura, width=nueva_anchura)

def ajustar_altura_consolas(valor):
    altura = int(valor)
    widgets = [consola_textbox, consola_matrices_listadas, consola_distributiva, consola_transpuesta,consola_pasos_determinante]
    for widget in widgets:
        widget.configure(height=altura)

def ajustar_ancho_consolas(valor):
    ancho = int(valor)
    widgets = [consola_textbox, consola_matrices_listadas, consola_distributiva, consola_transpuesta,consola_pasos_determinante]
    for widget in widgets:
        widget.configure(width=ancho)
        
    
# Función para ocultar el contenido del sidebar inmediatamente
def hide_sidebar():
    global sidebar_visible
    sidebar_frame_content.forget() # Colapsar el sidebar a 0 de ancho
    sidebar_visible = False  # El sidebar ya está oculto

# Función para mostrar el contenido del sidebar inmediatamente
def show_sidebar(icon_button):
    global sidebar_visible
    sidebar_frame_content.pack(side="left", fill="y")  # Vuelve a colocar el sidebar en la vista
    sidebar_visible = True  # El sidebar ya está visible
    mostrar_contenido(icon_button)  # Mostrar el contenido relacionado con el icono

# Función para alternar la visibilidad del sidebar
def toggle_sidebar(icon_button):
    global sidebar_visible
    if sidebar_visible:
        hide_sidebar()  # Si está visible, lo ocultamos
    else:
        show_sidebar(icon_button)  # Si está oculto, lo mostramos
    
def toggle_consola():
    global consola_matrices_visible, consola_pasos_determinante_visible,consola_pasos_inversa_visible
    
    def configurar_consola(consola, toggle_btn, visible):
        if visible:
            consola.pack_forget()
            toggle_btn.configure(text="Mostrar Consolas")
        else:
            toggle_btn.configure(text="Ocultar Consolas")
            consola.pack(padx=20)
            
    configurar_consola(consola_matrices_listadas, btn_toggle_consola1, consola_matrices_visible)
    configurar_consola(consola_pasos_determinante, btn_toggle_consola2, consola_pasos_determinante_visible)
    configurar_consola(consola_inversa_pasos,btn_toggle_consola3,consola_pasos_inversa_visible)
    consola_matrices_visible= not consola_matrices_visible
    consola_pasos_determinante_visible= not consola_pasos_determinante_visible
    consola_pasos_inversa_visible= not consola_pasos_inversa_visible

def limpiar_consolas(*consolas):
    for consola in consolas:
        consola.delete("1.0", "end")

def limpiar_contenido_consola(event, consola):
    consola.delete("1.0", "end")

def mostrar_matrices_en_consola():
    limpiar_consolas(consola_suma, consola_matrices_listadas)
    
    if not matricesSuma:
        consola_matrices_listadas.insert("end", "No hay matricesSuma almacenadas.\n")
        return
    
    consola_matrices_listadas.insert("end", "Matrices almacenadas:\n")
    for idx, matriz in enumerate(matricesSuma):
        consola_matrices_listadas.insert("end", f"Matriz {idx + 1}:\n")
        for fila in matriz:
            consola_matrices_listadas.insert("end"," ".join(f"{elem:8.2f}" for elem in fila)+"\n\n")

# Función genérica para mostrar contenido en el sidebar con un botón de "Regresar"
def mostrar_contenido_con_regreso(funcion_regreso, crear_contenido_funcion):
    """
    Muestra contenido en el sidebar con un botón de "Regresar".
    
    :param funcion_regreso: Función que se ejecuta al hacer clic en el botón "Regresar".
    :param crear_contenido_funcion: Función que crea el contenido específico que se quiere mostrar en el sidebar.
    """
    # Limpiar el contenido anterior
    for widget in sidebar_frame_content.winfo_children():
        widget.destroy()

    # Agregar el botón "Regresar"
    btn_regresar = ctk.CTkButton(sidebar_frame_content, text="←", width=20, height=20, command=funcion_regreso)
    btn_regresar.pack(anchor="ne", pady=5, padx=5)

    # Mostrar el contenido que se pase a través de la función
    crear_contenido_funcion()

# Funciones para crear contenidos específicos que se quieren mostrar
def crear_contenido_ajustar_fuente():
    # Contenido específico para el ajuste de fuente
    label_fuente = ctk.CTkLabel(sidebar_frame_content, text="Ajustar Tamaño de Fuente Global")
    label_fuente.pack(pady=10)
    
    slider_fuente = ctk.CTkSlider(sidebar_frame_content, from_=8, to=24, command=ajustar_tamano_fuente)
    slider_fuente.pack(pady=20)
    slider_fuente.set(global_font_size)  # Valor inicial

def crear_contenido_ajustar_consolas():
    # Contenido específico para el ajuste de consolas
    label_altura = ctk.CTkLabel(sidebar_frame_content, text="Altura de Consolas")
    label_altura.pack(pady=5)
    
    slider_altura = ctk.CTkSlider(sidebar_frame_content, from_=100, to=500, command=ajustar_altura_consolas)
    slider_altura.pack(pady=10)
    slider_altura.set(300)  # Valor inicial

    label_ancho = ctk.CTkLabel(sidebar_frame_content, text="Ancho de Consolas")
    label_ancho.pack(pady=5)
    
    slider_ancho = ctk.CTkSlider(sidebar_frame_content, from_=200, to=1200, command=ajustar_ancho_consolas)
    slider_ancho.pack(pady=10)
    slider_ancho.set(500)  # Valor inicial

# Función para volver a la pantalla de opciones de configuraciones
def volver_a_opciones_configuracion():
    mostrar_contenido("configuraciones")

# Modificar las funciones para mostrar los deslizadores e incluir el botón "Regresar" usando la función genérica
def mostrar_ajustar_fuente():
    mostrar_contenido_con_regreso(volver_a_opciones_configuracion, crear_contenido_ajustar_fuente)

def mostrar_ajustar_consolas():
    mostrar_contenido_con_regreso(volver_a_opciones_configuracion, crear_contenido_ajustar_consolas)

# Función para mostrar la lista de matrices almacenadas en el sidebar
def mostrar_matrices_almacenadas():
    # Limpiar el contenido anterior del sidebar
    for widget in sidebar_frame_content.winfo_children():
        widget.destroy()

    # Título para las matrices almacenadas
    label = ctk.CTkLabel(sidebar_frame_content, text="Matrices Almacenadas", font=("Courier", 14))
    label.pack(pady=10)

    # Frame donde se mostrará la lista de matrices
    frame_matrices = ctk.CTkFrame(sidebar_frame_content)
    frame_matrices.pack(fill="both", expand=True, padx=10, pady=10)

    # Mostrar cada matriz en formato monoespaciado y hacerlo arrastrable
    for i, matriz in enumerate(matricesGlobal):
        # Convertir la matriz a texto monoespaciado
        matriz_str = "\n".join([" ".join(f"{elem:8.2f}" for elem in fila) for fila in matriz])
        
        # Crear una etiqueta que sea "arrastrable"
        label_matriz = ctk.CTkLabel(frame_matrices, text=f"Matriz {i + 1}:\n{matriz_str}", font=("Courier", 10))
        label_matriz.pack(pady=5)

        # Hacer que la etiqueta sea arrastrable (drag and drop)
        label_matriz.bind("<Button-1>", lambda event, text=matriz_str: iniciar_arrastre(event, text))

    # Botón para regresar al menú principal del sidebar
    agregar_boton_regresar()# Función para cambiar el contenido del sidebar según el botón de icono

# Función para agregar el input de una consola a matrizGlobal
def agregar_a_matriz_global(result, consola):
    try:
        # Verificar si el resultado es una matriz válida
        if result is not None:
            # Agregar la matriz a matrizGlobal
            matricesGlobal.append(result)
            if consola:
                consola.insert("end", "Matriz agregada a matrizGlobal.\n")
        else:
            if consola:
                consola.insert("end", "Error: No se pudo agregar la matriz.\n")
    except Exception as e:
        if consola:
            consola.insert("end", f"Error: {str(e)}\n")

arrastre_activo = False
def iniciar_arrastre(event, text):
    global arrastre_activo
    arrastre_activo=True
    widget = event.widget
    widget._drag_data = text  # Guardar el texto a arrastrar
    root.clipboard_clear()  # Limpiar el portapapeles
    root.clipboard_append(text)  # Copiar el texto en el portapapeles

# Función para realizar el arrastre (drag)
def arrastrar_matriz(event):
    widget = event.widget
    widget.place(x=event.x_root, y=event.y_root)  # Mover el widget mientras se arrastra

def soltar_matriz(event, consola_input):
    global arrastre_activo
    if arrastre_activo:  # Solo permitir soltar si el arrastre está activo
        try:
            # Obtener el contenido del portapapeles
            text = root.clipboard_get() 
            # Insertar el texto en la consola
            consola_input.insert("end", text + "\n")
            consola_input.see("end")  # Desplazar la vista al final del texto
            arrastre_activo = False  # Desactivar el arrastre después de pegar
        except Exception as e:
            consola_input.insert("end", f"Error al soltar la matriz: {str(e)}\n")


# Modificar el comportamiento de las consolas para aceptar "drop"
def hacer_consola_droppable(consola):
    consola.bind("<ButtonRelease-1>", lambda event: soltar_matriz(event, consola))

def mostrar_contenido(icon_button):
    # Limpiar el contenido anterior
    for widget in sidebar_frame_content.winfo_children():
        widget.destroy()

    # Cambiar el contenido del sidebar dependiendo del icono presionado
    if icon_button == "configuraciones":
        label = ctk.CTkLabel(sidebar_frame_content, text="Ajustes de Configuración")
        label.pack(pady=10)
        
        # Botón para ajustar el tamaño de la fuente
        btn_ajustar_fuente = ctk.CTkButton(sidebar_frame_content, text="Ajustar Tamaño de Fuente", command=mostrar_ajustar_fuente)
        btn_ajustar_fuente.pack(pady=10)
        
        # Botón para ajustar el tamaño de las consolas
        btn_ajustar_consolas = ctk.CTkButton(sidebar_frame_content, text="Ajustar Tamaño de Consolas", command=mostrar_ajustar_consolas)
        btn_ajustar_consolas.pack(pady=10)
        
    elif icon_button == "matrices_almacenadas":
        mostrar_matrices_almacenadas()

def crear_widget(tipo, texto, comando=None, padre=None, **kwargs):
    widget = tipo(padre, text=texto, command=comando, **kwargs)
    widget.pack(pady=10)
    return widget
def agregar_boton_regresar():
    # Crear un botón pequeño en la esquina superior derecha del sidebar
    btn_regresar = ctk.CTkButton(sidebar_frame_content, text="←", width=20, height=20, 
                                 command=volver_a_opciones_configuracion)
    btn_regresar.pack(anchor="ne", pady=5, padx=5)  # Posicionar en la esquina superior derecha
def agregar_boton(texto, comando):
    button = ctk.CTkButton(sidebar_frame, text=texto, command=comando)
    button.pack(pady=10)
    buttons.append(button)  


def agregar_matriz():
    input_text = matriz_input_suma.get("1.0", "end-1c")
    matriz = validar_entrada_matriz(input_text)
    if matriz is not None and input_text:
        matricesSuma.append(matriz)
        logger.log("Matriz agregada", matriz)
        matriz_input_suma.delete("1.0", "end")
    else:
        consola_suma.insert("end", "Error: Asegúrate de que la matriz contiene solo números.\n")
        
def mostrar_checkboxes_matrices():
    # Limpiar cualquier widget anterior
    for widget in checkboxes_frame.winfo_children():
        widget.destroy()

    # Diccionario para almacenar el estado de los checkboxes
    checkboxes = {}
    
    # Crear un checkbox para cada matriz en matricesSuma
    for i, matriz in enumerate(matricesSuma):
        var = ctk.IntVar(value=0)  # Variable para almacenar el estado del checkbox
        checkbox = ctk.CTkCheckBox(checkboxes_frame, text=f"Matriz {i+1}", variable=var)
        checkbox.pack(anchor="w", padx=10, pady=5)
        checkboxes[i] = var  # Asociar el índice de la matriz con el checkbox

    # Crear el botón eliminar
    btn_eliminar = ctk.CTkButton(checkboxes_frame, text="Eliminar Seleccionadas", command=lambda: eliminar_matrices_seleccionadas(checkboxes))
    btn_eliminar.pack(pady=10)

    checkboxes_frame.pack(pady=10, padx=10)

def eliminar_matrices_seleccionadas(checkboxes):
    global matricesSuma

    # Obtener los índices de las matrices seleccionadas
    indices_seleccionados = [i for i, var in checkboxes.items() if var.get() == 1]

    # Eliminar las matrices seleccionadas
    matricesSuma = [matriz for i, matriz in enumerate(matricesGlobal) if i not in indices_seleccionados]

    # Limpiar la consola de lista de matrices y recargarla
    consola_matrices_listadas.delete("1.0", "end")
    mostrar_matrices_en_consola()

    # Limpiar los checkboxes después de eliminar
    for widget in checkboxes_frame.winfo_children():
        widget.destroy()
        

def obtener_y_resolver_matriz(matriz_input, consola_textbox):
    consola_textbox.delete("1.0", "end")  # Limpiar el contenido anterior en la consola
    input_text = matriz_input.get("1.0", "end-1c")  # Obtener texto desde el widget de texto
    matriz = validar_entrada_matriz(input_text)
    
    if matriz is not None:
        print("Matriz inicial:")
        printMatrix(matriz,False)

        pivoteoMax(matriz,False)

        print("Matriz después del pivoteo:")
        printMatrix(matriz,False)

        print("Resultados finales:")
        printResult(matriz,False)
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
    copiar_matriz_en_formato_excel(matriz_suma_global, consola_suma, root, 
                                   mensaje_exito="Matriz sumada copiada en formato Excel.", 
                                   mensaje_error="Error: No hay matriz sumada para copiar.")

def conseguir_matriz(matriz, consola=None, root=None, mensaje_exito="Matriz Guardada a Matrices Globales.", mensaje_error="Error: No hay matriz para guardar."):
    if matriz is None or not matriz:
        if consola:
            consola.insert("end", mensaje_error + "\n")
        return
    
    try:
        # Si la matriz es un conjunto de widgets como celdas_generadas, construimos la matriz
        if isinstance(matriz[0], list) and isinstance(matriz[0][0], ctk.CTkEntry):
            matriz_copia = []
            for fila_celdas in matriz:
                fila_datos = [celda.get() for celda in fila_celdas]  # Obtener los valores de la fila
                matriz_copia.append("\t".join(fila_datos))  # Unir los valores con tabulaciones
            formato_excel = "\n".join(matriz_copia)
        else:
            formato_excel = "\n".join(["\t".join(map(str, fila)) for fila in matriz])
        if consola:
            consola.insert("end", mensaje_exito + "\n")
        return validar_entrada_matriz(formato_excel)

    except Exception as e:
        if consola:
            consola.insert("end", f"{mensaje_error}: {str(e)}\n")

def copiar_matriz_en_formato_excel(matriz, consola=None, root=None, mensaje_exito="Matriz copiada en formato Excel.", mensaje_error="Error: No hay matriz para copiar."):
    if matriz is None or not matriz:
        if consola:
            consola.insert("end", mensaje_error + "\n")
        return
    
    try:
        # Si la matriz es un conjunto de widgets como celdas_generadas, construimos la matriz
        if isinstance(matriz[0], list) and isinstance(matriz[0][0], ctk.CTkEntry):
            matriz_copia = []
            for fila_celdas in matriz:
                fila_datos = [celda.get() for celda in fila_celdas]  # Obtener los valores de la fila
                matriz_copia.append("\t".join(fila_datos))  # Unir los valores con tabulaciones
            formato_excel = "\n".join(matriz_copia)
        else:
            # Si la matriz es una lista de listas de números
            formato_excel = "\n".join(["\t".join(map(str, fila)) for fila in matriz])

        # Copiar al portapapeles
        root.clipboard_clear()
        root.clipboard_append(formato_excel)
        root.update()  # Mantener el portapapeles actualizado

        if consola:
            consola.insert("end", mensaje_exito + "\n")

    except Exception as e:
        if consola:
            consola.insert("end", f"{mensaje_error}: {str(e)}\n")


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
    copiar_matriz_en_formato_excel(matriz_transpuesta, consola_transpuesta, root, 
                                   mensaje_exito="Matriz transpuesta copiada en formato Excel.", 
                                   mensaje_error="No hay matriz transpuesta para copiar.")

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
    copiar_matriz_en_formato_excel(celdas_generadas, None, root, 
                                   mensaje_exito="Hoja copiada en formato Excel.", 
                                   mensaje_error="Error al copiar la hoja.")



# Función para limpiar el mensaje de error
def limpiar_error(event):
    label_error.configure(text="")
def mostrar_menu_agregar_eliminar(menu, frame, btn_text):
    if menu.winfo_ismapped():
        menu.pack_forget()  # Ocultar el menú si está visible
    else:
        menu.pack(side="left",padx=5, pady=5)  # Mostrar el menú debajo del botón
def mostrar_menu_copiar_guardar(menu, frame, btn_text):
    if menu.winfo_ismapped():
        menu.pack_forget()  # Ocultar el menú si está visible
    else:
        menu.pack(side="left",padx=5, pady=5)  # Mostrar el menú debajo del botón
def limpiar_menus(event, menu1, menu2):
    if not event.widget in (menu1, menu2):
        menu1.pack_forget()
        menu2.pack_forget()

# Función para inicializar la interfaz
def iniciar_interfaz():
    # Inicializar customtkinter
    ctk.set_appearance_mode("dark")  # Modo oscuro (opcional)
    ctk.set_default_color_theme("blue")  # Tema de color

    global root, sidebar_frame, sidebar_frame_content
    
    # Inicializar la ventana principal
    root = ctk.CTk()
    root.title("MATRIXCALC")
    root.geometry("1000x600")
    

    # Crear el frame para la barra lateral de iconos
    sidebar_frame = ctk.CTkFrame(root, width=sidebar_width, height=600)
    sidebar_frame.pack(side="left", fill="y")

    # Botón o icono de Configuraciones
    btn_configuraciones = ctk.CTkButton(sidebar_frame, text="⚙", width=40, height=40, command=lambda: toggle_sidebar("configuraciones"))
    btn_configuraciones.pack(pady=10)
    btn_matrices_almacenadas = ctk.CTkButton(sidebar_frame, text="Matrices Almacenadas", width=40, height=40, command=lambda: toggle_sidebar("matrices_almacenadas"))
    btn_matrices_almacenadas.pack(pady=10)

    # Crear el frame para el contenido expandido del sidebar
    sidebar_frame_content = ctk.CTkFrame(root, width=0, height=600)
    sidebar_frame_content.pack(side="left", fill="y")

    # Crear el notebook de pestañas
    global notebook
    notebook = ctk.CTkTabview(root)
    notebook.pack(side="right", fill="both", expand=True)

    # Crear pestañas
    notebook.add("Resolutor Matriz")
    notebook.add("Suma Matrices")
    notebook.add("Vectores 1")
    notebook.add("Distributiva")
    notebook.add("Transpuesta")
    notebook.add("Determinante")
    notebook.add("Inversa")
    notebook.add("Cramer")
    notebook.add("Reportes")
    notebook.add("Excel View")

    # Pestaña "Resolutor Matriz"
    tab_resolutor = notebook.tab("Resolutor Matriz")
    label_resolutor = ctk.CTkLabel(tab_resolutor, text="Ingresa la matriz copiada desde Excel:")
    label_resolutor.pack(pady=10)

    # Crear widget de texto para ingresar la matriz
    global matriz_input
    matriz_input = ctk.CTkTextbox(tab_resolutor, height=100)
    matriz_input.pack(pady=10, padx=20)
    matriz_input.bind("<KeyRelease>", lambda event: ajustar_tamano_texto(matriz_input))  # Ajustar tamaño al escribir

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

    # Etiqueta de instrucción
    label_suma = ctk.CTkLabel(tab_suma, text="Ingresa una matriz copiada desde Excel (formato de tabla):")
    label_suma.pack(pady=10)

    # Entrada de texto para las matrices
    global matriz_input_suma
    matriz_input_suma = ctk.CTkTextbox(tab_suma, height=100)
    matriz_input_suma.pack(pady=10, padx=20)
    matriz_input_suma.bind("<KeyRelease>", lambda event: ajustar_tamano_texto(matriz_input_suma))  # Ajustar tamaño al escribir

    # Frame para los botones de acción
    btn_frame = ctk.CTkFrame(tab_suma)
    btn_frame.pack(pady=5)

    # Crear menú desplegable para agregar/eliminar matrices
    menu_agregar_eliminar = ctk.CTkFrame(btn_frame)
    menu_agregar_eliminar.pack_forget()

    btn_agregar = ctk.CTkButton(menu_agregar_eliminar, text="Agregar Matriz", command=agregar_matriz)
    btn_agregar.configure(fg_color="green", text_color="black")
    btn_agregar.pack(pady=5)

    btn_mostrar_checkboxes = ctk.CTkButton(menu_agregar_eliminar, text="Seleccionar Matrices para Eliminar", command=mostrar_checkboxes_matrices)
    btn_mostrar_checkboxes.configure(fg_color="green", text_color="black")
    btn_mostrar_checkboxes.pack(pady=5)

    # Crear menú desplegable para copiar formato Excel/guardar resultado
    menu_copiar_guardar = ctk.CTkFrame(btn_frame)
    menu_copiar_guardar.pack_forget()

    btn_copiar_matriz_suma = ctk.CTkButton(menu_copiar_guardar, text="Copiar Formato Excel", command=copiar_matriz_suma_formato_excel)
    btn_copiar_matriz_suma.configure(fg_color="red", text_color="white")
    btn_copiar_matriz_suma.pack(pady=5)

    btn_matrices_global_suma = ctk.CTkButton(menu_copiar_guardar, text="Guardar Resultado", command=lambda: agregar_a_matriz_global(matriz_suma_global, consola_suma))
    btn_matrices_global_suma.configure(fg_color="red", text_color="white")
    btn_matrices_global_suma.pack(pady=5)
    
    # Botón para resolver la suma de matrices
    btn_resolver_suma = ctk.CTkButton(btn_frame, text="Resolver", command=resolver_matrices)
    btn_resolver_suma.pack(side="left", padx=5)
    #Boton para Mostrar lista de matrices
    btn_mostrar_lista_matriz_suma = ctk.CTkButton(btn_frame,text="Mostrar Lista de Matrices",command=mostrar_matrices_en_consola)
    btn_mostrar_lista_matriz_suma.pack(side="left",padx=5)
    # Botones principales que muestran el menú desplegable
    btn_agregar_eliminar = ctk.CTkButton(btn_frame, text="Agregar/Eliminar", command=lambda: mostrar_menu_agregar_eliminar(menu_agregar_eliminar, btn_frame, "Agregar/Eliminar"))
    btn_agregar_eliminar.configure(fg_color="green", text_color="black")
    btn_agregar_eliminar.pack(padx=5)

    btn_copiar_guardar = ctk.CTkButton(btn_frame, text="Copiar/Guardar", command=lambda: mostrar_menu_copiar_guardar(menu_copiar_guardar, btn_frame, "Copiar/Guardar"))
    btn_copiar_guardar.configure(fg_color="red", text_color="white")
    btn_copiar_guardar.pack(padx=5)
    

    # Consola para la salida de la operación Suma Matrices
    global consola_suma
    consola_suma = ctk.CTkTextbox(tab_suma, height=200, width=500, font=("Courier", global_font_size))
    consola_suma.pack(pady=10, padx=20)
    
    # Botón para mostrar las matrices (toggle consola)
    global btn_toggle_consola1
    btn_toggle_consola1 = ctk.CTkButton(tab_suma, text="Ocultar Consolas", command=toggle_consola)
    btn_toggle_consola1.pack(pady=10)

    # Consola para la lista de matrices (mostrada u oculta con el botón toggle)
    global consola_matrices_listadas
    consola_matrices_listadas = ctk.CTkTextbox(tab_suma, height=200, width=500, font=("Courier", global_font_size))
    consola_matrices_listadas.pack(pady=10, padx=20)

    # Frame para los checkboxes
    global checkboxes_frame
    checkboxes_frame = ctk.CTkFrame(tab_suma)


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
    matriz_input_distributiva.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(matriz_input_distributiva))  # Ajustar tamaño al escribir

    # Frame para alinear los inputs de los vectores en la misma fila
    frame_vectores = ctk.CTkFrame(tab_distributiva)
    frame_vectores.pack(pady=10)

    # Etiqueta y entrada para el vector u
    label_vector_u = ctk.CTkLabel(frame_vectores, text="Vector u:")
    label_vector_u.grid(row=0, column=0, padx=10)
    vector_u_input = ctk.CTkTextbox(frame_vectores, height=50, width=200)
    vector_u_input.grid(row=0, column=1, padx=10)
    vector_u_input.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(vector_u_input))  # Ajustar tamaño al escribir

    # Etiqueta y entrada para el vector v
    label_vector_v = ctk.CTkLabel(frame_vectores, text="Vector v:")
    label_vector_v.grid(row=0, column=2, padx=10)
    vector_v_input = ctk.CTkTextbox(frame_vectores, height=50, width=200)
    vector_v_input.grid(row=0, column=3, padx=10)
    vector_v_input.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(vector_v_input))  # Ajustar tamaño al escribir

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
    matriz_input_transpuesta.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(matriz_input_transpuesta))  # Ajustar tamaño al escribir

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
    # Boton para agregar a matrices global
    btn_agregar_matriz_globalT=ctk.CTkButton(tab_Transpuesta, text="Guardar Matriz", command=lambda:agregar_a_matriz_global(matriz_transpuesta,consola_transpuesta))
    btn_agregar_matriz_globalT.pack(pady=5)
    
    
    # Pestaña para cálculo de determinante
    tab_determinante = notebook.tab("Determinante")
    
    # Crear un frame scrolleable para la pestaña "Regla de Cramer"
    scrollable_frame_determinante = ctk.CTkScrollableFrame(tab_determinante)
    scrollable_frame_determinante.pack(fill="both", expand=True)
    
    label_determinante = ctk.CTkLabel(scrollable_frame_determinante, text="Determinante de una matriz")
    label_determinante.pack(pady=10)

    # Cuadro de texto para ingresar la matriz
    global matriz_input_determinante
    matriz_input_determinante = ctk.CTkTextbox(scrollable_frame_determinante, height=100)
    matriz_input_determinante.pack(pady=10, padx=20)
    matriz_input_determinante.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(matriz_input_determinante))  # Ajustar tamaño al escribir

        # Botón para calcular el determinante
    btn_calcular_det = ctk.CTkButton(scrollable_frame_determinante, text="Calcular Determinante", command=calcular_determinante_tab)
    btn_calcular_det.pack(pady=5)
    
    # Consola para mostrar el resultado del determinante
    global consola_determinante
    consola_determinante = ctk.CTkTextbox(scrollable_frame_determinante, height=200, width=500, font=("Courier", global_font_size))
    consola_determinante.pack(pady=10, padx=20)
    global btn_toggle_consola2
    btn_toggle_consola2 = ctk.CTkButton(scrollable_frame_determinante, text="Ocultar Consolas", command=toggle_consola)
    btn_toggle_consola2.pack(pady=10)
    global consola_pasos_determinante
    consola_pasos_determinante = ctk.CTkTextbox(scrollable_frame_determinante, height=200, width=500, font=("Courier", global_font_size))
    consola_pasos_determinante.pack(pady=10, padx=20)
    # Pestana Inversa
    tab_inversa=notebook.tab("Inversa")
    scrollable_frame_inversa=ctk.CTkScrollableFrame(tab_inversa)
    scrollable_frame_inversa.pack(fill="both",expand=True)
    label_inversa=ctk.CTkLabel(scrollable_frame_inversa, text="Ingresa la matriz cuadrada para obtener su inversa:")
    label_inversa.pack(pady=10)
    global matriz_input_inversa
    matriz_input_inversa=ctk.CTkTextbox(scrollable_frame_inversa, height=200, width=400)
    matriz_input_inversa.pack(pady=10,padx=20)
    matriz_input_inversa.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(matriz_input_inversa))  # Ajustar tamaño al escribir
    #Boton para Resolver usando Gauss Jordan
    btn_inversa= ctk.CTkButton(scrollable_frame_inversa, text="Resolver con Gauss", command=resolver_Inversa)
    btn_inversa.pack(pady=5)
    #Consola Inversa Pasos y Resultado
    global consola_inversa_pasos, consola_inversa
    consola_inversa = ctk.CTkTextbox(scrollable_frame_inversa, height=300, width=500, font=("Courier", global_font_size))
    consola_inversa.pack(pady=10, padx=20)
    global btn_toggle_consola3
    btn_toggle_consola3 = ctk.CTkButton(scrollable_frame_inversa, text="Ocultar Consolas", command=toggle_consola)
    btn_toggle_consola3.pack(pady=10)
    consola_inversa_pasos = ctk.CTkTextbox(scrollable_frame_inversa, height=300, width=500, font=("Courier", global_font_size))
    consola_inversa_pasos.pack(pady=10, padx=20)


    # Pestaña "Regla de Cramer"
    tab_cramer = notebook.tab("Cramer")
    # Crear un frame scrolleable para la pestaña "Regla de Cramer"
    scrollable_frame_cramer = ctk.CTkScrollableFrame(tab_cramer)
    scrollable_frame_cramer.pack(fill="both", expand=True)

    # Etiqueta de instrucción
    label_cramer = ctk.CTkLabel(scrollable_frame_cramer, text="Ingresa la matriz de coeficientes y el vector de términos independientes:")
    label_cramer.pack(pady=10)
    # Cuadro de texto para ingresar la matriz de coeficientes
    global matriz_input_cramer
    matriz_input_cramer = ctk.CTkTextbox(scrollable_frame_cramer, height=200, width=400)
    matriz_input_cramer.pack(pady=10, padx=20)
    matriz_input_cramer.bind("<KeyRelease>", lambda event:ajustar_tamano_texto(matriz_input_cramer))  # Ajustar tamaño al escribir

    # Cuadro de texto para ingresar el vector de términos independientes
    global vector_input_cramer
    vector_input_cramer = ctk.CTkTextbox(scrollable_frame_cramer, height=50, width=400)
    vector_input_cramer.pack(pady=10, padx=20)

    # Botón para resolver usando la Regla de Cramer
    btn_cramer = ctk.CTkButton(scrollable_frame_cramer, text="Resolver con Cramer", command=resolver_cramer)
    btn_cramer.pack(pady=5)

    # Consola para mostrar los resultados y pasos de Cramer
    global consola_cramer_pasos, consola_cramer
    consola_cramer_pasos = ctk.CTkTextbox(scrollable_frame_cramer, height=300, width=500, font=("Courier", global_font_size))
    consola_cramer_pasos.pack(pady=10, padx=20)

    consola_cramer = ctk.CTkTextbox(scrollable_frame_cramer, height=300, width=500, font=("Courier", global_font_size))
    consola_cramer.pack(pady=10, padx=20)

    

    
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
    btn_agregar_matriz_global=ctk.CTkButton(tab_excel, text="Guardar Matriz",command=lambda:agregar_a_matriz_global(conseguir_matriz(celdas_generadas,None,root,mensaje_exito="Guardado con exito",mensaje_error="No se ha podido guardar la matriz"),None))
    btn_agregar_matriz_global.pack(pady=10)
    btn_seleccionar_consolas = ctk.CTkButton(tab_excel, text="Seleccionar Consolas",
                                         command=crear_seleccionador_consolas)
    btn_seleccionar_consolas.pack(pady=10)

    # Modificar las consolas para que acepten el "drop"
    matriz_input.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input))
    hacer_consola_droppable(matriz_input)
    
    matriz_input_suma.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_suma))
    hacer_consola_droppable(matriz_input_suma)
    
    matriz_input_cramer.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_cramer))
    hacer_consola_droppable(matriz_input_cramer)
    vector_input_cramer.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,vector_input_cramer))
    hacer_consola_droppable(vector_input_cramer)
    
    matriz_input_distributiva.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_distributiva))
    hacer_consola_droppable(matriz_input_distributiva)
    hacer_consola_droppable(vector_u_input)
    hacer_consola_droppable(vector_v_input)
    
    matriz_input_determinante.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_determinante))
    hacer_consola_droppable(matriz_input_determinante)
    
    matriz_input_inversa.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_inversa))
    hacer_consola_droppable(matriz_input_inversa)

    matriz_input_transpuesta.bind("<Button-3>",lambda event: limpiar_contenido_consola(event,matriz_input_transpuesta))
    hacer_consola_droppable(matriz_input_transpuesta)
    # Llamar a la función de verificación periódica después de iniciar la interfaz
    verificar_cambio_pestana()

    # Iniciar la aplicación
    root.mainloop()

# Verificar si el archivo se está ejecutando directamente y no como módulo importado
if __name__ == "__main__":
    iniciar_interfaz()


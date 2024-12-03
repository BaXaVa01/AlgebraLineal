# main.py
import customtkinter as ctk
from tkinter import ttk, Text, messagebox
import biseccion_logic  
import newton_raphson_logic  
import math
from math import sin, cos, tan, log, sqrt, pi, e
import re
import numpy as np
from plotter import graficar_funcion
from sympy import sympify, latex, symbols
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
  # Importa el archivo de animación
import subprocess  # Para ejecutar Manim en un proceso separado
from PIL import Image, ImageTk

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

tabla_visible = False  # Variable para mostrar/ocultar la tabla en el método de Bisección



import tempfile

import subprocess

# Función para guardar `funcion_str` en un archivo temporal
def guardar_funcion_temp(funcion):
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_file:
        temp_file.write(funcion)
        print(f"Archivo temporal creado: {temp_file.name}")  # Agregar esta línea
        return temp_file.name

# Modificar generar_gif_biseccion para mostrar la barra después de crear el GIF
def generar_gif_biseccion():
    funcion = funcion_input_biseccion.get("1.0", "end-1c").strip()
    if not funcion:
        messagebox.showerror("Error", "Por favor, ingresa una función válida.")
        return
    temp_file = guardar_funcion_temp(funcion)  # Guardar la función en un archivo temporal
    result = subprocess.run([
        "manim", "-pql", "animation.py", "BiseccionAnimation", "--format=gif", temp_file
    ])
    
    # Verificar si el GIF se generó correctamente
    if result.returncode == 0:
        crear_barra_extensible(tab_biseccion)  # Mostrar la barra en la pestaña de Bisección

# Modificar generar_gif_newton para mostrar la barra después de crear el GIF
def generar_gif_newton():
    funcion = funcion_input_newton.get("1.0", "end-1c").strip()
    if not funcion:
        messagebox.showerror("Error", "Por favor, ingresa una función válida.")
        return
    temp_file = guardar_funcion_temp(funcion)  # Guardar la función en un archivo temporal
    result = subprocess.run([
        "manim", "-pql", "animation.py", "NewtonRaphsonAnimation", "--format=gif", temp_file
    ])
    
    # Verificar si el GIF se generó correctamente
    if result.returncode == 0:
        crear_barra_extensible(tab_newton)  # Mostrar la barra en la pestaña de Newton-Raphson


# Función para ejecutar el método de Bisección desde la interfaz
def ejecutar_biseccion():
    try:
        funcion = funcion_input_biseccion.get("1.0", "end-1c")
        a = float(a_input.get())
        b = float(b_input.get())
        E = float(tol_input.get())
        max_iter = int(max_iter_input.get())
        
        funcion = biseccion_logic.procesar_funcion(funcion)
        f = lambda x: eval(funcion, {"x": x, "math": math})
        
        raiz, error, pasos, iteraciones = biseccion_logic.biseccion(f, a, b, E, max_iter)
        
        consola_biseccion.delete("1.0", "end")
        if raiz is not None:
            consola_biseccion.insert("1.0", f"El método converge a {iteraciones} iteraciones.\n", "bold")
            consola_biseccion.insert("end", f"La raíz es: {raiz} con un error relativo porcentual de: {error}%", "bold")
        
        global pasos_biseccion
        pasos_biseccion = pasos
    except ValueError as ve:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error de valor: {ve}")
    except Exception as e:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error inesperado: {e}")

def mostrar_ocultar_tabla():
    global tabla_visible
    if not tabla_visible:
        mostrar_pasos_biseccion()
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        btn_mostrar_tabla.config(text="Ocultar tabla de resultados")
        tabla_visible = True
    else:
        tree.pack_forget()
        btn_mostrar_tabla.config(text="Mostrar tabla de resultados")
        tabla_visible = False

def mostrar_pasos_biseccion():
    for row in tree.get_children():
        tree.delete(row)
    
    for paso in pasos_biseccion:
        iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
        tree.insert("", "end", values=(iteracion, xi, xu, xr, Ea, yi, yu, yr))

# Función para ejecutar el método de Newton-Raphson desde la interfaz
def ejecutar_newton_raphson():
    try:
        funcion_str = funcion_input_newton.get("1.0", "end-1c")
        x0 = float(valor_inicial_input.get())
        
        resultado = newton_raphson_logic.newton_raphson(funcion_str, x0)
        
        consola_newton.delete("1.0", "end")
        consola_newton.insert("1.0", f"{'Iteración':<10}{'x':<20}{'f(x)':<20}\n")
        consola_newton.insert("end", "-" * 50 + "\n")
        
        for iteracion in resultado["iteraciones"]:
            consola_newton.insert(
                "end",
                f"{iteracion['iteracion']:<10}{iteracion['x']:<20.10f}{iteracion['f(x)']:<20.10f}\n"
            )

        if resultado["convergencia"]:
            consola_newton.insert("end", f"\nConvergencia alcanzada.\nRaíz = {resultado['raiz']:.10f}")
        else:
            consola_newton.insert("end", "\nNo se encontró convergencia en el número máximo de iteraciones.")
    except ValueError as e:
        consola_newton.delete("1.0", "end")
        consola_newton.insert("1.0", str(e))

# Crear una función general para la barra extensible
def crear_barra_extensible(tab):
    # Crear un frame en el lado derecho de la pestaña
    barra_frame = ctk.CTkFrame(tab, width=200)
    barra_frame.pack(side="right", fill="y")
    
    # Etiqueta para indicar que el GIF se generó
    label_gif_generado = ctk.CTkLabel(barra_frame, text="GIF generado:", font=("Arial", 14, "bold"))
    label_gif_generado.pack(pady=10)
    
    # Agregar el contenido específico de la barra
    # Aquí puedes añadir más elementos, como botones, etiquetas, etc.
    # Ejemplo de un botón para ver el GIF generado
    btn_ver_gif = ctk.CTkButton(barra_frame, text="Ver GIF", command=lambda: messagebox.showinfo("GIF", "Aquí se mostraría el GIF"))
    btn_ver_gif.pack(pady=10)

    # Puedes retornar el frame para realizar modificaciones si es necesario
    return barra_frame

# Crear la interfaz para el método de Bisección
def crear_interfaz_biseccion(tabview):
    global funcion_input_biseccion, a_input, b_input, tol_input, max_iter_input, consola_biseccion, pasos_biseccion, tree, btn_mostrar_tabla
    global tab_biseccion
    tab_biseccion = tabview.add("Bisección")
    label_funcion = ctk.CTkLabel(tab_biseccion, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion.pack(pady=5)
    funcion_input_biseccion = ctk.CTkTextbox(tab_biseccion, height=50, font=("Arial", 12))
    funcion_input_biseccion.pack(pady=5, padx=20)

    label_a = ctk.CTkLabel(tab_biseccion, text="Límite inferior a:", font=("Arial", 14, "bold"))
    label_a.pack(pady=5)
    a_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    a_input.pack(pady=5)

    label_b = ctk.CTkLabel(tab_biseccion, text="Límite superior b:", font=("Arial", 14, "bold"))
    label_b.pack(pady=5)
    b_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    b_input.pack(pady=5)

    label_tol = ctk.CTkLabel(tab_biseccion, text="Tolerancia:", font=("Arial", 14, "bold"))
    label_tol.pack(pady=5)
    tol_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    tol_input.pack(pady=5)

    label_max_iter = ctk.CTkLabel(tab_biseccion, text="Número máximo de iteraciones:", font=("Arial", 14, "bold"))
    label_max_iter.pack(pady=5)
    max_iter_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    max_iter_input.pack(pady=5)

    btn_ejecutar_biseccion = ctk.CTkButton(tab_biseccion, text="Ejecutar Bisección", command=ejecutar_biseccion, font=("Arial", 12, "bold"))
    btn_ejecutar_biseccion.pack(pady=10)
    btn_animar_biseccion = ctk.CTkButton(tab_biseccion, text="Generar GIF Bisección", command=generar_gif_biseccion, font=("Arial", 12, "bold"))
    btn_animar_biseccion.pack(pady=10)


    consola_biseccion = Text(tab_biseccion, height=5, width=60, font=("Courier", 12))
    consola_biseccion.tag_configure("bold", font=("Courier", 12, "bold"))
    consola_biseccion.pack(pady=10, padx=20)

    btn_mostrar_tabla = ctk.CTkButton(tab_biseccion, text="Mostrar tabla de resultados", command=mostrar_ocultar_tabla, font=("Arial", 12, "bold"))
    btn_mostrar_tabla.pack(pady=10)

    tree = ttk.Treeview(tab_biseccion, columns=("Iteración", "xi", "xu", "xr", "Ea", "yi", "yu", "yr"), show="headings")
    tree.heading("Iteración", text="Iteración")
    tree.heading("xi", text="xi")
    tree.heading("xu", text="xu")
    tree.heading("xr", text="xr")
    tree.heading("Ea", text="Ea")
    tree.heading("yi", text="yi")
    tree.heading("yu", text="yu")
    tree.heading("yr", text="yr")

# Crear la interfaz para el método de Newton-Raphson
def crear_interfaz_newton(tabview):
    global funcion_input_newton, valor_inicial_input, consola_newton
    global tab_newton
    tab_newton = tabview.add("Newton-Raphson")
    label_funcion = ctk.CTkLabel(tab_newton, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion.pack(pady=5)
    funcion_input_newton = ctk.CTkTextbox(tab_newton, height=50, font=("Arial", 12))
    funcion_input_newton.pack(pady=5, padx=20)

    label_valor_inicial = ctk.CTkLabel(tab_newton, text="Valor inicial x0:", font=("Arial", 14, "bold"))
    label_valor_inicial.pack(pady=5)
    valor_inicial_input = ctk.CTkEntry(tab_newton, font=("Arial", 12))
    valor_inicial_input.pack(pady=5)

    btn_ejecutar_newton = ctk.CTkButton(tab_newton, text="Calcular Raíz", command=ejecutar_newton_raphson, font=("Arial", 12, "bold"))
    btn_ejecutar_newton.pack(pady=10)
    btn_animar_newton = ctk.CTkButton(tab_newton, text="Generar GIF Newton-Raphson", command=generar_gif_newton, font=("Arial", 12, "bold"))
    btn_animar_newton.pack(pady=10)



    consola_newton = Text(tab_newton, height=15, width=60, font=("Courier", 12))
    consola_newton.pack(pady=10, padx=20)

# Función para crear la interfaz de la calculadora estilo GeoGebra


def crear_interfaz_introductoria(tabview):
    # Crear una nueva pestaña para la introducción
    tab_intro = tabview.add("Introducción")

    # Cargar y mostrar la imagen de bienvenida
    try:
        imagen = Image.open("noelle.png")  # Cambia 'bienvenida.png' por el nombre de tu imagen
        imagen = imagen.resize((300, 200))
        imagen = ImageTk.PhotoImage(imagen)
        label_imagen = ctk.CTkLabel(tab_intro, image=imagen)
        label_imagen.image = imagen  # Mantener referencia para que no se borre de memoria
        label_imagen.pack(pady=10)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    # Título de bienvenida
    label_titulo = ctk.CTkLabel(tab_intro, text="Bienvenido a Numway ", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=10)

    # Texto de instrucciones
    instrucciones = (
        "Esta aplicación ofrece varias herramientas numéricas para ayudar con el cálculo y visualización de funciones:\n\n"
        "1. **Calculadora Estilo GeoGebra**: Realiza cálculos matemáticos avanzados incluyendo funciones trigonométricas.\n"
        "2. **Método de Bisección**: Calcula raíces de funciones en intervalos específicos.\n"
        "3. **Método de Newton-Raphson**: Encuentra raíces de funciones usando aproximaciones sucesivas.\n"
        "4. **Graficador de Funciones**: Genera gráficos para visualizar cualquier función matemática en un rango especificado.\n\n"
        "Para empezar, selecciona una de las pestañas en la parte superior."
    )
    label_instrucciones = ctk.CTkLabel(tab_intro, text=instrucciones, font=("Arial", 12), justify="left", wraplength=400)
    label_instrucciones.pack(pady=20, padx=20)


# Función para actualizar la vista previa de la expresión en formato agradable
def actualizar_preview():
    global entry_text, preview_label
    try:
        # Crear una copia de entry_text para aplicar las transformaciones necesarias
        expression_to_evaluate = entry_text.replace("^", "**")
        expression_to_evaluate = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expression_to_evaluate)

        # Convertir la expresión a SymPy y luego a LaTeX
        x = symbols("x")
        sympy_expr = sympify(expression_to_evaluate)
        latex_expr = latex(sympy_expr)

        # Crear una imagen de la expresión en formato LaTeX
        buf = io.BytesIO()
        plt.figure(figsize=(4, 1))
        plt.text(0.5, 0.5, f"${latex_expr}$", size=20, ha="center", va="center")
        plt.axis("off")
        plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
        buf.seek(0)

        # Cargar la imagen en Tkinter
        img = Image.open(buf)
        img_tk = ImageTk.PhotoImage(img)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk  # Mantener referencia de la imagen para evitar garbage collection
    except Exception as e:
        preview_label.config(text="Error en la expresión")

# Función para evaluar la expresión en la entrada
def evaluate_expression():
    global entry_text
    try:
        # Evaluar la expresión, con transformaciones para interpretarla correctamente
        expression_to_evaluate = entry_text.replace("^", "**")
        expression_to_evaluate = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expression_to_evaluate)

        # Evaluar la expresión
        result = eval(expression_to_evaluate, {"__builtins__": None}, {
            "sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e
        })

        # Mostrar el resultado en la entrada
        entry.delete(0, ctk.END)
        entry.insert(0, str(result))
        entry_text = str(result)
    except Exception:
        entry.delete(0, ctk.END)
        entry.insert(0, "Error")
        entry_text = ""


def crear_interfaz_calculadora(tabview):
    global entry, entry_text, calculadora_frame

    # Crear pestaña para la calculadora en el tabview
    tab_calculadora = tabview.add("Calculadora")

    # Frame para centrar la calculadora dentro de la pestaña
    calculadora_frame = ctk.CTkFrame(tab_calculadora)
    calculadora_frame.pack(expand=True)  # Centrar el frame en la pestaña

    # Inicializar variable de entrada
    entry_text = ""

    # Campo de entrada
    entry = ctk.CTkEntry(calculadora_frame, width=300, font=("Arial", 20))
    entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)


    # Función para insertar texto en la entrada
        # def insert_text(text):
        #     global entry_text
        #     entry_text += text
        #     entry.delete(0, ctk.END)
        #     entry.insert(0, entry_text)

    def insert_text(text):
        global entry_text
        cursor_position = entry.index(ctk.INSERT)  # Obtener la posición actual del cursor
        entry.insert(cursor_position, text)        # Insertar texto en esa posición
        entry_text = entry.get() 

    # # Función para evaluar la expresión en la entrada
    # def evaluate_expression():
    #     global entry_text
    #     try:
    #         # Crear una copia de entry_text para evaluar, realizando los reemplazos necesarios
    #         expression_to_evaluate = entry_text

    #         # Reemplazar ^ con ** para la potencia
    #         expression_to_evaluate = expression_to_evaluate.replace("^", "**")
            
    #         # Insertar * entre un número y una variable o función (por ejemplo, 2x -> 2*x)
    #         expression_to_evaluate = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expression_to_evaluate)
            
    #         # Evaluar la expresión
    #         result = eval(expression_to_evaluate, {"__builtins__": None}, {
    #             "sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e
    #         })

    #         # Mostrar el resultado en la entrada
    #         entry.delete(0, ctk.END)
    #         entry.insert(0, str(result))
    #         entry_text = str(result)
    #     except Exception:
    #         # Mostrar error si la evaluación falla
    #         entry.delete(0, ctk.END)
    #         entry.insert(0, "Error")
    #         entry_text = ""


    # Función para borrar la entrada
    def clear_entry():
        global entry_text
        entry_text = ""
        entry.delete(0, ctk.END)
    
       # Actualizar preview en tiempo real al escribir en el campo de entrada
    def actualizar_texto(event):
        global entry_text
        entry_text = entry.get()
        actualizar_preview()

    entry.bind("<KeyRelease>", actualizar_texto)  # Actualizar preview en cada pulsación de tecla
 

    # Botones numéricos, operaciones y funciones
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '(', ')'),
        ('+', 'sin', 'cos', 'tan'),
        ('pi', 'e', '^', 'sqrt'),
        ('x', 'y', 'z', 'clear'),  # Nueva fila con las variables y el botón de limpiar
        ('C', '=', 'log', 'clear')
    ]

    # Crear botones en la interfaz
    for i, row in enumerate(buttons):
        for j, btn_text in enumerate(row):
            # Asignar función a cada botón
            if btn_text == 'C':
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=clear_entry)
            elif btn_text == '=':
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=evaluate_expression)
            elif btn_text == 'clear':
                button = ctk.CTkButton(calculadora_frame, text="Clear", width=60, command=clear_entry)
            else:
                # Autocompletar para funciones trigonométricas y logarítmicas
                if btn_text in ('sin', 'cos', 'tan', 'log', 'sqrt'):
                    command = lambda t=btn_text: insert_text(f"{t}(")
                else:
                    command = lambda t=btn_text: insert_text(t)
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=command)
            button.grid(row=i+1, column=j, padx=5, pady=5)

    # Función para crear la interfaz de graficador
    # Función para añadir un nuevo input para una nueva función
def añadir_funcion():
    nueva_funcion_input = ctk.CTkEntry(tab_graficador, font=("Arial", 12), width=200)
    nueva_funcion_input.pack(pady=5)
    funcion_inputs.append(nueva_funcion_input)


def crear_interfaz_graficador(tabview):
    global tab_graficador, funcion_inputs, funciones_frame

    # Crear pestaña para el graficador en el tabview
    tab_graficador = tabview.add("Graficador")

    # Inicializar lista de inputs de funciones
    funcion_inputs = []

    # Frame para contener los inputs de funciones
    funciones_frame = ctk.CTkFrame(tab_graficador)
    funciones_frame.pack(pady=5)

    # Etiqueta y primer entrada para la función
    label_funcion = ctk.CTkLabel(funciones_frame, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion.pack(pady=5)
    funcion_input = ctk.CTkEntry(funciones_frame, font=("Arial", 12), width=200)
    funcion_input.pack(pady=5)
    funcion_inputs.append(funcion_input)

    # Contenedor para los rangos de x y y
    rango_frame = ctk.CTkFrame(tab_graficador)
    rango_frame.pack(pady=5)

    # Etiqueta y entrada para el rango mínimo y máximo de x
    label_x_min = ctk.CTkLabel(rango_frame, text="Rango mínimo (x_min):", font=("Arial", 14, "bold"))
    label_x_min.grid(row=0, column=0, padx=5)
    x_min_input = ctk.CTkEntry(rango_frame, font=("Arial", 12), width=100)
    x_min_input.grid(row=0, column=1, padx=5)

    label_x_max = ctk.CTkLabel(rango_frame, text="Rango máximo (x_max):", font=("Arial", 14, "bold"))
    label_x_max.grid(row=0, column=2, padx=5)
    x_max_input = ctk.CTkEntry(rango_frame, font=("Arial", 12), width=100)
    x_max_input.grid(row=0, column=3, padx=5)

    # Contenedor para los rangos de y
    rango_frame_y = ctk.CTkFrame(tab_graficador)
    rango_frame_y.pack(pady=5)

    label_y_min = ctk.CTkLabel(rango_frame_y, text="Rango mínimo (y_min):", font=("Arial", 14, "bold"))
    label_y_min.grid(row=0, column=0, padx=5)
    y_min_input = ctk.CTkEntry(rango_frame_y, font=("Arial", 12), width=100)
    y_min_input.grid(row=0, column=1, padx=5)

    label_y_max = ctk.CTkLabel(rango_frame_y, text="Rango máximo (y_max):", font=("Arial", 14, "bold"))
    label_y_max.grid(row=0, column=2, padx=5)
    y_max_input = ctk.CTkEntry(rango_frame_y, font=("Arial", 12), width=100)
    y_max_input.grid(row=0, column=3, padx=5)

    # Función para añadir un nuevo input de función
    def añadir_funcion():
        nueva_funcion_input = ctk.CTkEntry(funciones_frame, font=("Arial", 12), width=200)
        nueva_funcion_input.pack(pady=5)  # Añade el nuevo input debajo del original
        funcion_inputs.append(nueva_funcion_input)  # Añade a la lista de inputs

    # Función para procesar la función ingresada y graficarla
    def graficar():
        try:
            funciones = [funcion_input.get() for funcion_input in funcion_inputs]
            x_min = float(x_min_input.get()) if x_min_input.get() else -10
            x_max = float(x_max_input.get()) if x_max_input.get() else 10
            y_min = float(y_min_input.get()) if y_min_input.get() else -10
            y_max = float(y_max_input.get()) if y_max_input.get() else 10

            # Definir las funciones evaluables
            def crear_funcion(funcion_str):
                return lambda x: eval(funcion_str, {"x": x, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e})

            funciones_evaluables = [crear_funcion(funcion_str) for funcion_str in funciones]
            titulo = "F(x) = " + ", ".join(funciones)

            # Llamar al módulo graficador para graficar múltiples funciones
            graficar_funcion(funciones_evaluables, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, titulo=titulo)

        except Exception as e:
            print(f"Error al graficar: {e}")

    # Botón para graficar
    btn_graficar = ctk.CTkButton(tab_graficador, text="Graficar", command=graficar, font=("Arial", 12, "bold"))
    btn_graficar.pack(pady=10)

    # Botón para añadir una nueva función
    btn_añadir_funcion = ctk.CTkButton(tab_graficador, text="Añadir Función", command=añadir_funcion, font=("Arial", 12, "bold"))
    btn_añadir_funcion.pack(pady=10)

def main():
    root = ctk.CTk()
    root.title("NUMWAY")
    root.geometry("1000x600")

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    crear_interfaz_introductoria(tabview)
    crear_interfaz_calculadora(tabview)
    crear_interfaz_biseccion(tabview)
    crear_interfaz_newton(tabview)
    crear_interfaz_graficador(tabview)

    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
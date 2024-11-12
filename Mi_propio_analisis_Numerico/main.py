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

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

tabla_visible = False  # Variable para mostrar/ocultar la tabla en el método de Bisección




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

# Crear la interfaz para el método de Bisección
def crear_interfaz_biseccion(tabview):
    global funcion_input_biseccion, a_input, b_input, tol_input, max_iter_input, consola_biseccion, pasos_biseccion, tree, btn_mostrar_tabla

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

    consola_newton = Text(tab_newton, height=15, width=60, font=("Courier", 12))
    consola_newton.pack(pady=10, padx=20)

# Función para crear la interfaz de la calculadora estilo GeoGebra



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
    def insert_text(text):
        global entry_text
        entry_text += text
        entry.delete(0, ctk.END)
        entry.insert(0, entry_text)

    # Función para evaluar la expresión en la entrada
    def evaluate_expression():
        global entry_text
        try:
            entry_text = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', entry_text)
            result = eval(entry_text, {"__builtins__": None}, {"sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e})
            entry.delete(0, ctk.END)
            entry.insert(0, str(result))
            entry_text = str(result)
        except Exception as e:
            entry.delete(0, ctk.END)
            entry.insert(0, "Error")
            entry_text = ""

    # Función para borrar la entrada
    def clear_entry():
        global entry_text
        entry_text = ""
        entry.delete(0, ctk.END)

    # Botones numéricos, operaciones y funciones
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '(', ')'),
        ('+', 'sin', 'cos', 'tan'),
        ('pi', 'e', '^', 'sqrt'),
        ('C', '=', 'log', 'clear')
    ]

    # Crear botones en la interfaz
    for i, row in enumerate(buttons):
        for j, btn_text in enumerate(row):
            if btn_text == 'C':
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=clear_entry)
            elif btn_text == '=':
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=evaluate_expression)
            elif btn_text == 'clear':
                button = ctk.CTkButton(calculadora_frame, text="Clear", width=60, command=clear_entry)
            else:
                button = ctk.CTkButton(calculadora_frame, text=btn_text, width=60, command=lambda t=btn_text: insert_text(t))
            button.grid(row=i+1, column=j, padx=5, pady=5)

# Función para crear la interfaz de graficador
def crear_interfaz_graficador(tabview):
    # Crear pestaña para el graficador en el tabview
    tab_graficador = tabview.add("Graficador")

    # Etiqueta y entrada para la función
    label_funcion = ctk.CTkLabel(tab_graficador, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion.pack(pady=5)
    funcion_input = ctk.CTkEntry(tab_graficador, font=("Arial", 12), width=200)
    funcion_input.pack(pady=5)
    # Contenedor para los rangos de x
    rango_frame = ctk.CTkFrame(tab_graficador)
    rango_frame.pack(pady=5)

    # Etiqueta y entrada para el rango mínimo de x
    label_x_min = ctk.CTkLabel(rango_frame, text="Rango mínimo (x_min):", font=("Arial", 14, "bold"))
    label_x_min.grid(row=0, column=0, padx=5)
    x_min_input = ctk.CTkEntry(rango_frame, font=("Arial", 12), width=100)
    x_min_input.grid(row=0, column=1, padx=5)

    # Etiqueta y entrada para el rango máximo de x
    label_x_max = ctk.CTkLabel(rango_frame, text="Rango máximo (x_max):", font=("Arial", 14, "bold"))
    label_x_max.grid(row=0, column=2, padx=5)
    x_max_input = ctk.CTkEntry(rango_frame, font=("Arial", 12), width=100)
    x_max_input.grid(row=0, column=3, padx=5)
    # Contenedor para los rangos de y
    rango_frame_y = ctk.CTkFrame(tab_graficador)
    rango_frame_y.pack(pady=5)

    # Etiqueta y entrada para el rango mínimo de y
    label_y_min = ctk.CTkLabel(rango_frame_y, text="Rango mínimo (y_min):", font=("Arial", 14, "bold"))
    label_y_min.grid(row=0, column=0, padx=5)
    y_min_input = ctk.CTkEntry(rango_frame_y, font=("Arial", 12), width=100)
    y_min_input.grid(row=0, column=1, padx=5)

    # Etiqueta y entrada para el rango máximo de y
    label_y_max = ctk.CTkLabel(rango_frame_y, text="Rango máximo (y_max):", font=("Arial", 14, "bold"))
    label_y_max.grid(row=0, column=2, padx=5)
    y_max_input = ctk.CTkEntry(rango_frame_y, font=("Arial", 12), width=100)
    y_max_input.grid(row=0, column=3, padx=5)


    # Función para procesar la función ingresada y graficarla
    def graficar():
        try:
            # Obtener y procesar los valores ingresados
            funcion_str = funcion_input.get()

            if(x_min_input.get() != ''):
                 x_min = float(y_min_input.get()) 
            else: x_min = -10
            if(x_max_input.get() != ''):
                 x_max = float(y_max_input.get()) 
            else: x_max = 10
            if(y_min_input.get() != ''):
                 y_min = float(y_min_input.get()) 
            else: y_min = -10
            if(y_max_input.get() != ''):
                 y_max = float(y_max_input.get()) 
            else: y_max = 10

            # Definir la función evaluable
            def funcion(x):
                return eval(funcion_str, {"x": x, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e})

            # Llamar al módulo graficador
            graficar_funcion(funcion, x_min=x_min, x_max=x_max,y_min= y_min, y_max= y_max, titulo=f"Gráfica de f(x) = {funcion_str}")

        except Exception as e:
            print(f"Error al graficar: {e}")

    # Botón para graficar
    btn_graficar = ctk.CTkButton(tab_graficador, text="Graficar", command=graficar, font=("Arial", 12, "bold"))
    btn_graficar.pack(pady=10)
# Crear la ventana principal y el menú de pestañas
def main():
    root = ctk.CTk()
    root.title("Métodos Numéricos")
    root.geometry("1000x600")

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)

    crear_interfaz_biseccion(tabview)
    crear_interfaz_newton(tabview)
    crear_interfaz_calculadora(tabview)
    crear_interfaz_graficador(tabview)

    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()

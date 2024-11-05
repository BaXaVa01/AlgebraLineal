import customtkinter as ctk
from tkinter import ttk, Text
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para ejecutar el método de bisección desde la interfaz
def ejecutar_biseccion():
    try:
        # Obtener los valores de los campos de entrada
        funcion = funcion_input.get("1.0", "end-1c")
        a = float(a_input.get())
        b = float(b_input.get())
        E = float(tol_input.get())
        max_iter = int(max_iter_input.get())
        
        # Definir la función a partir de la cadena ingresada
        f = lambda x: eval(funcion)
        
        # Ejecutar el método de bisección
        raiz, error, pasos, iteraciones = biseccion(f, a, b, E, max_iter)
        
        # Mostrar el resultado en la consola
        consola_biseccion.delete("1.0", "end")
        if raiz is not None:
            consola_biseccion.insert("1.0", f"El método converge a {iteraciones} iteraciones.\n", "bold")
            consola_biseccion.insert("end", f"La raíz es: {raiz} con un error relativo porcentual de: {error}%", "bold")
        
        # Guardar los pasos en una variable global para mostrarlos después
        global pasos_biseccion
        pasos_biseccion = pasos

        # Mostrar los pasos en la tabla
        mostrar_pasos_biseccion()
    except ValueError as ve:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error de valor: {ve}")
    except TypeError as te:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error de tipo: {te}")
    except Exception as e:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error inesperado: {e}")

def mostrar_pasos_biseccion():
    # Limpiar la tabla antes de insertar nuevos datos
    for row in tree.get_children():
        tree.delete(row)
    
    # Insertar los pasos en la tabla
    for paso in pasos_biseccion:
        iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
        tree.insert("", "end", values=(iteracion, xi, xu, xr, Ea, yi, yu, yr))

# Función de bisección
def biseccion(f, a, b, E=1e-5, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.
    
    :param f: Función para la cual se busca la raíz.
    :param a: Límite inferior del intervalo.
    :param b: Límite superior del intervalo.
    :param E: Precisión requerida.
    :param max_iter: Número máximo de iteraciones.
    :return: Aproximación de la raíz, el error relativo porcentual, los pasos de cada iteración y el número de iteraciones.
    """
    try:
        if f(a) * f(b) >= 0:
            raise ValueError("La función debe tener signos opuestos en los extremos del intervalo [a, b].")
        
        iter_count = 0
        c = (a + b) / 2.0
        prev_c = c
        error_relativo = float('inf')
        pasos = []
        
        while (b - a) / 2.0 > E and iter_count < max_iter:
            c = (a + b) / 2.0
            yi = f(a)
            yu = f(b)
            yr = f(c)
            if iter_count > 0:
                error_relativo = abs((c - prev_c) / c) * 100
            else:
                error_relativo = float('inf')
            pasos.append(f"{iter_count + 1}, {a}, {b}, {c}, {error_relativo}, {yi}, {yu}, {yr}")
            if f(c) == 0:
                return c, 0, pasos, iter_count + 1  # La raíz exacta ha sido encontrada
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
            
            prev_c = c
            iter_count += 1
        
        return c, error_relativo, pasos, iter_count
    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except TypeError as te:
        print(f"Error de tipo: {te}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Crear la interfaz para el método de bisección
def crear_interfaz_biseccion(tabview):
    global funcion_input, a_input, b_input, tol_input, max_iter_input, consola_biseccion, pasos_biseccion, tree

    # Crear pestaña para el método de bisección
    tab_biseccion = tabview.add("Bisección")

    # Etiqueta y entrada para la función
    label_funcion = ctk.CTkLabel(tab_biseccion, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion.pack(pady=5)
    funcion_input = ctk.CTkTextbox(tab_biseccion, height=50, font=("Arial", 12))
    funcion_input.pack(pady=5, padx=20)

    # Etiqueta y entrada para el límite inferior a
    label_a = ctk.CTkLabel(tab_biseccion, text="Límite inferior a:", font=("Arial", 14, "bold"))
    label_a.pack(pady=5)
    a_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    a_input.pack(pady=5)

    # Etiqueta y entrada para el límite superior b
    label_b = ctk.CTkLabel(tab_biseccion, text="Límite superior b:", font=("Arial", 14, "bold"))
    label_b.pack(pady=5)
    b_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    b_input.pack(pady=5)

    # Etiqueta y entrada para la tolerancia
    label_tol = ctk.CTkLabel(tab_biseccion, text="Tolerancia:", font=("Arial", 14, "bold"))
    label_tol.pack(pady=5)
    tol_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    tol_input.pack(pady=5)

    # Etiqueta y entrada para el número máximo de iteraciones
    label_max_iter = ctk.CTkLabel(tab_biseccion, text="Número máximo de iteraciones:", font=("Arial", 14, "bold"))
    label_max_iter.pack(pady=5)
    max_iter_input = ctk.CTkEntry(tab_biseccion, font=("Arial", 12))
    max_iter_input.pack(pady=5)

    # Botón para ejecutar el método de bisección
    btn_ejecutar_biseccion = ctk.CTkButton(tab_biseccion, text="Ejecutar Bisección", command=ejecutar_biseccion, font=("Arial", 12, "bold"))
    btn_ejecutar_biseccion.pack(pady=10)

    # Consola para mostrar los resultados
    consola_biseccion = Text(tab_biseccion, height=5, width=60, font=("Courier", 12))
    consola_biseccion.tag_configure("bold", font=("Courier", 12, "bold"))
    consola_biseccion.pack(pady=10, padx=20)

    # Crear la tabla para mostrar los pasos
    tree = ttk.Treeview(tab_biseccion, columns=("Iteración", "xi", "xu", "xr", "Ea", "yi", "yu", "yr"), show="headings")
    tree.heading("Iteración", text="Iteración")
    tree.heading("xi", text="xi")
    tree.heading("xu", text="xu")
    tree.heading("xr", text="xr")
    tree.heading("Ea", text="Ea")
    tree.heading("yi", text="yi")
    tree.heading("yu", text="yu")
    tree.heading("yr", text="yr")
    tree.pack(pady=10, padx=20, fill="both", expand=True)

# Crear la interfaz para graficar la función
def crear_interfaz_grafica(tabview):
    global funcion_input_grafica, a_input_grafica, b_input_grafica, fig, ax, canvas

    # Crear pestaña para la gráfica
    tab_grafica = tabview.add("Gráfica")

    # Etiqueta y entrada para la función
    label_funcion_grafica = ctk.CTkLabel(tab_grafica, text="Función f(x):", font=("Arial", 14, "bold"))
    label_funcion_grafica.pack(pady=5)
    funcion_input_grafica = ctk.CTkTextbox(tab_grafica, height=50, font=("Arial", 12))
    funcion_input_grafica.pack(pady=5, padx=20)

    # Etiqueta y entrada para el límite inferior a
    label_a_grafica = ctk.CTkLabel(tab_grafica, text="Límite inferior a:", font=("Arial", 14, "bold"))
    label_a_grafica.pack(pady=5)
    a_input_grafica = ctk.CTkEntry(tab_grafica, font=("Arial", 12))
    a_input_grafica.pack(pady=5)

    # Etiqueta y entrada para el límite superior b
    label_b_grafica = ctk.CTkLabel(tab_grafica, text="Límite superior b:", font=("Arial", 14, "bold"))
    label_b_grafica.pack(pady=5)
    b_input_grafica = ctk.CTkEntry(tab_grafica, font=("Arial", 12))
    b_input_grafica.pack(pady=5)

    # Botón para graficar la función
    btn_graficar = ctk.CTkButton(tab_grafica, text="Graficar", command=graficar_funcion, font=("Arial", 12, "bold"))
    btn_graficar.pack(pady=10)

    # Crear el canvas para la gráfica
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=tab_grafica)
    canvas.get_tk_widget().pack(pady=10, padx=20, fill="both", expand=True)

def graficar_funcion():
    # Obtener los valores de los campos de entrada
    funcion = funcion_input_grafica.get("1.0", "end-1c")
    a = float(a_input_grafica.get())
    b = float(b_input_grafica.get())

    # Definir la función a partir de la cadena ingresada
    f = lambda x: eval(funcion)

    # Generar los valores de x e y para la gráfica
    x = [i for i in range(int(a), int(b) + 1)]
    y = [f(i) for i in x]

    # Limpiar la gráfica anterior
    ax.clear()

    # Graficar la función
    ax.plot(x, y, label=f"f(x) = {funcion}")
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    ax.legend()

    # Actualizar el canvas
    canvas.draw()

# Función para crear todas las interfaces
def crear_interfaz(tabview):
    crear_interfaz_biseccion(tabview)
    crear_interfaz_grafica(tabview)

# Ejecutar la función principal
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Calculadora y Bisección")
    root.geometry("1000x600")

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)

    crear_interfaz(tabview)

    root.mainloop()
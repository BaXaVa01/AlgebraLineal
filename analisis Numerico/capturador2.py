import customtkinter as ctk
from tkinter import ttk, Text
import math  # Importamos math para usar funciones matemáticas de forma segura.

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Variable para mostrar/ocultar la tabla
tabla_visible = False

# Función para procesar la expresión del usuario
def procesar_funcion(funcion):
    funcion = funcion.replace("^", "**")
    funciones_permitidas = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp']
    for fn in funciones_permitidas:
        funcion = funcion.replace(f"{fn}(", f"math.{fn}(")

    # Agregar un reemplazo para ln (logaritmo natural)
    funcion = funcion.replace("ln(", "math.log(")  # Reemplazo para ln

    return funcion


# Función para ejecutar el método de bisección desde la interfaz
def ejecutar_biseccion():
    try:
        # Obtener los valores de los campos de entrada
        funcion = funcion_input.get("1.0", "end-1c")
        a = float(a_input.get())
        b = float(b_input.get())
        E = float(tol_input.get())
        max_iter = int(max_iter_input.get())
        
        # Procesar y definir la función de la expresión ingresada
        funcion = procesar_funcion(funcion)
        f = lambda x: eval(funcion, {"x": x, "math": math})
        
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
    except ValueError as ve:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error de valor: {ve}")
    except TypeError as te:
        consola_biseccion.delete("1.0", "end")
        consola_biseccion.insert("1.0", f"Error de tipo: {te}")
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
    # Limpiar la tabla antes de insertar nuevos datos
    for row in tree.get_children():
        tree.delete(row)
    
    # Insertar los pasos en la tabla
    for paso in pasos_biseccion:
        iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
        tree.insert("", "end", values=(iteracion, xi, xu, xr, Ea, yi, yu, yr))

# Función de bisección
def biseccion(f, a, b, E=1e-5, max_iter=100):
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
    global funcion_input, a_input, b_input, tol_input, max_iter_input, consola_biseccion, pasos_biseccion, tree, btn_mostrar_tabla

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

    # Botón para mostrar/ocultar la tabla de resultados
    btn_mostrar_tabla = ctk.CTkButton(tab_biseccion, text="Mostrar tabla de resultados", command=mostrar_ocultar_tabla, font=("Arial", 12, "bold"))
    btn_mostrar_tabla.pack(pady=10)

    # Crear la tabla (inicialmente oculta)
    tree = ttk.Treeview(tab_biseccion, columns=("Iteración", "xi", "xu", "xr", "Ea", "yi", "yu", "yr"), show="headings")
    tree.heading("Iteración", text="Iteración")
    tree.heading("xi", text="xi")
    tree.heading("xu", text="xu")
    tree.heading("xr", text="xr")
    tree.heading("Ea", text="Ea")
    tree.heading("yi", text="yi")
    tree.heading("yu", text="yu")
    tree.heading("yr", text="yr")

    # Estilo para mejorar la apariencia de la tabla
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="lightblue")
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.map("Treeview", background=[("selected", "lightgreen")])


# Crear la interfaz para la calculadora
def crear_interfaz_calculadora(tabview):
    global entry, button_frame, side_frame, mode, toggle_button

    # Crear pestaña para la calculadora
    tab_calculadora = tabview.add("Calculadora")

    # Frame lateral para los botones de cambio de modo y limpiar
    side_frame = ctk.CTkFrame(tab_calculadora)
    side_frame.grid(row=0, column=0, padx=10)

    # Frame para los botones numéricos y de funciones
    button_frame = ctk.CTkFrame(tab_calculadora)
    button_frame.grid(row=0, column=1, padx=10)

    # Variable para alternar entre modos
    mode = "Funciones"

    # Función para insertar texto en el campo de entrada
    def insert_text(text, latexFormat):
        entry.configure(state='normal')
        entry.insert(ctk.END, text)
        entry.configure(state='readonly')

    # Función para alternar entre modos
    def toggle_mode():
        global mode
        mode = "Numérico" if mode == "Funciones" else "Funciones"
        toggle_button.configure(text=f"Cambiar a {mode}")
        update_buttons()

    # Actualizar botones según el modo seleccionado
    def update_buttons():
        # Limpiar botones existentes
        for widget in button_frame.winfo_children():
            widget.destroy()
        
        if mode == "Funciones":
            # Botones de operadores básicos
            btn_add = ctk.CTkButton(button_frame, text="+", command=lambda: insert_text("+", "\\text{sum}"), width=60)
            btn_subtract = ctk.CTkButton(button_frame, text="-", command=lambda: insert_text("-", "\\text{subtract}"), width=60)
            btn_multiply = ctk.CTkButton(button_frame, text="*", command=lambda: insert_text("*", "\\text{multiply}"), width=60)
            btn_divide = ctk.CTkButton(button_frame, text="/", command=lambda: insert_text("/", "\\text{divide}"), width=60)

            btn_add.grid(row=0, column=0, padx=5, pady=5)
            btn_subtract.grid(row=0, column=1, padx=5, pady=5)
            btn_multiply.grid(row=0, column=2, padx=5, pady=5)
            btn_divide.grid(row=0, column=3, padx=5, pady=5)

            # Botones de funciones avanzadas
            btn_sqrt = ctk.CTkButton(button_frame, text="√", command=lambda: insert_text("√(", "\\sqrt{}"), width=60)
            btn_pow = ctk.CTkButton(button_frame, text="^", command=lambda: insert_text("^", "^{}"), width=60)
            btn_frac = ctk.CTkButton(button_frame, text="a/b", command=lambda: insert_text("/", "\\frac{}{}"), width=60)
            btn_parentheses = ctk.CTkButton(button_frame, text="(", command=lambda: insert_text("(", "\\left("), width=60)
            btn_parentheses_right = ctk.CTkButton(button_frame, text=")", command=lambda: insert_text(")", "\\right)"), width=60)

            btn_sqrt.grid(row=1, column=0, padx=5, pady=5)
            btn_pow.grid(row=1, column=1, padx=5, pady=5)
            btn_frac.grid(row=1, column=2, padx=5, pady=5)
            btn_parentheses.grid(row=1, column=3, padx=5, pady=5)
            btn_parentheses_right.grid(row=1, column=4, padx=5, pady=5)

            # Botones de funciones trigonométricas
            btn_sin = ctk.CTkButton(button_frame, text="sin", command=lambda: insert_text("sin(", "\\sin{}"), width=60)
            btn_cos = ctk.CTkButton(button_frame, text="cos", command=lambda: insert_text("cos(", "\\cos{}"), width=60)
            btn_tan = ctk.CTkButton(button_frame, text="tan", command=lambda: insert_text("tan(", "\\tan{}"), width=60)
            btn_log = ctk.CTkButton(button_frame, text="log", command=lambda: insert_text("log(", "\\log{}"), width=60)

            btn_sin.grid(row=2, column=0, padx=5, pady=5)
            btn_cos.grid(row=2, column=1, padx=5, pady=5)
            btn_tan.grid(row=2, column=2, padx=5, pady=5)
            btn_log.grid(row=2, column=3, padx=5, pady=5)

        else:
            # Botones numéricos y de operadores básicos
            buttons = [
                ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
                ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
                ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
                ('0', 4, 1), ('.', 4, 0), ('=', 4, 2),
                ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3)
            ]

            for (text, row, col) in buttons:
                ctk.CTkButton(button_frame, text=text, command=lambda t=text: insert_text(t, t), width=60).grid(row=row, column=col, padx=5, pady=5)

    # Botón para alternar entre modos en el frame lateral
    toggle_button = ctk.CTkButton(side_frame, text="Cambiar a Numérico", command=toggle_mode, width=100)
    toggle_button.pack(pady=10)

    # Botón de limpiar entrada en el frame lateral
    btn_clear = ctk.CTkButton(side_frame, text="Limpiar", command=lambda: entry.delete(0, "end"), width=100)
    btn_clear.pack(pady=10)

    # Campo de entrada
    entry = ctk.CTkEntry(tab_calculadora, width=400, font=("Arial", 14))
    entry.grid(row=1, column=0, columnspan=2, pady=10)

    # Inicializar los botones en el modo "Funciones"
    update_buttons()

# Crear la ventana principal y el menú de pestañas
def main():
    # Crear ventana principal
    root = ctk.CTk()
    root.title("Calculadora y Bisección")
    root.geometry("1000x600")

    # Crear frame principal
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el menú de pestañas
    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear la interfaz para la calculadora en una pestaña separada
    crear_interfaz_calculadora(tabview)

    # Crear la interfaz para el método de bisección en una pestaña separada
    crear_interfaz_biseccion(tabview)

    # Iniciar la aplicación
    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
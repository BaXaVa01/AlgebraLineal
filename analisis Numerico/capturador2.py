import customtkinter as ctk
from calculadora import mostrar_calculadora  # Importa la función para mostrar la calculadora

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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
        
        # Frame para mostrar el gráfico Matplotlib
        self.plot_frame = ctk.CTkFrame(self, width=780, height=500)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Mostrar el resultado en la consola
        consola_biseccion.delete("1.0", "end")
        if raiz is not None:
            consola_biseccion.insert("1.0", f"El método converge a {iteraciones} iteraciones.\n")
            consola_biseccion.insert("end", f"La raíz es: {raiz} con un error relativo porcentual de: {error}%")
        
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

def mostrar_pasos_biseccion():
    consola_pasos_biseccion.delete("1.0", "end")
    for paso in pasos_biseccion:
        consola_pasos_biseccion.insert("end", paso + "\n")

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
            pasos.append(f"Iteración {iter_count + 1}: a = {a}, b = {b}, c = {c}, f(c) = {f(c)}")
            if f(c) == 0:
                return c, 0, pasos, iter_count + 1  # La raíz exacta ha sido encontrada
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
            
            # Calcular el error relativo porcentual
            if iter_count > 0:
                error_relativo = abs((c - prev_c) / c) * 100
            
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
    global funcion_input, a_input, b_input, tol_input, max_iter_input, consola_biseccion, consola_pasos_biseccion, pasos_biseccion

    # Crear pestaña para el método de bisección
    tab_biseccion = tabview.add("Bisección")

    # Etiqueta y entrada para la función
    label_funcion = ctk.CTkLabel(tab_biseccion, text="Función f(x):")
    label_funcion.pack(pady=5)
    funcion_input = ctk.CTkTextbox(tab_biseccion, height=50)
    funcion_input.bind("<Button-1>", lambda event: mostrar_calculadora(funcion_input))  # Mostrar la calculadora al hacer clic
    funcion_input.pack(pady=5, padx=20)

    # Etiqueta y entrada para el límite inferior a
    label_a = ctk.CTkLabel(tab_biseccion, text="Límite inferior a:")
    label_a.pack(pady=5)
    a_input = ctk.CTkEntry(tab_biseccion)
    a_input.pack(pady=5)

    # Etiqueta y entrada para el límite superior b
    label_b = ctk.CTkLabel(tab_biseccion, text="Límite superior b:")
    label_b.pack(pady=5)
    b_input = ctk.CTkEntry(tab_biseccion)
    b_input.pack(pady=5)

    # Etiqueta y entrada para la tolerancia
    label_tol = ctk.CTkLabel(tab_biseccion, text="Tolerancia:")
    label_tol.pack(pady=5)
    tol_input = ctk.CTkEntry(tab_biseccion)
    tol_input.pack(pady=5)

    # Etiqueta y entrada para el número máximo de iteraciones
    label_max_iter = ctk.CTkLabel(tab_biseccion, text="Número máximo de iteraciones:")
    label_max_iter.pack(pady=5)
    max_iter_input = ctk.CTkEntry(tab_biseccion)
    max_iter_input.pack(pady=5)

    # Botón para ejecutar el método de bisección
    btn_ejecutar_biseccion = ctk.CTkButton(tab_biseccion, text="Ejecutar Bisección", command=ejecutar_biseccion)
    btn_ejecutar_biseccion.pack(pady=10)

    # Consola para mostrar los resultados
    consola_biseccion = ctk.CTkTextbox(tab_biseccion, height=100, width=450, font=("Courier", 12))
    consola_biseccion.pack(pady=10, padx=20)

    # Botón para mostrar los pasos
    btn_mostrar_pasos = ctk.CTkButton(tab_biseccion, text="Mostrar Pasos", command=mostrar_pasos_biseccion)
    btn_mostrar_pasos.pack(pady=10)

    # Consola para mostrar los pasos
    consola_pasos_biseccion = ctk.CTkTextbox(tab_biseccion, height=300, width=500, font=("Courier", 12))
    consola_pasos_biseccion.pack(pady=10, padx=20)

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

    # Crear la interfaz para el método de bisección en una pestaña separada
    crear_interfaz_biseccion(tabview)

    # Iniciar la aplicación
    root.mainloop()

# Ejecutar la función principal
if __name__ == "__main__":
    main()

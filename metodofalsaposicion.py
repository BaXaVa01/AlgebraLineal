import customtkinter as ctk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sympy as sp
import numpy as np

# Configuración de customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Función del método de la falsa posición
def falsa_posicion(funcion, a, b, tolerancia, max_iter=100):
    x = sp.symbols('x')
    f = sp.sympify(funcion)

    fa = f.subs(x, a)
    fb = f.subs(x, b)

    # Verificar que la función cambia de signo en [a, b]
    if fa * fb >= 0:
        raise ValueError("La función no cambia de signo en el intervalo [a, b].")

    iteraciones = []
    for i in range(max_iter):
        c = a - (fa * (b - a)) / (fb - fa)
        fc = f.subs(x, c)

        iteraciones.append((i + 1, float(a), float(b), float(c), float(fc)))

        if abs(fc) < tolerancia:
            return c, iteraciones

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    raise ValueError("El método no converge después de {} iteraciones.".format(max_iter))

# Función para graficar
def graficar(funcion, iteraciones, a, b):
    global ax, fig, canvas  # Accedemos a las variables globales

    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(funcion), "numpy")

    x_vals = np.linspace(a, b, 500)
    y_vals = f(x_vals)

    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(x_vals, y_vals, label=f"f(x) = {funcion}")
    ax.axhline(0, color='black', linewidth=0.8, linestyle="--")

    # Graficar iteraciones
    for _, a_val, b_val, c_val, _ in iteraciones:
        ax.scatter(c_val, 0, color='red')  # Punto raíz aproximado

    ax.set_title("Convergencia del Método de la Falsa Posición")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()

    # Crear el canvas para mostrar la gráfica
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    # Crear la barra de herramientas de Matplotlib
    toolbar = NavigationToolbar2Tk(canvas, frame_grafica)
    toolbar.update()  # Actualiza la barra de herramientas
    toolbar.pack(side="top", fill="x")

# Función para graficar y calcular
def calcular_raiz():
    try:
        funcion = entrada_funcion.get()
        a = float(entrada_a.get())
        b = float(entrada_b.get())
        tolerancia = float(entrada_tolerancia.get())

        raiz, iteraciones = falsa_posicion(funcion, a, b, tolerancia)

        resultados_texto = f"Raíz aproximada: {raiz:.6f}\n\n"
        resultados_texto += "Iteraciones:\n"
        resultados_texto += "n\t\ta\t\tb\t\tc\t\tf(c)\n"
        for it in iteraciones:
            resultados_texto += "{:d}\t\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\n".format(*it)

        area_resultados.configure(state="normal")
        area_resultados.delete("1.0", ctk.END)
        area_resultados.insert(ctk.END, resultados_texto)
        area_resultados.configure(state="disabled")

        # Limpiar gráfica previa si existe
        for widget in frame_grafica.winfo_children():
            widget.destroy()

        # Crear gráfica
        graficar(funcion, iteraciones, a, b)
        
    except ValueError as ve:
        messagebox.showwarning("Advertencia", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Ventana principal
app = ctk.CTk()
app.title("Método de la Falsa Posición")
app.geometry("900x600")

# Configuración de diseño
frame_principal = ctk.CTkFrame(app)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

titulo = ctk.CTkLabel(frame_principal, text="Método de la Falsa Posición", font=("Arial", 20, "bold"))
titulo.pack(pady=10)

frame_inputs = ctk.CTkFrame(frame_principal)
frame_inputs.pack(pady=10, padx=20, fill="x")

# Entradas de datos
ctk.CTkLabel(frame_inputs, text="Función (en términos de x):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entrada_funcion = ctk.CTkEntry(frame_inputs, width=300)
entrada_funcion.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_inputs, text="Límite a:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entrada_a = ctk.CTkEntry(frame_inputs, width=100)
entrada_a.grid(row=1, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(frame_inputs, text="Límite b:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entrada_b = ctk.CTkEntry(frame_inputs, width=100)
entrada_b.grid(row=2, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(frame_inputs, text="Tolerancia:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entrada_tolerancia = ctk.CTkEntry(frame_inputs, width=100)
entrada_tolerancia.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botón calcular
boton_calcular = ctk.CTkButton(frame_principal, text="Calcular Raíz", command=calcular_raiz)
boton_calcular.pack(pady=10)

# Resultados
ctk.CTkLabel(frame_principal, text="Resultados:").pack(pady=5)
area_resultados = ctk.CTkTextbox(frame_principal, height=150, state="disabled")
area_resultados.pack(pady=10, padx=20, fill="both")

# Gráfica
frame_grafica = ctk.CTkFrame(frame_principal, height=300)
frame_grafica.pack(pady=10, padx=20, fill="both", expand=True)

# Iniciar la app
app.mainloop()

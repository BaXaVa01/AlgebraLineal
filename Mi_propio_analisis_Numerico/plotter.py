# graficador.py
import numpy as np
import matplotlib.pyplot as plt

def graficar_funcion(func, x_min=-10, x_max=10, num_points=1000, y_min=-10, y_max=10, titulo="Gráfica de la Función", xlabel="x", ylabel="f(x)"):
    """
    Genera una gráfica de la función proporcionada, con ejes resaltados en negrita.
    
    Parámetros:
    - func: La función a graficar. Debe ser una función que acepte un valor de `x` y retorne el valor `f(x)`.
    - x_min: Valor mínimo de x en el eje (default es -10).
    - x_max: Valor máximo de x en el eje (default es 10).
    - num_points: Número de puntos a evaluar para la gráfica (default es 1000).
    - y_min: Valor mínimo en el eje y para escalar la vista.
    - y_max: Valor máximo en el eje y para escalar la vista.
    - titulo: Título de la gráfica (default es "Gráfica de la Función").
    - xlabel: Etiqueta del eje x (default es "x").
    - ylabel: Etiqueta del eje y (default es "f(x)").
    """
    # Generar valores de x
    x_vals = np.linspace(x_min, x_max, num_points)
    
    # Evaluar la función en cada valor de x y manejar errores de evaluación
    y_vals = []
    for x in x_vals:
        try:
            y = func(x)
            y_vals.append(y)
        except Exception:
            y_vals.append(np.nan)  # Asigna NaN para valores indefinidos

    # Convertir listas a arrays de numpy para mejorar la compatibilidad con matplotlib
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=titulo)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()

    # Ajustar límites del eje y si se especifican
    if y_min is not None and y_max is not None:
        plt.ylim(y_min, y_max)

    # Configurar los ejes en negrita
    ax = plt.gca()  # Obtener el objeto de ejes actual
    ax.spines['left'].set_linewidth(2)  # Eje y
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_linewidth(2)  # Eje x
    ax.spines['bottom'].set_color('black')


    ax.axhline(0, color='black', linewidth=2)  # Línea horizontal en y=0
    ax.axvline(0, color='black', linewidth=2)  # Línea vertical en x=0


    plt.show()

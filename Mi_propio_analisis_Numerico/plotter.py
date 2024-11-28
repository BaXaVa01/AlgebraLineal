# graficador.py
import numpy as np
import matplotlib.pyplot as plt

def graficar_funcion(funcs, x_min=-10, x_max=10, num_points=1000, y_min=-10, y_max=10, titulo="Gráfica de las Funciones", xlabel="x", ylabel="f(x)"):
    """
    Genera una gráfica de múltiples funciones proporcionadas, con ejes resaltados en negrita.
    
    Parámetros:
    - funcs: Lista de funciones a graficar. Cada función debe aceptar un valor de `x` y retornar el valor `f(x)`.
    - x_min: Valor mínimo de x en el eje (default es -10).
    - x_max: Valor máximo de x en el eje (default es 10).
    - num_points: Número de puntos a evaluar para la gráfica (default es 1000).
    - y_min: Valor mínimo en el eje y para escalar la vista.
    - y_max: Valor máximo en el eje y para escalar la vista.
    - titulo: Título de la gráfica (default es "Gráfica de las Funciones").
    - xlabel: Etiqueta del eje x (default es "x").
    - ylabel: Etiqueta del eje y (default es "f(x)").
    """
    # Generar valores de x
    x_vals = np.linspace(x_min, x_max, num_points)
    
    plt.figure(figsize=(10, 6))
    
    # Graficar cada función de la lista
    for func in funcs:
        # Evaluar la función en cada valor de x y manejar errores de evaluación
        y_vals = []
        for x in x_vals:
            try:
                y = func(x)
                y_vals.append(y)
            except Exception:
                y_vals.append(np.nan)  # Asigna NaN para valores indefinidos

        # Convertir lista a array de numpy para mejorar la compatibilidad con matplotlib
        y_vals = np.array(y_vals)

        # Agregar la función a la gráfica
        plt.plot(x_vals, y_vals, label=func.__name__ if hasattr(func, '__name__') else "Función sin nombre")

    # Configurar título, etiquetas y leyenda
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
  

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


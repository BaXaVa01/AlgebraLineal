import numpy as np
import matplotlib.pyplot as plt

# Función para graficar un vector
def plot_vector(v, color='b', label=None):
    plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color=color, label=label)

# Definir la matriz de transformación
A = np.array([[2, 1], [1, 2]])  # Puedes cambiar la matriz por cualquier otra

# Definir el vector original
v = np.array([1, 1])  # Puedes cambiar el vector por cualquier otro

# Aplicar la transformación lineal
v_transformed = np.dot(A, v)

# Crear la figura
plt.figure()

# Graficar el vector original (antes de la transformación)
plot_vector(v, color='b', label='Vector original')

# Graficar el vector transformado (después de la transformación)
plot_vector(v_transformed, color='r', label='Vector transformado')

# Configuración de la gráfica
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.xlim(-1, 0)
plt.ylim(0, -1)
plt.grid()
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.title('Transformación lineal de un vector')

# Mostrar la gráfica
plt.show()

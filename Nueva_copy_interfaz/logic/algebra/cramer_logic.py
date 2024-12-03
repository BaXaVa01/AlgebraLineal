import numpy as np
from .determinante_logic import determinante
# Regla de Cramer
def regla_cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la Regla de Cramer.
    """
    det_A = determinante(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única, determinante es cero.")

    n = len(A)
    x = np.zeros(n)
    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        x[i] = determinante(A_i) / det_A
    return x

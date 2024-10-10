def sumar_vectores(u, v):
    return [u[i] + v[i] for i in range(len(u))]

def multiplicar_matriz_vector(matriz, vector):
    resultado = []
    for fila in matriz:
        valor = sum(fila[i] * vector[i] for i in range(len(vector)))
        resultado.append(valor)
    return resultado

def son_vectores_iguales(u, v):
    return all([u[i] == v[i] for i in range(len(u))])

def mostrar_vector(vector):
    return f"[{', '.join(map(str, vector))}]"

def mostrar_matriz(matriz):
    return f"[{', '.join(mostrar_vector(fila) for fila in matriz)}]"

def validar_matriz_vectores(matriz, u, v):
    # Validar que la matriz tenga la misma cantidad de columnas que la longitud de los vectores
    num_columnas = len(matriz[0])
    if any(len(fila) != num_columnas for fila in matriz):
        raise ValueError("Todas las filas de la matriz deben tener la misma cantidad de columnas.")
    
    if len(u) != len(v):
        raise ValueError("Los vectores u y v deben tener la misma longitud.")
    
    if num_columnas != len(u):
        raise ValueError("La cantidad de columnas de la matriz debe ser igual a la longitud de los vectores.")

    # Si pasa todas las validaciones
    return True

def calcular(matriz, u, v):
    # Suma de los vectores u y v
    u_plus_v = sumar_vectores(u, v)

    # Multiplicación de la matriz por u+v
    A_u_plus_v = multiplicar_matriz_vector(matriz, u_plus_v)

    # Multiplicación de la matriz por u y por v
    A_u = multiplicar_matriz_vector(matriz, u)
    A_v = multiplicar_matriz_vector(matriz, v)

    # Suma de los productos
    A_u_plus_A_v = sumar_vectores(A_u, A_v)

    # Texto explicativo paso a paso
    steps = []
    steps.append(f"1. Suma de los vectores u y v:")
    steps.append(f"   u = {mostrar_vector(u)}")
    steps.append(f"   v = {mostrar_vector(v)}")
    steps.append(f"   u + v = {mostrar_vector(u)} + {mostrar_vector(v)} = {mostrar_vector(u_plus_v)}")
    steps.append("\n2. Multiplicación de la matriz A por el vector (u + v):")
    steps.append(f"   A = {mostrar_matriz(matriz)}")
    steps.append(f"   A(u + v) = A * {mostrar_vector(u_plus_v)} = {mostrar_vector(A_u_plus_v)}")
    steps.append("\n3. Multiplicación de A por u y A por v por separado:")
    steps.append(f"   Au = A * {mostrar_vector(u)} = {mostrar_vector(A_u)}")
    steps.append(f"   Av = A * {mostrar_vector(v)} = {mostrar_vector(A_v)}")
    steps.append("\n4. Suma de Au y Av:")
    steps.append(f"   Au + Av = {mostrar_vector(A_u)} + {mostrar_vector(A_v)} = {mostrar_vector(A_u_plus_A_v)}")

    # Verificar si se cumple la propiedad distributiva
    if son_vectores_iguales(A_u_plus_v, A_u_plus_A_v):
        steps.append(f"\nPropiedad distributiva verificada: A(u + v) = Au + Av")
        steps.append("\n**Explicación:**")
        steps.append("   Se cumple la propiedad distributiva porque:")
        steps.append("   A(u + v) es igual a la suma de los productos A por u y A por v por separado.")
    else:
        steps.append(f"\nLa propiedad distributiva NO se cumple")

    steps_text = "\n".join(steps)
    return steps_text
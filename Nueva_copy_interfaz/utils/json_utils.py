# utils/json_utils.py
import json
import os

# Calcular la ruta relativa a la carpeta "files" al mismo nivel que "main.py"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")

def obtener_ultimo_indice(json_path, metodo):
    """Obtiene el índice del último elemento para un método específico en el JSON."""
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
            if metodo in data and "funciones" in data[metodo]:
                return len(data[metodo]["funciones"]) - 1  # Último índice
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return -1  # Si no existe el método o el JSON está vacío


def guardar_input_operacion(metodo, funcion, variables,resultado,fprime=""):
    """
    Guarda una nueva operación en el archivo JSON.
    - metodo: Nombre del método, como "biseccion" o "newton_raphson".
    - funcion: La función utilizada en el cálculo.
    - variables: Un diccionario de variables (e.g., {"a": 1, "b": 2, "E": 0.01}).
    - resultado: El resultado o la raíz obtenida del cálculo.
    """
    # Verificar si el archivo JSON existe
    if not os.path.exists(JSON_PATH):
        # Crear la estructura inicial si no existe el archivo
        data = {}
    else:
        # Cargar el archivo JSON existente
        with open(JSON_PATH, "r") as file:
            data = json.load(file)

    # Estructura de la nueva operación
    if fprime=="":
        nueva_operacion = {
        "funcion": funcion,
        "variables": variables,
        "resultado": resultado
        }
    else:
        nueva_operacion = {
            "funcion": funcion,
            "variables": variables,
            "dx":fprime,
            "resultado": resultado
        }

    # Agregar la operación al método correspondiente
    if metodo not in data:
        data[metodo] = {"funciones": []}

    data[metodo]["funciones"].append(nueva_operacion)

    # Guardar los datos actualizados en el archivo JSON
    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)

def cargar_datos():
    """
    Carga los datos de operaciones guardadas en el archivo JSON.
    Retorna un diccionario con listas de operaciones por cada método si el archivo existe y es válido.
    Si el archivo no existe o está corrupto, retorna un diccionario vacío.
    """
    if not os.path.exists(JSON_PATH):
        print(f"El archivo JSON no existe en la ruta: {JSON_PATH}")
        return {}

    try:
        with open(JSON_PATH, "r") as file:
            data = json.load(file)

            # Validar que el JSON contenga un diccionario con el formato esperado
            if isinstance(data, dict):
                # Validar que cada clave (método) contenga un diccionario con una lista en "funciones"
                for metodo, contenido in data.items():
                    if not isinstance(contenido, dict) or "funciones" not in contenido or not isinstance(contenido["funciones"], list):
                        raise ValueError("Formato del JSON incorrecto. Se esperaba un diccionario con listas de funciones.")
                
                return data  # Retorna el JSON tal cual si pasa todas las validaciones
            else:
                raise ValueError("Formato del JSON incorrecto. Se esperaba un diccionario.")

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return {}
    except Exception as e:
        print(f"Error inesperado al cargar datos: {e}")
        return {}

def eliminar_operaciones(metodo, indices):
    """
    Elimina operaciones específicas de un método en el archivo JSON.
    
    - metodo: Nombre del método (e.g., "biseccion", "newton_raphson").
    - indices: Lista de índices a eliminar.
    """
    try:
        if not os.path.exists(JSON_PATH):
            raise FileNotFoundError("El archivo JSON no existe.")

        # Cargar datos actuales
        with open(JSON_PATH, "r") as file:
            data = json.load(file)

        if metodo not in data or "funciones" not in data[metodo]:
            raise ValueError(f"No se encontraron operaciones para el método: {metodo}")

        # Ordenar los índices en orden descendente para evitar problemas al eliminar
        indices = sorted(indices, reverse=True)

        # Eliminar las operaciones correspondientes
        for i in indices:
            del data[metodo]["funciones"][i]

        # Si no quedan funciones para el método, eliminar la clave del método
        if not data[metodo]["funciones"]:
            del data[metodo]

        # Guardar los cambios
        with open(JSON_PATH, "w") as file:
            json.dump(data, file, indent=4)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


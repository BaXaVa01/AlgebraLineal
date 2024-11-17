import os
import subprocess
import threading
from tkinter import messagebox

# Definir la ruta base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subimos un nivel desde 'utils'
ANIMATION_PATH = os.path.join(BASE_DIR, "animation.py")  # Ruta completa a animation.py

def generar_gif_desde_json(metodo, indice, callback=None):
    """
    Genera un GIF utilizando datos guardados en JSON en un hilo separado.
    - metodo: Nombre del método, como "biseccion" o "newton_raphson".
    - indice: Índice de la operación en el JSON.
    - callback: Función para recibir el path generado después de finalizar.
    """
    json_path = os.path.join(BASE_DIR, "files", "operaciones.json")  # Ruta al archivo JSON
    gifs_dir = os.path.join(BASE_DIR, "files", "gifs")  # Directorio para guardar los GIFs

    # Crear el directorio de gifs si no existe
    os.makedirs(gifs_dir, exist_ok=True)

    # Determinar la clase de animación según el método
    animation_class = "BiseccionAnimation" if metodo == "biseccion" else "NewtonRaphsonAnimation"

    # Generar el nombre del archivo GIF
    output_file = os.path.join(gifs_dir, f"{metodo}_{indice}.gif")

    def generar_en_hilo():
        # Asegurarse de que el archivo animation.py existe en la ruta especificada
        if not os.path.exists(ANIMATION_PATH):
            messagebox.showerror("Error", f"El archivo animation.py no se encontró en la ruta: {ANIMATION_PATH}")
            return

        # Ejecutar el comando de Manim para generar GIF
        result = subprocess.run([
            "manim", "-ql", ANIMATION_PATH, animation_class,
            "--format=gif",
            "--output_file", output_file,
            metodo, str(indice), json_path
        ])

        if result.returncode == 0:
            if callback:
                callback(output_file)  # Llamar al callback con el path generado
        else:
            messagebox.showerror("Error", "Hubo un error al generar el GIF desde JSON.")
            if callback:
                callback(None)  # Indicar error con None

    # Iniciar el hilo
    hilo = threading.Thread(target=generar_en_hilo)
    hilo.start()

    # Retornar el path esperado (aunque no está garantizado hasta que el hilo termine)
    return output_file

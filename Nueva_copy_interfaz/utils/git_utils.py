import os
import subprocess
import threading
from tkinter import messagebox

# Definir la ruta que sube un nivel para apuntar a "Nueva_copy_interfaz"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subimos un nivel desde 'utils'
ANIMATION_PATH = os.path.join(BASE_DIR, "animation.py")  # Ruta completa a animation.py

def generar_gif_desde_json(metodo, indice):
    """
    Genera un GIF utilizando datos guardados en JSON en un hilo separado.
    - metodo: Nombre del método, como "biseccion" o "newton_raphson".
    - indice: Índice de la operación en el JSON.
    """
    json_path = os.path.join(BASE_DIR, "files", "operaciones.json")  # Ruta al archivo JSON

    def generar_en_hilo():
        # Asegurarse de que el archivo animation.py existe en la ruta especificada
        if not os.path.exists(ANIMATION_PATH):
            messagebox.showerror("Error", f"El archivo animation.py no se encontró en la ruta: {ANIMATION_PATH}")
            return

        # Determinar la clase de animación según el método
        animation_class = "BiseccionAnimation" if metodo == "biseccion" else "NewtonRaphsonAnimation"

        # Ejecutar el comando de Manim para generar GIF
        result = subprocess.run([
            "manim", "-pql", ANIMATION_PATH, animation_class,
            "--format=gif",
            metodo, str(indice), json_path
        ])

        if result.returncode == 0:
            messagebox.showinfo("Éxito", "GIF generado correctamente desde JSON.")
        else:
            messagebox.showerror("Error", "Hubo un error al generar el GIF desde JSON.")

    # Iniciar el hilo
    hilo = threading.Thread(target=generar_en_hilo)
    hilo.start()

import os
import subprocess
import threading
from tkinter import messagebox
import customtkinter as ctk
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANIMATION_PATH = os.path.join(BASE_DIR, "animation.py")

def generar_gif_desde_json(metodo, indice, gif_frame, callback=None):
    """
    Genera un GIF utilizando datos guardados en JSON con una barra de progreso en el frame de los GIFs.
    - metodo: Nombre del método.
    - indice: Índice de la operación en el JSON.
    - gif_frame: Frame donde se muestra la barra de progreso y los GIFs.
    - callback: Función a ejecutar al finalizar.
    """
    json_path = os.path.join(BASE_DIR, "files", "operaciones.json")
    gifs_dir = os.path.join(BASE_DIR, "files", "gifs")
    os.makedirs(gifs_dir, exist_ok=True)

    animation_class = "BiseccionAnimation" if metodo == "biseccion" else "NewtonRaphsonAnimation"
    output_file = os.path.join(gifs_dir, f"{metodo}_{indice}.gif")

    # Crear barra de progreso dentro del frame de GIFs
    progress_frame = ctk.CTkFrame(gif_frame, fg_color="gray25", corner_radius=10)
    progress_frame.pack(fill="x", padx=10, pady=10)
    progress_label = ctk.CTkLabel(progress_frame, text=f"Generando GIF {metodo}...", font=("Arial", 12))
    progress_label.pack(side="top", pady=5)
    progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
    progress_bar.pack(fill="x", padx=10, pady=5)  # Adapta automáticamente al ancho del frame
    progress_bar.start()

    def generar_en_hilo():
        try:
            if not os.path.exists(ANIMATION_PATH):
                raise FileNotFoundError(f"El archivo animation.py no se encontró en la ruta: {ANIMATION_PATH}")

            result = subprocess.run([
                "manim", "-ql", ANIMATION_PATH, animation_class,
                "--format=gif",
                "--output_file", output_file,
                metodo, str(indice), json_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            gif_frame.after(0, progress_bar.stop)  # Detener la barra de progreso
            gif_frame.after(0, progress_frame.destroy)  # Eliminar el frame de la barra de progreso

            if result.returncode == 0:
                if callback:
                    gif_frame.after(0, lambda: callback(output_file))
            else:
                raise RuntimeError("Error al generar el GIF desde JSON.")
        except Exception as e:
            gif_frame.after(0, progress_bar.stop)
            gif_frame.after(0, progress_frame.destroy)
            gif_frame.after(0, lambda: messagebox.showerror("Error", str(e)))
            if callback:
                gif_frame.after(0, lambda: callback(None))

    # Iniciar hilo
    hilo = threading.Thread(target=generar_en_hilo)
    hilo.start()

    return output_file


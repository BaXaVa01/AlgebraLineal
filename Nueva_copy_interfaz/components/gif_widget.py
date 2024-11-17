import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import os

# Definir la ruta base relativa al archivo actual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subimos un nivel desde el directorio actual
GIFS_DIR = os.path.join(BASE_DIR, "files", "gifs")  # Directorio de GIFs


class GIFWidget(ctk.CTkFrame):
    def __init__(self, master, gif_paths=None, width=None, height=None, horizontal=False, **kwargs):
        """
        Widget para cargar y mostrar GIFs animados redimensionados.
        - master: Contenedor padre.
        - gif_paths: Lista de rutas de los GIFs.
        - width, height: Dimensiones deseadas para los GIFs.
        - horizontal: Si True, organiza los GIFs horizontalmente.
        """
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.horizontal = horizontal
        self.gif_labels = []  # Lista para etiquetas de GIFs
        self.frames = {}  # Diccionario para almacenar fotogramas de cada GIF
        self.running = False  # Control de animación de GIFs

        # Cargar y mostrar los GIFs
        self.load_gifs(gif_paths or self._get_default_gif_paths())

    def _get_default_gif_paths(self):
        """Obtiene las rutas de los GIFs del directorio predeterminado."""
        return [
            os.path.join(GIFS_DIR, file)
            for file in os.listdir(GIFS_DIR)
            if file.lower().endswith(".gif")
        ]

    def load_gifs(self, gif_paths, horizontal=False):
        """
        Carga y muestra múltiples GIFs en el widget.
        - gif_paths: Lista de rutas de los GIFs.
        - horizontal: Si True, organiza los GIFs horizontalmente.
        """
        self.clear_gifs()

        for gif_path in gif_paths:
            if os.path.isfile(gif_path):
                gif_label = ctk.CTkLabel(self, text="")  # Elimina cualquier texto predeterminado
                gif_label.pack(
                    side="left" if horizontal else "top", padx=2, pady=2  # Reduce el espaciado entre GIFs
                )
                self.gif_labels.append((gif_label, gif_path))
                self.frames[gif_path] = self._load_frames(gif_path)

        self.running = True
        self.animate_gifs()

    def _load_frames(self, gif_path):
        """Carga y redimensiona los fotogramas de un GIF."""
        frames = []
        with Image.open(gif_path) as img:
            for frame in ImageSequence.Iterator(img):
                resized_frame = frame.copy()
                if self.width and self.height:
                    resized_frame = resized_frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(resized_frame))
        return frames

    def animate_gifs(self):
        """Anima cada GIF cargado en el widget."""
        for gif_label, gif_path in self.gif_labels:
            if gif_path in self.frames:
                self._update_frame(gif_label, self.frames[gif_path], 0)

    def _update_frame(self, gif_label, frames, index):
        """Actualiza el fotograma actual de un GIF."""
        if not self.running:
            return
        gif_label.configure(image=frames[index])
        gif_label.image = frames[index]  # Mantener referencia para evitar el garbage collection
        self.after(100, self._update_frame, gif_label, frames, (index + 1) % len(frames))

    def clear_gifs(self):
        """Limpia todos los GIFs del widget."""
        self.running = False
        for gif_label, _ in self.gif_labels:
            gif_label.pack_forget()
        self.gif_labels.clear()
        self.frames.clear()





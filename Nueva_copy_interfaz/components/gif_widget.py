import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence
import os

class GIFWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack_propagate(False)
        
        # Lista para almacenar etiquetas de GIFs
        self.gif_labels = []
        self.running = False  # Control de animación de GIFs

    def load_gifs(self, gif_paths):
        """Carga y muestra múltiples GIFs en el widget."""
        self.clear_gifs()  # Limpiar GIFs existentes

        for gif_path in gif_paths:
            if os.path.isfile(gif_path) and gif_path.lower().endswith(".gif"):
                gif_label = ctk.CTkLabel(self)
                gif_label.pack(pady=5)
                self.gif_labels.append((gif_label, gif_path))
        
        self.running = True
        self.animate_gifs()

    def animate_gifs(self):
        """Anima cada GIF cargado en el widget."""
        for gif_label, gif_path in self.gif_labels:
            frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(Image.open(gif_path))]
            self._update_frame(gif_label, frames, 0)

    def _update_frame(self, gif_label, frames, index):
        """Actualiza el frame actual de un GIF."""
        if not self.running:
            return
        gif_label.configure(image=frames[index])
        self.after(100, self._update_frame, gif_label, frames, (index + 1) % len(frames))

    def clear_gifs(self):
        """Limpia todos los GIFs en el widget."""
        self.running = False
        for gif_label, _ in self.gif_labels:
            gif_label.pack_forget()
        self.gif_labels = []

    def open_gif_dialog(self):
        """Abre el diálogo para cargar GIFs desde el sistema de archivos."""
        gif_paths = filedialog.askopenfilenames(title="Selecciona archivos GIF", filetypes=[("GIF Files", "*.gif")])
        if gif_paths:
            self.load_gifs(gif_paths)

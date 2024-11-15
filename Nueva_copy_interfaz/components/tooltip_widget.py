# components/tooltip_widget.py
import customtkinter as ctk
from tkinter import Toplevel

class CTkToolTip(Toplevel):
    def __init__(self, widget, message="", delay=500, **kwargs):
        super().__init__(**kwargs)
        self.widget = widget
        self.message = message
        self.delay = delay  # Tiempo de retraso en ms antes de mostrar el mensaje
        self.withdraw()  # Ocultar inicialmente
        self.overrideredirect(True)  # Sin barra de título ni bordes
        self.after_id = None  # ID para el after

        # Configuración del contenido del tooltip
        self.bg_frame = ctk.CTkFrame(self, corner_radius=8)
        self.bg_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Mensaje en el tooltip
        self.label = ctk.CTkLabel(self.bg_frame, text=self.message, wraplength=200)
        self.label.pack()

        # Eventos para mostrar y ocultar el tooltip
        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

        self.showing = False  # Estado de visibilidad del tooltip

    def schedule_show(self, event=None):
        """Programar la aparición del tooltip después de un retraso."""
        if not self.showing:
            # Cancelar cualquier llamada programada anterior antes de programar una nueva
            if self.after_id:
                self.after_cancel(self.after_id)
            self.after_id = self.after(self.delay, self.show_tooltip)

    def show_tooltip(self):
        """Mostrar el tooltip en la posición del cursor."""
        self.showing = True
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.geometry(f"+{x}+{y}")
        self.deiconify()  # Mostrar el tooltip
        self.after_id = None  # Resetear el ID después de mostrar el tooltip

    def hide_tooltip(self, event=None):
        """Ocultar el tooltip y restablecer el estado."""
        # Cancelar el temporizador si el cursor sale antes de que el tooltip se muestre
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.showing = False
        self.withdraw()

    def move_tooltip(self, event=None):
        """Mover el tooltip con el cursor, si es necesario."""
        if self.showing:
            x = event.x_root + 20
            y = event.y_root + 20
            self.geometry(f"+{x}+{y}")

# components/sidebar.py
import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, title="Opciones", width=250, **kwargs):
        super().__init__(master, width=width, **kwargs)
        self.width_closed = 50  # Ancho cuando está retraída
        self.width_expanded = width  # Ancho cuando está expandida
        self.is_expanded = False  # Estado inicial de la sidebar (retraída)

        # Configuración de apariencia y título de la sidebar
        self.config(border_width=1, corner_radius=8)
        self.pack_propagate(False)
        
        # Botón para expandir/retraer la sidebar
        self.toggle_button = ctk.CTkButton(self, text=">", width=self.width_closed, command=self.toggle_sidebar)
        self.toggle_button.pack(side="top", pady=5)

        # Contenedor de contenido de la sidebar
        self.content_frame = ctk.CTkFrame(self, width=self.width_expanded - 20)
        self.content_frame.pack(side="top", fill="both", expand=True)
        self.content_frame.pack_forget()  # Ocultar el contenido al iniciar

        # Título de la barra lateral
        self.title_label = ctk.CTkLabel(self.content_frame, text=title, font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

    def toggle_sidebar(self):
        """Expande o retrae la sidebar y ajusta su contenido."""
        if self.is_expanded:
            # Contraer la sidebar
            self.configure(width=self.width_closed)
            self.toggle_button.configure(text=">")
            self.content_frame.pack_forget()
        else:
            # Expandir la sidebar
            self.configure(width=self.width_expanded)
            self.toggle_button.configure(text="<")
            self.content_frame.pack(fill="both", expand=True)
        self.is_expanded = not self.is_expanded

    def add_widget(self, widget, **kwargs):
        """Agrega un widget al contenido de la sidebar."""
        widget.pack(in_=self.content_frame, **kwargs)

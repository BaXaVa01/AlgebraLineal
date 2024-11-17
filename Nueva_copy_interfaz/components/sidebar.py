import customtkinter as ctk
import os
from components.gif_widget import GIFWidget


class FloatingSidebar(ctk.CTkFrame):
    def __init__(self, master, title="Opciones", width=250, height=150, from_right=True, **kwargs):
        super().__init__(master, width=width, **kwargs)  # Asignar ancho directamente en el constructor
        self.master = master
        self.default_width = width
        self.height = height
        self.from_right = from_right
        self.is_expanded = False  # Estado inicial (retraída)

        # Configuración inicial de apariencia
        self.configure(border_width=1, corner_radius=12, fg_color="gray20")
        self.place(x=self.master.winfo_width(), y=0, relheight=1)

        # Botón para expandir/retraer la sidebar
        self.toggle_button = ctk.CTkButton(self.master, text="☰", width=40, command=self.toggle_sidebar, fg_color="gray25")
        self.toggle_button.place(x=self.master.winfo_width() - 50, y=10)

        # Contenido de la sidebar
        self.content_frame = ctk.CTkFrame(self, fg_color="gray15", corner_radius=8)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título de la sidebar
        self.title_label = ctk.CTkLabel(self.content_frame, text=title, font=("Arial", 16, "bold"), text_color="white")
        self.title_label.pack(pady=15)

        # Scrollable frame para GIFs
        self.scrollable_gif_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="gray10", corner_radius=8)
        self.scrollable_gif_frame.pack(fill="both", expand=True, pady=10)

        # Botón para cerrar la sidebar
        self.close_button = ctk.CTkButton(self.content_frame, text="Cerrar", command=self.toggle_sidebar, fg_color="red")
        self.close_button.pack(side="bottom", pady=10)

        # Vincular eventos de redimensionamiento
        self.master.bind("<Configure>", self.update_position)

    def toggle_sidebar(self):
        """Controla la animación para expandir o retraer la sidebar."""
        current_width = self.winfo_width() if self.is_expanded else self.default_width
        target_x = self.master.winfo_width() if self.is_expanded else self.master.winfo_width() - current_width

        self.animate(target_x)
        self.is_expanded = not self.is_expanded
        self.toggle_button.configure(text="☰" if not self.is_expanded else "×")

    def animate(self, target_x):
        """Realiza la animación suave para mover la sidebar."""
        current_x = self.winfo_x()
        step = 10 if target_x > current_x else -10  # Dirección de la animación

        if abs(target_x - current_x) > abs(step):
            self.place(x=current_x + step, y=0, relheight=1)
            self.master.after(10, lambda: self.animate(target_x))
        else:
            self.place(x=target_x, y=0, relheight=1)  # Posiciona la sidebar en el destino final

    def update_position(self, event=None):
        """
        Mantiene la posición del botón y la sidebar sincronizados con la ventana principal,
        respetando el estado actual de expansión.
        """
        # Mantener el botón de toggle visible
        button_x = max(0, self.master.winfo_width() - 50)
        self.toggle_button.place(x=button_x, y=10)

        # Ajustar la posición de la sidebar según su estado
        if self.is_expanded:
            self.place(x=self.master.winfo_width() - self.default_width, y=0, relheight=1)
        else:
            self.place(x=self.master.winfo_width(), y=0, relheight=1)

    def show_single_gif(self, gif_path):
        """
        Muestra un único GIF en la sidebar.
        - gif_path: Ruta al archivo GIF a mostrar.
        """
        self.clear_gif_frame()
        if os.path.isfile(gif_path) and gif_path.lower().endswith(".gif"):
            gif_widget = GIFWidget(self.scrollable_gif_frame, gif_paths=[gif_path], width=200, height=200)
            gif_widget.pack(fill="both", expand=True)

    def clear_gif_frame(self):
        """Limpia el contenido de la sección de GIFs en la sidebar."""
        for widget in self.scrollable_gif_frame.winfo_children():
            widget.destroy()

    def show_gifs(self, horizontal):
        """Carga y muestra GIFs desde el directorio `files/gifs`."""
        # Ruta base para los GIFs
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gifs_dir = os.path.join(BASE_DIR, "files", "gifs")

        # Verificar si el directorio existe y tiene GIFs
        if not os.path.exists(gifs_dir):
            print(f"Directorio no encontrado: {gifs_dir}")
            return
        gif_files = [os.path.join(gifs_dir, f) for f in os.listdir(gifs_dir) if f.lower().endswith(".gif")]

        if not gif_files:
            print(f"No se encontraron archivos GIF en: {gifs_dir}")
            return

        # Crear el widget GIF y cargar los GIFs
        self.clear_gif_frame()
        for gif_path in gif_files:
            gif_widget = GIFWidget(self.scrollable_gif_frame, gif_paths=[gif_path], width=200, height=200)
            gif_widget.pack(fill="x", pady=5, padx=5)  # Los GIFs estarán organizados verticalmente

        

class FloatingSideBarUp(ctk.CTkFrame):
    def __init__(self, master, title="Opciones", width=250, height=150, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.default_height = height
        self.width = width
        self.is_expanded = False  # Estado inicial (retraída)

        # Configuración inicial de apariencia
        self.configure(border_width=1, corner_radius=12, fg_color="gray20")
        self.place(x=0, y=-self.default_height, relwidth=1)

        # Botón para expandir/retraer la sidebar
        self.toggle_button = ctk.CTkButton(self.master, text="▼", width=40, command=self.toggle_sidebar, fg_color="gray25")
        self.toggle_button.place(x=10, y=10)

        # Contenido de la sidebar
        self.content_frame = ctk.CTkFrame(self, fg_color="gray15", corner_radius=8)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título de la sidebar
        self.title_label = ctk.CTkLabel(self.content_frame, text=title, font=("Arial", 16, "bold"), text_color="white")
        self.title_label.pack(pady=15)

        # Espacio para los GIFs
        self.gif_frame = ctk.CTkFrame(self.content_frame, fg_color="gray10", corner_radius=8)
        self.gif_frame.pack(fill="both", expand=True, pady=10)

        # Botón para cerrar la sidebar
        self.close_button = ctk.CTkButton(self.content_frame, text="Cerrar", command=self.toggle_sidebar, fg_color="red")
        self.close_button.pack(side="bottom", pady=10)

        # Vincular eventos de redimensionamiento
        self.master.bind("<Configure>", self.update_position)

    def toggle_sidebar(self):
        """Controla la animación para expandir o retraer la sidebar."""
        current_y = self.winfo_y() if self.is_expanded else 0
        target_y = -self.default_height if self.is_expanded else 0

        self.animate(current_y, target_y)
        self.is_expanded = not self.is_expanded
        self.toggle_button.configure(text="▼" if not self.is_expanded else "▲")

    def animate(self, current_y, target_y):
        """Realiza la animación suave para mover la sidebar."""
        step = 10 if target_y > current_y else -10  # Dirección de la animación

        if abs(target_y - current_y) > abs(step):
            self.place(x=0, y=current_y + step, relwidth=1)
            self.master.after(10, lambda: self.animate(current_y + step, target_y))
        else:
            self.place(x=0, y=target_y, relwidth=1)  # Posiciona la sidebar en el destino final

    def update_position(self, event=None):
        """Mantiene la posición del botón y la sidebar sincronizados con la ventana principal."""
        button_y = max(0, 10)
        self.toggle_button.place(x=10, y=button_y)

        if self.is_expanded:
            self.place(x=0, y=0, relwidth=1)
        else:
            self.place(x=0, y=-self.default_height, relwidth=1)


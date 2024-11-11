import customtkinter as ctk
from ResolutorDeMatrices.resolutorMatrix import iniciar_interfaz
from analisis_Numerico.capturador2 import BiseccionInterface  # Importar BiseccionInterface

class MatrixCalcApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de la ventana principal
        self.title("MatrixCalc")
        self.geometry("800x600")
        
        # Diccionario para almacenar los frames de cada interfaz
        self.frames = {
            "main": MainFrame(self, self.show_frame),
            "interfaz1": Interfaz1Frame(self, self.show_frame),
            "interfaz2": Interfaz2Frame(self, self.show_frame)
        }
        
        # Mostrar el frame principal al inicio
        self.show_frame("main")
        
    def show_frame(self, frame_name):
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Reinicializar Interfaz2Frame y BiseccionInterface cada vez que se muestra
        if frame_name == "interfaz2":
            # Destruye la instancia anterior de Interfaz2Frame y vuelve a crearla
            self.frames["interfaz2"].destroy()
            self.frames["interfaz2"] = Interfaz2Frame(self, self.show_frame)
            self.frames["interfaz2"].initialize_interface()

        # Mostrar el frame seleccionado
        self.frames[frame_name].pack(fill="both", expand=True)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback

        # Configuración de la interfaz principal
        self.configure(bg_color="gray12")

        # Título principal estilizado
        title_label = ctk.CTkLabel(self, text="MatrixCalc", font=("Helvetica", 32, "bold"), text_color="lightblue")
        title_label.pack(pady=40)

        # Botones para cambiar entre interfaces
        self._crear_boton("Abrir Interfaz 1", "interfaz1", "blue")
        self._crear_boton("Abrir Interfaz 2", "interfaz2", "green")

    def _crear_boton(self, texto, frame_destino, color):
        button = ctk.CTkButton(
            self,
            text=texto,
            command=lambda: self.show_frame(frame_destino),
            font=("Helvetica", 16, "bold"),
            text_color="white",
            hover_color="lightblue",
            fg_color=color
        )
        button.pack(pady=20, ipadx=10, ipady=5)

class Interfaz1Frame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback
        iniciar_interfaz(self)  # Inicializar interfaz específica

        # Botón de regreso al menú principal
        self._crear_boton_volver()

    def _crear_boton_volver(self):
        back_button = ctk.CTkButton(self, text="Volver a la Interfaz Principal", command=lambda: self.show_frame("main"))
        back_button.pack(pady=10)

class Interfaz2Frame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback

        # Crear un CTkTabview para manejar la pestaña de bisección
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

    def initialize_interface(self):
        # Inicializar la interfaz de bisección utilizando BiseccionInterface y pasando el tabview
        BiseccionInterface(self.tabview)

        # Botón de regreso al menú principal
        self._crear_boton_volver()

    def _crear_boton_volver(self):
        back_button = ctk.CTkButton(self, text="Volver a la Interfaz Principal", command=lambda: self.show_frame("main"))
        back_button.pack(pady=10)

# Ejecutar la aplicación
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = MatrixCalcApp()
    app.mainloop()

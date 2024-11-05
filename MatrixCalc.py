import customtkinter as ctk
from PIL import Image, ImageTk
from ResolutorDeMatrices.resolutorMatrix import iniciar_interfaz
from analisis_Numerico.capturador2 import Interfaz_AN

class MatrixCalcApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de la ventana principal
        self.title("MatrixCalc")
        self.geometry("800x600")
        
        # Diccionario para almacenar los frames de cada interfaz
        self.frames = {}
        
        # Crear los frames para cada interfaz y almacenarlos en el diccionario
        self.frames["main"] = MainFrame(self, self.show_frame)
        self.frames["interfaz1"] = Interfaz1Frame(self, self.show_frame)
        self.frames["interfaz2"] = Interfaz2Frame(self, self.show_frame)
        
        # Mostrar el frame principal al inicio
        self.show_frame("main")
        
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        
        if frame_name == "interfaz2":
            self.frames[frame_name].initialize_interface()

        self.frames[frame_name].pack(fill="both", expand=True)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback

        # Configuración de la interfaz principal
        self.configure(bg_color="gray12")  # Fondo oscuro para estilo moderno

        # Título principal estilizado
        title_label = ctk.CTkLabel(self, text="MatrixCalc", font=("Helvetica", 32, "bold"), text_color="lightblue")
        title_label.pack(pady=40)

        # Botón para la Interfaz 1
        btn_interface1 = ctk.CTkButton(
            self,
            text="Abrir Interfaz 1",
            command=lambda: self.show_frame("interfaz1"),
            font=("Helvetica", 16, "bold"),
            text_color="white",
            hover_color="lightblue",
            fg_color="blue"
        )
        btn_interface1.pack(pady=20, ipadx=10, ipady=5)

        # Botón para la Interfaz 2
        btn_interface2 = ctk.CTkButton(
            self,
            text="Abrir Interfaz 2",
            command=lambda: self.show_frame("interfaz2"),
            font=("Helvetica", 16, "bold"),
            text_color="white",
            hover_color="lightblue",
            fg_color="green"
        )
        btn_interface2.pack(pady=20, ipadx=10, ipady=5)

class Interfaz1Frame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback
        iniciar_interfaz(self)
        back_button = ctk.CTkButton(self, text="Volver a la Interfaz Principal", command=lambda: self.show_frame("main"))
        back_button.pack(pady=10)

class Interfaz2Frame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent)
        self.show_frame = show_frame_callback


    def initialize_interface(self):
        Interfaz_AN(self.winfo_toplevel())
        back_button = ctk.CTkButton(self, text="Volver a la Interfaz Principal", command=lambda: self.show_frame("main"))
        back_button.pack(pady=10)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = MatrixCalcApp()
    app.mainloop()

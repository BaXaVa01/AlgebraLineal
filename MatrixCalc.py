import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from ResolutorDeMatrices.resolutorMatrix import iniciar_interfaz
from analisis_Numerico.capturador2 import Interfaz_AN
class MatrixCalcApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de la ventana principal
        self.title("MatrixCalc")
        self.geometry("800x600")
        
        # Título principal
        title_label = ctk.CTkLabel(self, text="MatrixCalc", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        # Frame principal para los botones y el GIF
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Botones para conectar interfaces
        btn_interface1 = ctk.CTkButton(main_frame, text="Abrir Interfaz 1", command=self.conectar_interface1)
        btn_interface1.pack(pady=10)
        
        btn_interface2 = ctk.CTkButton(main_frame, text="Abrir Interfaz 2", command=self.conectar_interface2)
        btn_interface2.pack(pady=10)
        
        # Frame para el GIF
        gif_frame = ctk.CTkFrame(main_frame, width=500, height=300)
        gif_frame.pack(pady=20)
        
        # Mostrar el GIF (opcional)
        self.display_gif(gif_frame, "ruta/a/tu_gif.gif")
        
    def conectar_interface1(self):
        iniciar_interfaz()
        
        
    def conectar_interface2(self):
        
        Interfaz_AN()
        
    def display_gif(self, parent, gif_path):
        try:
            # Cargar el GIF
            gif = Image.open(gif_path)
            
            # Configurar el GIF para que se ajuste automáticamente al tamaño del frame
            frames = [ImageTk.PhotoImage(frame.resize((500, 300), Image.ANTIALIAS)) for frame in ImageSequence.Iterator(gif)]
            label_gif = ctk.CTkLabel(parent)
            label_gif.pack(fill="both", expand=True)
            
            # Función para animar el GIF
            def animate_gif(frame_index=0):
                frame = frames[frame_index]
                label_gif.configure(image=frame)
                frame_index = (frame_index + 1) % len(frames)
                self.after(100, animate_gif, frame_index)  # Velocidad de animación
            
            animate_gif()  # Iniciar la animación
        except Exception as e:
            print("Error al cargar el GIF:", e)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = MatrixCalcApp()
    app.mainloop()

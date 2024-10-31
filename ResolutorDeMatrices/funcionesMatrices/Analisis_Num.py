from resolutorMatrix import *
# Función para inicializar la interfaz
def iniciar_interfaz():
    # Inicializar customtkinter
    ctk.set_appearance_mode("dark")  # Modo oscuro (opcional)
    ctk.set_default_color_theme("blue")  # Tema de color

    
    # Inicializar la ventana principal
    root = ctk.CTk()
    root.title("MATRIXCALC")
    root.geometry("1000x600")
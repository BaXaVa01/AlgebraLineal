# tabs/intro_tab.py
import customtkinter as ctk
from PIL import Image, ImageTk

class IntroTab:
    def __init__(self, tabview):
        # Crear la pestaña de introducción
        self.tab = tabview.add("Introducción")

        # Título de bienvenida
        self.title_label = ctk.CTkLabel(self.tab, text="Bienvenido a la App de Métodos Numéricos", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Imagen de bienvenida
        try:
            image = Image.open("noelle.png")  # Cambia el nombre del archivo a una imagen que tengas
            image = image.resize((300, 200))
            self.image = ImageTk.PhotoImage(image)
            self.image_label = ctk.CTkLabel(self.tab, image=self.image)
            self.image_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # Texto de instrucciones
        instructions = (
            "Esta aplicación ofrece varias herramientas numéricas para ayudar con el cálculo y visualización de funciones:\n\n"
            "1. **Calculadora de Expresiones**: Realiza cálculos matemáticos avanzados incluyendo funciones trigonométricas.\n"
            "2. **Método de Bisección**: Calcula raíces de funciones en intervalos específicos.\n"
            "3. **Método de Newton-Raphson**: Encuentra raíces de funciones usando aproximaciones sucesivas.\n"
            "4. **Graficador de Funciones**: Genera gráficos para visualizar cualquier función matemática en un rango especificado.\n\n"
            "Para empezar, selecciona una de las pestañas en la parte superior."
        )
        self.instructions_label = ctk.CTkLabel(self.tab, text=instructions, font=("Arial", 12), justify="left", wraplength=400)
        self.instructions_label.pack(pady=20, padx=20)

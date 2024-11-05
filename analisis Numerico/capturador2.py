import customtkinter as ctk
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageTk
import os
import tempfile
from Latex_Funct_Validator import crear_funcion  # Importa tu módulo de funciones aquí

class MatplotlibViewerModule(ctk.CTk):
    def __init__(self, latex_expr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de la ventana principal
        self.title("Visor de Gráficos Matplotlib - Tema Oscuro")
        self.geometry("800x600")
        
        # Etiqueta de título
        self.label = ctk.CTkLabel(self, text="Visualización de la Función", font=("Arial", 20))
        self.label.pack(pady=10)
        
        # Frame para mostrar el gráfico Matplotlib
        self.plot_frame = ctk.CTkFrame(self, width=780, height=500)
        self.plot_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Llamar a la función de graficación
        self.plot_graph(latex_expr)

    def plot_graph(self, latex_expr):
        try:
            # Crear la función evaluable a partir de la expresión LaTeX
            funcion = crear_funcion(latex_expr)

            # Generar datos para graficar
            x_values = [x * 0.1 for x in range(-100, 101)]  # Rango de -10 a 10 con pasos de 0.1
            y_values = [funcion(x) for x in x_values]

            # Aplicar estilo de tema oscuro
            plt.style.use("dark_background")
            sns.set(style="darkgrid", palette="deep")

            # Crear gráfico
            plt.figure(figsize=(10, 6))
            plt.plot(x_values, y_values, color="cyan", linewidth=2.5, linestyle='-', label=f"{latex_expr}")

            # Personalización del gráfico
            plt.title("Gráfico de la Función - Tema Oscuro", fontsize=16, fontweight='bold', color="white")
            plt.xlabel("Eje X", fontsize=14, fontweight='medium', color="lightgrey")
            plt.ylabel("f(x)", fontsize=14, fontweight='medium', color="lightgrey")
            plt.xticks(fontsize=12, color="lightgrey")
            plt.yticks(fontsize=12, color="lightgrey")
            plt.legend(loc="upper right", fontsize=12, fancybox=True, shadow=True)

            # Guardar el gráfico como PNG en una carpeta temporal
            temp_dir = tempfile.gettempdir()
            image_path = os.path.join(temp_dir, "matplotlib_plot_dark.png")
            plt.savefig(image_path, bbox_inches='tight', dpi=100)
            plt.close()  # Cerrar la figura para liberar memoria

            # Cargar la imagen en el frame de la interfaz
            img = Image.open(image_path)
            img = img.resize((780, 500), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS
            self.img_tk = ImageTk.PhotoImage(img)

            # Etiqueta de imagen para mostrar el gráfico
            label_img = ctk.CTkLabel(self.plot_frame, image=self.img_tk)
            label_img.pack(fill="both", expand=True)

            # Eliminar la imagen temporal después de cargarla
            os.remove(image_path)
        except Exception as e:
            print("Error en la generación del gráfico:", e)

# Ejemplo de uso
if __name__ == "__main__":
    latex_expr = r"\sin{x} + x^2"  # Ejemplo de expresión en LaTeX
    app = MatplotlibViewerModule(latex_expr)
    app.mainloop()


import customtkinter as ctk
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageTk
import os
import tempfile
from Latex_Funct_Validator import crear_funcion

def crear_frame_con_plot(parent, latex_expr):
    # Crear frame para el gráfico
    plot_frame = ctk.CTkFrame(parent, width=780, height=500)
    plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        # Crear la función evaluable a partir de la expresión LaTeX
        funcion = crear_funcion(latex_expr)

        # Generar datos para graficar
        x_values = [x * 0.1 for x in range(-100, 101)]
        y_values = [funcion(x) for x in x_values]

        # Aplicar tema oscuro al gráfico
        plt.style.use("dark_background")
        sns.set(style="darkgrid", palette="deep")

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, color="cyan", linewidth=2.5, linestyle='-', label=f"{latex_expr}")

        # Personalizar el gráfico
        plt.title("Gráfico de la Función - Tema Oscuro", fontsize=16, fontweight='bold', color="white")
        plt.xlabel("Eje X", fontsize=14, fontweight='medium', color="lightgrey")
        plt.ylabel("f(x)", fontsize=14, fontweight='medium', color="lightgrey")
        plt.xticks(fontsize=12, color="lightgrey")
        plt.yticks(fontsize=12, color="lightgrey")
        plt.legend(loc="upper right", fontsize=12, fancybox=True, shadow=True)

        # Guardar la imagen en una carpeta temporal
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, "matplotlib_plot_dark.png")
        plt.savefig(image_path, bbox_inches='tight', dpi=100)
        plt.close()  # Cerrar la figura para liberar memoria

        # Cargar la imagen en el frame
        img = Image.open(image_path)
        img = img.resize((780, 500), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        # Etiqueta de imagen para mostrar el gráfico
        label_img = ctk.CTkLabel(plot_frame, image=img_tk)
        label_img.image = img_tk  # Mantener referencia para evitar recolección de basura
        label_img.pack(fill="both", expand=True)

        # Botón para guardar la imagen
        def guardar_imagen():
            save_path = ctk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                img.save(save_path)

        # Crear y posicionar el botón de guardado
        boton_guardar = ctk.CTkButton(parent, text="Guardar imagen", command=guardar_imagen)
        boton_guardar.pack(pady=5)
        
        # Limpiar la imagen temporal
        os.remove(image_path)
    except Exception as e:
        print("Error en la generación del gráfico:", e)

# tabs/intro_tab.py
import customtkinter as ctk
from components.pdf_widget import CTkPDFViewer  # Importa el widget para visualizar PDFs
import os

class IntroTab:
    def __init__(self, tabview):
        # Crear la pestaña de introducción
        self.tab = tabview.add("Introducción")

        # Ruta al PDF
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(base_dir, "files", "pdfs", "DOCUMENTACION_MATHCALC.pdf")

        # Título de bienvenida
        self.title_label = ctk.CTkLabel(self.tab, text="Bienvenido a la App de Métodos Numéricos", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Visor de PDF
        try:
            self.pdf_viewer = CTkPDFViewer(self.tab, file=pdf_path, page_width=600, page_height=700)
            self.pdf_viewer.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            error_label = ctk.CTkLabel(self.tab, text=f"Error al cargar el PDF: {e}", font=("Arial", 12), fg_color="red")
            error_label.pack(pady=10)


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
        self.title_label = ctk.CTkLabel(
            self.tab, text="Bienvenido a la App de Métodos Numéricos", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)

        # Botón para mostrar el manual
        self.show_manual_button = ctk.CTkButton(
            self.tab,
            text="Mostrar Manual",
            command=lambda: self.show_pdf(pdf_path),
        )
        self.show_manual_button.pack(pady=20)

        # Frame para el visor del PDF (se ocultará inicialmente)
        self.pdf_frame = ctk.CTkFrame(self.tab)
        self.pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.pdf_frame.pack_forget()  # Ocultar inicialmente

    def show_pdf(self, pdf_path):
        """Muestra el visor de PDF en la pestaña."""
        try:
            # Si el visor ya está visible, no hacer nada
            if self.pdf_frame.winfo_ismapped():
                return

            # Deshabilitar el botón para evitar múltiples clics
            self.show_manual_button.configure(state="disabled")

            # Mostrar el frame del visor de PDF
            self.pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Cargar y mostrar el PDF
            self.pdf_viewer = CTkPDFViewer(
                self.pdf_frame, file=pdf_path, page_width=600, page_height=700
            )
            self.pdf_viewer.pack(fill="both", expand=True)
        except Exception as e:
            error_label = ctk.CTkLabel(self.tab, text=f"Error al cargar el PDF: {e}", font=("Arial", 12), fg_color="red")
            error_label.pack(pady=10)


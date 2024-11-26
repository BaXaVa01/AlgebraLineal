"""
CTkPDFViewer is a pdf viewer widget for customtkinter.
Author: Akash Bora
License: MIT
"""

import customtkinter
from PIL import Image
import fitz
import math
import io
import os
from tkinter import messagebox

class CTkPDFViewer(customtkinter.CTkScrollableFrame):

    def __init__(self,
                 master: any,
                 file: str,
                 page_width: int = 600,
                 page_height: int = 700,
                 page_separation_height: int = 2,
                 **kwargs):
        
        super().__init__(master, **kwargs)

        self.page_width = page_width
        self.page_height = page_height
        self.separation = page_separation_height
        self.pdf_images = []
        self.labels = []
        self.file = file

        self.percentage_view = 0
        self.percentage_load = customtkinter.StringVar()
        
        self.loading_message = customtkinter.CTkLabel(self, textvariable=self.percentage_load, justify="center")
        self.loading_message.pack(pady=10)

        self.loading_bar = customtkinter.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        self.loading_bar.pack(side="top", fill="x", padx=10)

        self.open_pdf = fitz.open(self.file)
        self.current_page = 0
        self.total_pages = len(self.open_pdf)
        self.after(250, self.load_next_page)

    def load_next_page(self):
        """Carga progresivamente las páginas del PDF."""
        try:
            if self.current_page < self.total_pages:
                # Procesar la página actual
                page = self.open_pdf[self.current_page]
                page_data = page.get_pixmap()
                pix = fitz.Pixmap(page_data, 0) if page_data.alpha else page_data
                img = Image.open(io.BytesIO(pix.tobytes('ppm')))
                
                # Crear la imagen y almacenarla
                label_img = customtkinter.CTkImage(img, size=(self.page_width, self.page_height))
                self.pdf_images.append(label_img)  # Mantener referencia

                # Actualizar barra de progreso
                self.current_page += 1
                percentage_view = (float(self.current_page) / float(self.total_pages) * float(100))
                self.loading_bar.set(percentage_view / 100)
                self.percentage_load.set(f"Loading {os.path.basename(self.file)} \n{int(math.floor(percentage_view))}%")

                # Mostrar la imagen como etiqueta
                label = customtkinter.CTkLabel(self, image=label_img, text="")
                label.pack(pady=(0, self.separation))
                self.labels.append(label)

                # Programar la carga de la siguiente página
                self.after(50, self.load_next_page)
            else:
                # Finalizar el proceso de carga
                self.loading_bar.pack_forget()
                self.loading_message.pack_forget()
                self.open_pdf.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error durante la carga de páginas: {e}")


    def configure(self, **kwargs):
        """ configurable options """
        
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            self.pdf_images = []
            for i in self.labels:
                i.destroy()
            self.labels = []
            self.current_page = 0
            self.total_pages = 0
            self.open_pdf = fitz.open(self.file)
            self.after(250, self.load_next_page)
            
        if "page_width" in kwargs:
            self.page_width = kwargs.pop("page_width")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
                
        if "page_height" in kwargs:
            self.page_height = kwargs.pop("page_height")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for i in self.labels:
                i.pack_forget()
                i.pack(pady=(0,self.separation))
        
        super().configure(**kwargs)

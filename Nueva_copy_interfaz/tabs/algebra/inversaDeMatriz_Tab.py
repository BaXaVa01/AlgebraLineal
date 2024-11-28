from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from customtkinter import CTkFrame
from utils.matrixDisplay_utils  import MatrizEditable  # Clase MatrizEditable importada

class InversaDeMatriz_Tab(QWidget):
    def __init__(self, tabview):

        super().__init__()
        self.tab = tabview.add("Inversa de Matriz")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Título del tab
        self.title_label = QLabel("Inversa de Matriz", self)
        self.layout.addWidget(self.title_label)

        # Input para filas y columnas
        input_layout = QHBoxLayout()
        self.filas_input = QLineEdit()
        self.filas_input.setPlaceholderText("Filas")
        input_layout.addWidget(QLabel("Filas:"))
        input_layout.addWidget(self.filas_input)

        self.columnas_input = QLineEdit()
        self.columnas_input.setPlaceholderText("Columnas")
        input_layout.addWidget(QLabel("Columnas:"))
        input_layout.addWidget(self.columnas_input)

        # Botón para generar matriz
        self.generar_btn = QPushButton("Generar Matriz")
        input_layout.addWidget(self.generar_btn)
        self.generar_btn.clicked.connect(self.generar_matriz)  # Vincular al método para generar matriz

        self.layout.addLayout(input_layout)

        # Contenedor para la matriz generada
        self.matriz_container = None

    def generar_matriz(self):
        try:
            # Leer valores de filas y columnas
            filas = int(self.filas_input.text())
            columnas = int(self.columnas_input.text())

            if filas <= 0 or columnas <= 0:
                raise ValueError("Las dimensiones deben ser mayores a 0.")

            # Eliminar matriz anterior, si existe
            if self.matriz_container:
                self.layout.removeWidget(self.matriz_container)
                self.matriz_container.deleteLater()
                self.matriz_container = None

            # Crear un contenedor con customtkinter para la matriz
            self.matriz_container = CTkFrame()
            self.matriz_editable = MatrizEditable(self.matriz_container, filas, columnas)

            # Agregar el contenedor al layout principal
            self.layout.addWidget(self.matriz_container)

        except ValueError:
            QMessageBox.warning(self, "Error", "Introduce valores válidos para filas y columnas.")

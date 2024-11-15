# tabs/calculator_tab.py
import customtkinter as ctk
from components.calculator_widget import CalculatorWidget

class CalculatorTab:
    def __init__(self, tabview):
        # Crear la pestaña de la calculadora
        self.tab = tabview.add("Calculadora")

        # Instancia de la calculadora de expresiones
        self.calculator = CalculatorWidget(self.tab)
        self.calculator.pack(pady=20, padx=20)

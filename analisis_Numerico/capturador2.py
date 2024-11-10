import customtkinter as ctk
from analisis_Numerico.calculadora import mostrar_calculadora
from analisis_Numerico.aproxfunctions import definir_intervalo_auto
from analisis_Numerico.plotter import inicializar_grafico, actualizar_grafico
from analisis_Numerico.Latex_Funct_Validator import crear_funcion

class BiseccionInterface:
    def __init__(self, parent):
        self.tab = parent.add("Bisección")
        self.pasos_biseccion = []

        # Crear widgets de entrada
        self.funcion_input = self._crear_textbox("Función f(x):", self.tab, on_click=mostrar_calculadora)
        self.a_input = self._crear_entry("Límite inferior a:", self.tab)
        self.b_input = self._crear_entry("Límite superior b:", self.tab)
        self.tol_input = self._crear_entry("Tolerancia:", self.tab)
        self.max_iter_input = self._crear_entry("Número máximo de iteraciones:", self.tab)
        self.consola_biseccion = self._crear_textbox("Resultado:", self.tab, height=100)
        self.consola_pasos_biseccion = self._crear_textbox("Pasos:", self.tab, height=300)

        # Botones de acción
        self._crear_button("Elegir puntos automáticamente", self.tab, self.elegir_puntos_automaticamente)
        self._crear_button("Ejecutar Bisección", self.tab, self.ejecutar_biseccion)
        self._crear_button("Mostrar Pasos", self.tab, self.mostrar_pasos_biseccion)

        # Inicializar el gráfico en el frame
        self.fig, self.ax, self.canvas = inicializar_grafico(self.tab)

    def _crear_textbox(self, label_text, parent, height=50, on_click=None):
        ctk.CTkLabel(parent, text=label_text).pack(pady=5)
        textbox = ctk.CTkTextbox(parent, height=height)
        textbox.pack(pady=5, padx=20)
        if on_click:
            textbox.bind("<Button-1>", lambda event: on_click(textbox))
        return textbox

    def _crear_entry(self, label_text, parent):
        ctk.CTkLabel(parent, text=label_text).pack(pady=5)
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        return entry

    def _crear_button(self, text, parent, command):
        button = ctk.CTkButton(parent, text=text, command=command)
        button.pack(pady=10)
        return button

    def elegir_puntos_automaticamente(self):
        funcion = self.funcion_input.get("1.0", "end-1c")
        try:
            a, b = definir_intervalo_auto(funcion)
            self.a_input.delete(0, "end")
            self.a_input.insert(0, str(a))
            self.b_input.delete(0, "end")
            self.b_input.insert(0, str(b))
        except Exception as e:
            self._actualizar_consola(self.consola_biseccion, f"Error al calcular puntos automáticamente: {e}")

    def ejecutar_biseccion(self):
        try:
            funcion_texto = self.funcion_input.get("1.0", "end-1c")
            a, b = float(self.a_input.get()), float(self.b_input.get())
            E, max_iter = float(self.tol_input.get()), int(self.max_iter_input.get())
            funcion = crear_funcion(funcion_texto)

            # Ejecutar el método de bisección
            raiz, error, pasos, iteraciones = self._biseccion(funcion, a, b, E, max_iter)
            self.pasos_biseccion = pasos
            self._actualizar_consola(self.consola_biseccion, f"Converge en {iteraciones} iteraciones.\nRaíz: {raiz} (Error: {error}%)")

            # Graficar la función en el intervalo especificado
            actualizar_grafico(self.ax, self.canvas, funcion, x_min=a, x_max=b)
        except Exception as e:
            self._actualizar_consola(self.consola_biseccion, f"Error inesperado: {e}")

    def mostrar_pasos_biseccion(self):
        self._actualizar_consola(self.consola_pasos_biseccion, "\n".join(self.pasos_biseccion))

    def _biseccion(self, f, a, b, E=1e-5, max_iter=100):
        iter_count, pasos, prev_c = 0, [], (a + b) / 2.0
        while (b - a) / 2.0 > E and iter_count < max_iter:
            c = (a + b) / 2.0
            pasos.append(f"Iteración {iter_count + 1}: a = {a}, b = {b}, c = {c}, f(c) = {f(c)}")
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
            error_relativo = abs((c - prev_c) / c) * 100 if iter_count > 0 else float('inf')
            prev_c, iter_count = c, iter_count + 1
        return c, error_relativo, pasos, iter_count

    def _actualizar_consola(self, consola, mensaje):
        consola.delete("1.0", "end")
        consola.insert("1.0", mensaje)

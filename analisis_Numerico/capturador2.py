import customtkinter as ctk
from analisis_Numerico.calculadora import mostrar_calculadora
from analisis_Numerico.aproxfunctions import definir_intervalo_auto
from analisis_Numerico.plotter import inicializar_grafico, actualizar_grafico
from analisis_Numerico.Latex_Funct_Validator import crear_funcion

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind_all("<MouseWheel>")


class BiseccionInterface:
    def __init__(self, parent):
        self.tab = parent.add("Bisección")
        self.pasos_biseccion = []

        # Crear un frame scrollable
        self.scrollable_frame = ScrollableFrame(self.tab, width=460, height=580)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Crear widgets de entrada
        self.funcion_input = self._crear_textbox("Función f(x):", self.scrollable_frame, on_click=mostrar_calculadora)
        self.a_input = self._crear_entry("Límite inferior a:", self.scrollable_frame)
        self.b_input = self._crear_entry("Límite superior b:", self.scrollable_frame)
        self.tol_input = self._crear_entry("Tolerancia:", self.scrollable_frame)
        self.max_iter_input = self._crear_entry("Número máximo de iteraciones:", self.scrollable_frame)
        self.consola_biseccion = self._crear_textbox("Resultado:", self.scrollable_frame, height=100)
        self.consola_pasos_biseccion = self._crear_textbox("Pasos:", self.scrollable_frame, height=300)

        # Botones de acción
        self._crear_button("Elegir puntos automáticamente", self.scrollable_frame, self.elegir_puntos_automaticamente)
        self._crear_button("Ejecutar Bisección", self.scrollable_frame, self.ejecutar_biseccion)
        self._crear_button("Mostrar Pasos", self.scrollable_frame, self.mostrar_pasos_biseccion)

        # Inicializar el gráfico en el frame
        self.fig, self.ax, self.canvas = inicializar_grafico(self.scrollable_frame)

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
            
            # Verificar si 'a' y 'b' son convertibles a float antes de insertarlos
            a = float(a)
            b = float(b)
            
            # Insertar valores en los campos de entrada
            self.a_input.delete(0, "end")
            self.a_input.insert(0, str(a))
            self.b_input.delete(0, "end")
            self.b_input.insert(0, str(b))
        except ValueError as ve:
            self._actualizar_consola(self.consola_biseccion, f"Error de valor: {ve}")
        except Exception as e:
            self._actualizar_consola(self.consola_biseccion, f"Error al calcular puntos automáticamente: {e}")


    def ejecutar_biseccion(self):
        try:
            # Lee el texto de la función y convierte a una función evaluable
            funcion_texto = self.funcion_input.get("1.0", "end-1c")
            funcion = crear_funcion(funcion_texto)

            # Lee los valores del intervalo y los otros parámetros
            a, b = float(self.a_input.get()), float(self.b_input.get())
            E, max_iter = float(self.tol_input.get()), int(self.max_iter_input.get())

            # Ejecuta el método de bisección
            raiz, error, pasos, iteraciones = self._biseccion(funcion, a, b, E, max_iter)
            self.pasos_biseccion = pasos

            # Muestra los resultados
            self._actualizar_consola(self.consola_biseccion, f"Converge en {iteraciones} iteraciones.\nRaíz: {raiz} (Error: {error}%)")

            # Graficar la función en el intervalo
            actualizar_grafico(self.ax, self.canvas, funcion, x_min=a, x_max=b)
        except ValueError as ve:
            self._actualizar_consola(self.consola_biseccion, f"Error de valor: {ve}")
        except Exception as e:
            self._actualizar_consola(self.consola_biseccion, f"Error inesperado: {e}")

    def mostrar_pasos_biseccion(self):
        self._actualizar_consola(self.consola_pasos_biseccion, "\n".join(self.pasos_biseccion))

    def _biseccion(self, f, a, b, E=1e-5, max_iter=100):
        iter_count, pasos = 0, []
        c = None  # Inicializa 'c' con un valor por defecto para evitar el error de no inicialización
        prev_c = (a + b) / 2.0  # Valor inicial de prev_c

        # Asegura que el intervalo sea válido
        if f(a) * f(b) >= 0:
            raise ValueError("La función debe tener signos opuestos en los extremos del intervalo [a, b].")

        while (b - a) / 2.0 > E and iter_count < max_iter:
            c = (a + b) / 2.0
            pasos.append(f"Iteración {iter_count + 1}: a = {a}, b = {b}, c = {c}, f(c) = {f(c)}")
            if f(c) == 0:
                return c, 0, pasos, iter_count + 1  # Raíz exacta encontrada
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c

            # Calcula el error relativo porcentual
            error_relativo = abs((c - prev_c) / c) * 100 if iter_count > 0 else float('inf')
            prev_c = c
            iter_count += 1

        if c is None:
            raise ValueError("No se encontró una raíz en el intervalo dado.")  # Manejo del caso donde 'c' nunca se asigna

        return c, error_relativo, pasos, iter_count

    def _actualizar_consola(self, consola, mensaje):
        consola.delete("1.0", "end")
        consola.insert("1.0", mensaje)
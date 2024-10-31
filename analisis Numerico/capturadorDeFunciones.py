import customtkinter as ctk

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ventana principal
app = ctk.CTk()
app.title("Interfaz de Funciones")
app.geometry("400x600")

# Campo de texto para ingresar funciones
func_entry = ctk.CTkEntry(app, width=300, font=("Arial", 20))
func_entry.pack(pady=20)

# Frame para los botones de operadores y funciones
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

# Función para insertar texto en el campo de entrada
def insert_text(text):
    func_entry.insert("end", text)

# Botones de operadores básicos
btn_add = ctk.CTkButton(button_frame, text="+", command=lambda: insert_text("+"), width=60)
btn_subtract = ctk.CTkButton(button_frame, text="-", command=lambda: insert_text("-"), width=60)
btn_multiply = ctk.CTkButton(button_frame, text="*", command=lambda: insert_text("*"), width=60)
btn_divide = ctk.CTkButton(button_frame, text="/", command=lambda: insert_text("/"), width=60)

# Organizar botones en una cuadrícula
btn_add.grid(row=0, column=0, padx=5, pady=5)
btn_subtract.grid(row=0, column=1, padx=5, pady=5)
btn_multiply.grid(row=0, column=2, padx=5, pady=5)
btn_divide.grid(row=0, column=3, padx=5, pady=5)

# Botones de funciones avanzadas
btn_sqrt = ctk.CTkButton(button_frame, text="√", command=lambda: insert_text("√("), width=60)
btn_pow = ctk.CTkButton(button_frame, text="^", command=lambda: insert_text("^"), width=60)
btn_frac = ctk.CTkButton(button_frame, text="a/b", command=lambda: insert_text("/"), width=60)
btn_parentheses = ctk.CTkButton(button_frame, text="()", command=lambda: insert_text("("), width=60)

# Organizar botones en una cuadrícula
btn_sqrt.grid(row=1, column=0, padx=5, pady=5)
btn_pow.grid(row=1, column=1, padx=5, pady=5)
btn_frac.grid(row=1, column=2, padx=5, pady=5)
btn_parentheses.grid(row=1, column=3, padx=5, pady=5)

# Botones de funciones trigonométricas
btn_sin = ctk.CTkButton(button_frame, text="sin", command=lambda: insert_text("sin("), width=60)
btn_cos = ctk.CTkButton(button_frame, text="cos", command=lambda: insert_text("cos("), width=60)
btn_tan = ctk.CTkButton(button_frame, text="tan", command=lambda: insert_text("tan("), width=60)
btn_log = ctk.CTkButton(button_frame, text="log", command=lambda: insert_text("log("), width=60)

# Organizar botones en una cuadrícula
btn_sin.grid(row=2, column=0, padx=5, pady=5)
btn_cos.grid(row=2, column=1, padx=5, pady=5)
btn_tan.grid(row=2, column=2, padx=5, pady=5)
btn_log.grid(row=2, column=3, padx=5, pady=5)

# Botón de limpiar entrada
btn_clear = ctk.CTkButton(app, text="Limpiar", command=lambda: func_entry.delete(0, "end"), width=300)
btn_clear.pack(pady=20)

# Ejecutar la aplicación
app.mainloop()

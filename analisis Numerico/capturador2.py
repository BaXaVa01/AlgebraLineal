import customtkinter as ctk
# from Latex_Funct_Validator import crear_funcion

# Configuración inicial de la aplicación
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ventana principal
app = ctk.CTk()
app.title("Interfaz de Funciones")
app.geometry("500x600")

# Campo de texto para ingresar funciones o números
entry = ctk.CTkEntry(app, width=400, font=("Arial", 20))
entry.pack(pady=20)

# Frame principal que contiene el frame lateral y el frame de botones
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=10, padx=10)

# Frame lateral para los botones de cambio de modo y limpiar
side_frame = ctk.CTkFrame(main_frame)
side_frame.grid(row=0, column=0, padx=10)

# Frame para los botones numéricos y de funciones
button_frame = ctk.CTkFrame(main_frame)
button_frame.grid(row=0, column=1, padx=10)

# Variable para alternar entre modos
mode = "Funciones"


# Función para insertar texto en el campo de entrada
def insert_text(text, latexFormat):
    entry.configure(state='normal')
    entry.insert(ctk.END, text)
    entry.insert(ctk.END, latexFormat)
    entry.configure(state='readonly')
    

# Función para alternar entre modos
def toggle_mode():
    global mode
    mode = "Numérico" if mode == "Funciones" else "Funciones"
    toggle_button.configure(text=f"Cambiar a {mode}")
    update_buttons()

# Actualizar botones según el modo seleccionado
def update_buttons():
    # Limpiar botones existentes
    for widget in button_frame.winfo_children():
        widget.destroy()
    
    if mode == "Funciones":
        # Botones de operadores básicos

        btn_add = ctk.CTkButton(button_frame, text="+", command=lambda: insert_text("+", "\\text{sum}"), width=60)
        btn_subtract = ctk.CTkButton(button_frame, text="-", command=lambda: insert_text("-", "\\text{subtract}"), width=60)
        btn_multiply = ctk.CTkButton(button_frame, text="*", command=lambda: insert_text("*", "\\text{multiply}"), width=60)
        btn_divide = ctk.CTkButton(button_frame, text="/", command=lambda: insert_text("/", "\\text{divide}"), width=60)

        btn_add.grid(row=0, column=0, padx=5, pady=5)
        btn_subtract.grid(row=0, column=1, padx=5, pady=5)
        btn_multiply.grid(row=0, column=2, padx=5, pady=5)
        btn_divide.grid(row=0, column=3, padx=5, pady=5)

        # Botones de funciones avanzadas
        btn_sqrt = ctk.CTkButton(button_frame, text="√", command=lambda: insert_text("√(", "\\sqrt{}"), width=60)
        btn_pow = ctk.CTkButton(button_frame, text="^", command=lambda: insert_text("^", "^{}"), width=60)
        btn_frac = ctk.CTkButton(button_frame, text="a/b", command=lambda: insert_text("/", "\\frac{}{}"), width=60)
        btn_parentheses = ctk.CTkButton(button_frame, text="(", command=lambda: insert_text("(", "\\left("), width=60)

        btn_parentheses_right = ctk.CTkButton(button_frame, text=")", command=lambda: insert_text(")", "\\right("), width=60)

        btn_sqrt.grid(row=1, column=0, padx=5, pady=5)
        btn_pow.grid(row=1, column=1, padx=5, pady=5)
        btn_frac.grid(row=1, column=2, padx=5, pady=5)
        btn_parentheses.grid(row=1, column=3, padx=5, pady=5)
        btn_parentheses_right.grid(row=1, column=4, padx=5, pady=5)

        # Botones de funciones trigonométricas
        btn_sin = ctk.CTkButton(button_frame, text="sin", command=lambda: insert_text("sin(", "\\sin{}"), width=60)
        btn_cos = ctk.CTkButton(button_frame, text="cos", command=lambda: insert_text("cos(", "\\cos{}"), width=60)
        btn_tan = ctk.CTkButton(button_frame, text="tan", command=lambda: insert_text("tan(", "\\tan{}"), width=60)
        btn_log = ctk.CTkButton(button_frame, text="log", command=lambda: insert_text("log(", "\\log{}"), width=60)

        btn_sin.grid(row=2, column=0, padx=5, pady=5)
        btn_cos.grid(row=2, column=1, padx=5, pady=5)
        btn_tan.grid(row=2, column=2, padx=5, pady=5)
        btn_log.grid(row=2, column=3, padx=5, pady=5)

    else:
        # Botones numéricos y de operadores básicos
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 0), ('=', 4, 2),
            ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3)
        ]

        for (text, row, col) in buttons:
            ctk.CTkButton(button_frame, text=text, command=lambda t=text: insert_text(t), width=60).grid(row=row, column=col, padx=5, pady=5)

# Botón para alternar entre modos en el frame lateral
toggle_button = ctk.CTkButton(side_frame, text="Cambiar a Numérico", command=toggle_mode, width=100)
toggle_button.pack(pady=10)

# Botón de limpiar entrada en el frame lateral
btn_clear = ctk.CTkButton(side_frame, text="Limpiar", command=lambda: func_entry.delete(0, "end"), width=100)
btn_clear.pack(pady=10)

# Inicializar los botones en el modo "Funciones"
update_buttons()

# Ejecutar la aplicación
app.mainloop()

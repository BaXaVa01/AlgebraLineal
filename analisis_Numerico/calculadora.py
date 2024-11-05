import customtkinter as ctk

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

# Variable para alternar entre modos
mode = "Funciones"

# Función para mostrar la calculadora en una ventana flotante
def mostrar_calculadora(entry_destino):
    # Crear ventana flotante para la calculadora
    calc_window = ctk.CTkToplevel(app)
    calc_window.title("Calculadora")
    calc_window.geometry("300x400")
    
    # Frame para botones en la calculadora
    button_frame = ctk.CTkFrame(calc_window)
    button_frame.pack(pady=10, padx=10)

    # Función para insertar texto en el entry destino
# Función para insertar texto en la posición del cursor en un CTkTextbox
# Función para insertar texto en la posición del cursor en un CTkTextbox
    def insert_text(text):
        # Habilitar el campo de entrada temporalmente
        entry_destino.configure(state='normal')
        cursor_position = entry_destino.index("insert")  # Obtener la posición actual del cursor, en formato "line.column"
        
        # Extraer solo la columna de la posición y convertirla a entero
        cursor_column = int(cursor_position.split('.')[1])  # Obtiene solo la columna como entero
        
        current_text = entry_destino.get("1.0", "end-1c")  # Obtener el texto actual del campo de entrada
        
        # Verificar si se debe insertar un "*" antes de la nueva entrada
        if cursor_column > 0 and current_text[cursor_column - 1].isdigit():
            entry_destino.insert(cursor_position, "*")
            cursor_position = entry_destino.index("insert")  # Actualizar la posición después de insertar "*"
        
        # Insertar el texto en la posición del cursor
        entry_destino.insert(cursor_position, text)
        entry_destino.configure(state='readonly')  # Bloquear el campo de entrada nuevamente


    # Función para alternar entre modos
    def toggle_mode():
        global mode
        mode = "Numérico" if mode == "Funciones" else "Funciones"
        toggle_button.configure(text=f"Cambiar a {mode}")
        update_buttons()

    # Función para actualizar botones según el modo seleccionado
    def update_buttons():
        # Limpiar botones existentes
        for widget in button_frame.winfo_children():
            widget.destroy()
        
        if mode == "Funciones":
            # Botones de operadores básicos
            btn_add = ctk.CTkButton(button_frame, text="+", command=lambda: insert_text("+"), width=60)
            btn_subtract = ctk.CTkButton(button_frame, text="-", command=lambda: insert_text("-"), width=60)
            btn_multiply = ctk.CTkButton(button_frame, text="*", command=lambda: insert_text("*"), width=60)
            btn_divide = ctk.CTkButton(button_frame, text="/", command=lambda: insert_text("/"), width=60)

            btn_add.grid(row=0, column=0, padx=5, pady=5)
            btn_subtract.grid(row=0, column=1, padx=5, pady=5)
            btn_multiply.grid(row=0, column=2, padx=5, pady=5)
            btn_divide.grid(row=0, column=3, padx=5, pady=5)

            # Botones de funciones avanzadas
            btn_sqrt = ctk.CTkButton(button_frame, text="√", command=lambda: insert_text("√("), width=60)
            btn_pow = ctk.CTkButton(button_frame, text="^", command=lambda: insert_text("^"), width=60)
            btn_frac = ctk.CTkButton(button_frame, text="a/b", command=lambda: insert_text("/"), width=60)
            btn_parentheses = ctk.CTkButton(button_frame, text="(", command=lambda: insert_text("("), width=60)
            btn_parentheses_right = ctk.CTkButton(button_frame, text=")", command=lambda: insert_text(")"), width=60)

            btn_sqrt.grid(row=1, column=0, padx=5, pady=5)
            btn_pow.grid(row=1, column=1, padx=5, pady=5)
            btn_frac.grid(row=1, column=2, padx=5, pady=5)
            btn_parentheses.grid(row=1, column=3, padx=5, pady=5)
            btn_parentheses_right.grid(row=1, column=4, padx=5, pady=5)

            # Botones de funciones trigonométricas
            btn_sin = ctk.CTkButton(button_frame, text="sin", command=lambda: insert_text("sin("), width=60)
            btn_cos = ctk.CTkButton(button_frame, text="cos", command=lambda: insert_text("cos("), width=60)
            btn_tan = ctk.CTkButton(button_frame, text="tan", command=lambda: insert_text("tan("), width=60)
            btn_log = ctk.CTkButton(button_frame, text="log", command=lambda: insert_text("log("), width=60)

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

    # Botón para alternar entre modos
    toggle_button = ctk.CTkButton(calc_window, text="Cambiar a Numérico", command=toggle_mode, width=100)
    toggle_button.pack(pady=10)

    # Inicializar botones en el modo "Funciones"
    update_buttons()


import tkinter as tk
from tkinter import messagebox

class Vector:
    def __init__(self, components):
        self.components = components

    def __mul__(self, scalar):
        return Vector([scalar * x for x in self.components])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __add__(self, other):
        return Vector([x + y for x, y in zip(self.components, other.components)])

    def __str__(self):
        return f"v^({', '.join(map(str, self.components))})"

def generate_entries():

    try:
        num_vectors = int(num_vectors_entry.get())
        dim = int(dim_entry.get())
        if dim <= 0 or dim > 10:
            raise ValueError("La dimensión debe estar entre 1 y 10.")
        if num_vectors <= 0 or num_vectors > 10:
            raise ValueError("El número de vectores debe estar entre 1 y 10.")
        
        for widget in vectors_frame.winfo_children():
            widget.destroy()

        global vector_entries, scalar_entries
        vector_entries = []
        scalar_entries = []

        for i in range(num_vectors):
            tk.Label(vectors_frame, text=f"Escalar para el vector {i+1}:", font=("Consolas", 14, "bold")).grid(row=i*2, column=0, sticky="w")
            scalar_entry = tk.Entry(vectors_frame, font=("Consolas", 14))
            scalar_entry.grid(row=i*2, column=1, pady=5)
            scalar_entries.append(scalar_entry)

            tk.Label(vectors_frame, text=f"Componentes del vector {i+1}:", font=("Consolas", 14, "bold")).grid(row=i*2+1, column=0, sticky="w")
            entries = []
            for j in range(dim):
                entry = tk.Entry(vectors_frame, width=5, font=("Consolas", 14))
                entry.grid(row=i*2+1, column=j+1, padx=1, pady=5)
                entries.append(entry)
            vector_entries.append(entries)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def calculate():
    try:
        num_vectors = int(num_vectors_entry.get())
        dim = int(dim_entry.get())

        vectors = []
        for i in range(num_vectors):
            components = [float(vector_entries[i][j].get()) for j in range(dim)]
            vectors.append(Vector(components))

        scalars = [float(scalar_entries[i].get()) for i in range(num_vectors)]

        result_vector = scalars[0] * vectors[0]
        result_details = [f"{scalars[0]} * {vectors[0]} = {result_vector}"]
        for i in range(1, num_vectors):
            scaled_vector = scalars[i] * vectors[i]
            result_vector = result_vector + scaled_vector
            result_details.append(f"{scalars[i]} * {vectors[i]} = {scaled_vector}")

        result_text.set("\n".join(result_details) + f"\nResultado final: {result_vector}")
        result_label.config(font=("Consolas", 16, "bold"))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

app = tk.Tk()
app.title("Calculadora de Vectores")
app.geometry("800x600")
app.resizable(False, False)

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(expand=True)

tk.Label(frame, text="Número de vectores:", font=("Consolas", 14, "bold")).grid(row=0, column=0, sticky="w")
num_vectors_entry = tk.Entry(frame, font=("Consolas", 12))
num_vectors_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Dimensión de los vectores:", font=("Consolas", 14, "bold")).grid(row=1, column=0, sticky="w")
dim_entry = tk.Entry(frame, font=("Consolas", 12))
dim_entry.grid(row=1, column=1, pady=5)

tk.Button(frame, text="Generar", command=generate_entries, font=("Consolas", 14, "bold")).grid(row=1, column=2, padx=10)

vectors_frame = tk.Frame(frame)
vectors_frame.grid(row=2, column=0, columnspan=10, pady=10)

tk.Button(frame, text="Calcular", command=calculate, font=("Consolas", 14, "bold")).grid(row=3, column=0, columnspan=3, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify="left", anchor="w", font=("Consolas", 14, "bold"))
result_label.grid(row=4, column=0, columnspan=10, sticky="w")

app.mainloop()
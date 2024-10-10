from pylatex import Document, Section, Math
from pylatex.utils import NoEscape

# Función para convertir una lista de listas a una cadena LaTeX de matriz
def matriz_a_latex(matriz):
    filas = [" & ".join(map(str, fila)) for fila in matriz]
    return "\\begin{bmatrix} " + " \\\\ ".join(filas) + " \\end{bmatrix}"

def crear_reporte_matrices():
    # Crear el documento LaTeX
    doc = Document(geometry_options={"tmargin": "1cm", "lmargin": "1cm"})
    doc.packages.append(NoEscape(r'\usepackage{amsmath}'))

    # Crear una sección para el reporte
    with doc.create(Section('Registro de Operaciones con Matrices')):
        doc.append('Matriz original:')
        
        # Matriz como lista de listas
        matrix = [[2.0, 3.0], [2.0, 3.0], [24.0, 4.0]]
        
        # Convertir la matriz a formato LaTeX
        matriz_latex = matriz_a_latex(matrix)
        
        # Agregar la matriz LaTeX al documento
        doc.append(Math(data=[NoEscape(matriz_latex)]))

    # Generar el PDF
    doc.generate_pdf('reporte_matrices', clean_tex=False)

crear_reporte_matrices()

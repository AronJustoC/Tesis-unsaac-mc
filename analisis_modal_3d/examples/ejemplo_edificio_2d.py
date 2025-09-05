"""
Ejemplo de Análisis Modal de un Edificio de 3 Pisos en 2D.

Este script modela un pórtico simple de 3 pisos y 1 vano, realiza un
análisis modal para encontrar sus frecuencias y modos de vibración, y
finalmente grafica los primeros modos.
"""

import sys
# Añade la ruta del proyecto al path para poder importar los módulos
sys.path.append(sys.path[0].replace('\\analisis_modal_3d\\examples', ''))

from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.visualization.plotter import plot_mode_shape
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info

def ejemplo_edificio_portico_2d():
    """
    Define y analiza un pórtico 2D de 3 pisos.
    """
    print("Iniciando ejemplo: Edificio de 3 pisos en 2D")
    
    # 1. Inicializar la estructura
    structure = Structure()

    # 2. Definir materiales y secciones
    # Se define un material único para toda la estructura (Acero)
    materials = {
        "acero": {
            "E": 200e9,  # Módulo de elasticidad (Pa)
            "G": 77e9,   # Módulo de corte (Pa)
            "rho": 7850, # Densidad (kg/m³)
        }
    }

    # Se definen secciones para columnas y vigas
    sections = {
        "columna_30x30": {
            "area": 0.3 * 0.3,
            "Ix": (1/12) * 0.3 * 0.3**3,  # Inercia torsional
            "Iy": (1/12) * 0.3 * 0.3**3,  # Inercia respecto a Y
            "Iz": (1/12) * 0.3 * 0.3**3,  # Inercia respecto a Z
        },
        "viga_40x20": {
            "area": 0.4 * 0.2,
            "Ix": 0.0001, # Valor aproximado para inercia torsional
            "Iy": (1/12) * 0.2 * 0.4**3,
            "Iz": (1/12) * 0.4 * 0.2**3,
        },
    }

    # 3. Definir la geometría del pórtico (nodos)
    # El pórtico estará en el plano XZ (Y=0)
    # Ancho del vano: 5 metros
    # Altura de cada piso: 3 metros
    
    # Nivel 0 (Base)
    n1 = structure.add_node(0, 0, 0)
    n2 = structure.add_node(5, 0, 0)
    
    # Nivel 1
    n3 = structure.add_node(0, 0, 3)
    n4 = structure.add_node(5, 0, 3)

    # Nivel 2
    n5 = structure.add_node(0, 0, 6)
    n6 = structure.add_node(5, 0, 6)

    # Nivel 3
    n7 = structure.add_node(0, 0, 9)
    n8 = structure.add_node(5, 0, 9)

    # 4. Definir los elementos estructurales (columnas y vigas)
    
    # Columnas
    structure.add_element(n1, n3, sections["columna_30x30"], materials["acero"])
    structure.add_element(n2, n4, sections["columna_30x30"], materials["acero"])
    structure.add_element(n3, n5, sections["columna_30x30"], materials["acero"])
    structure.add_element(n4, n6, sections["columna_30x30"], materials["acero"])
    structure.add_element(n5, n7, sections["columna_30x30"], materials["acero"])
    structure.add_element(n6, n8, sections["columna_30x30"], materials["acero"])

    # Vigas
    structure.add_element(n3, n4, sections["viga_40x20"], materials["acero"])
    structure.add_element(n5, n6, sections["viga_40x20"], materials["acero"])
    structure.add_element(n7, n8, sections["viga_40x20"], materials["acero"])

    # 5. Aplicar restricciones
    
    # Empotramiento en la base (nodos 1 y 2)
    structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n2, ["ux", "uy", "uz", "rx", "ry", "rz"])

    # Restricción para comportamiento 2D en el plano XZ
    # Se restringen los desplazamientos y giros fuera del plano para todos los nodos
    for node in structure.nodes:
        # Si el nodo no está en la base, aplicamos restricciones 2D
        if node.id not in [n1.id, n2.id]:
             structure.add_constraint(node, ["uy", "rx", "rz"])

    # 6. Visualizar la estructura definida
    print("Mostrando la estructura definida...")
    plot_structure_with_info(structure, title="Edificio de 3 Pisos (Pórtico 2D)")

    # 7. Realizar el análisis modal
    print("\nIniciando análisis modal...")
    try:
        # Se piden los primeros 5 modos de vibración
        num_modes = 5
        freqs, modes = modal_analysis(structure, num_modes=num_modes)

        print("\nFrecuencias Naturales (Hz):")
        print("-" * 25)
        for i, freq in enumerate(freqs):
            print(f"  Modo {i+1}: {freq:.2f} Hz")
        print("-" * 25)

        # 8. Visualizar los modos de vibración
        print(f"\nMostrando los primeros {num_modes} modos de vibración...")
        for i in range(num_modes):
            plot_mode_shape(
                structure,
                modes[:, i],
                title=f"Modo {i+1} ({freqs[i]:.2f} Hz)",
                deformation_scale=0.5 # Factor de escala para la deformada
            )

    except Exception as e:
        print(f"\nOcurrió un error durante el análisis: {e}")

if __name__ == "__main__":
    ejemplo_edificio_portico_2d()

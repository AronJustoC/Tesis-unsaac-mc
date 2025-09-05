"""
Ejemplo de Análisis Modal de un Edificio de 3 Pisos en 2D.

Este script modela un pórtico simple de 3 pisos y 1 vano, realiza un
análisis modal para encontrar sus frecuencias y modos de vibración, y
finalmente grafica los primeros modos.
"""

# Importaciones necesarias
from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.visualization.plotter import plot_mode_shape
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info
from analisis_modal_3d.analysis.assembler import assemble_global_matrices # NUEVA IMPORTACIÓN

# Variables globales para almacenar los resultados (serán pobladas por la llamada a la función)
structure = None
freqs = None
modes = None

def ejemplo_edificio_portico_2d():
    """
    Define y analiza un pórtico 2D de 3 pisos.
    """
    print("Iniciando ejemplo: Edificio de 3 pisos en 2D")
    
    # 1. Inicializar la estructura
    local_structure = Structure()

    # 2. Definir materiales y secciones
    materials = {
        "acero": {
            "E": 200e9,  # Módulo de elasticidad (Pa)
            "G": 77e9,   # Módulo de corte (Pa)
            "rho": 7850, # Densidad (kg/m³)
        }
    }

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
    n1 = local_structure.add_node(0, 0, 0)
    n2 = local_structure.add_node(5, 0, 0)
    
    # Nivel 1
    n3 = local_structure.add_node(0, 0, 3)
    n4 = local_structure.add_node(5, 0, 3)

    # Nivel 2
    n5 = local_structure.add_node(0, 0, 6)
    n6 = local_structure.add_node(5, 0, 6)

    # Nivel 3
    n7 = local_structure.add_node(0, 0, 9)
    n8 = local_structure.add_node(5, 0, 9)

    # 4. Definir los elementos estructurales (columnas y vigas)
    
    # Columnas
    local_structure.add_element(n1, n3, sections["columna_30x30"], materials["acero"])
    local_structure.add_element(n2, n4, sections["columna_30x30"], materials["acero"])
    local_structure.add_element(n3, n5, sections["columna_30x30"], materials["acero"])
    local_structure.add_element(n4, n6, sections["columna_30x30"], materials["acero"])
    local_structure.add_element(n5, n7, sections["columna_30x30"], materials["acero"])
    local_structure.add_element(n6, n8, sections["columna_30x30"], materials["acero"])

    # Vigas
    local_structure.add_element(n3, n4, sections["viga_40x20"], materials["acero"])
    local_structure.add_element(n5, n6, sections["viga_40x20"], materials["acero"])
    local_structure.add_element(n7, n8, sections["viga_40x20"], materials["acero"])

    # 5. APLICAR restricciones
    
    # Empotramiento en la base (nodos 1 y 2)
    local_structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])
    local_structure.add_constraint(n2, ["ux", "uy", "uz", "rx", "ry", "rz"])

    # Restricción para comportamiento 2D en el plano XZ
    # Se restringen los desplazamientos y giros fuera del plano para todos los nodos
    for node in local_structure.nodes:
        # Si el nodo no está en la base, aplicamos restricciones 2D
        if node.id not in [n1.id, n2.id]:
             local_structure.add_constraint(node, ["uy", "rx", "rz"])

    # 6. Visualizar la estructura definida
    print("Mostrando la estructura definida...")
    plot_structure_with_info(local_structure, title="Edificio de 3 Pisos (Pórtico 2D)")

    # 7. Realizar el análisis modal
    print("\nIniciando análisis modal...")
    try:
        # Ensamblar matrices globales de rigidez y masa
        K, M = assemble_global_matrices(local_structure) # NUEVA LÍNEA

        # Se piden los primeros 5 modos de vibración
        num_modes = 5
        # Pasar K y M a modal_analysis
        local_freqs, local_modes = modal_analysis(K, M, local_structure, num_modes=num_modes) # LÍNEA MODIFICADA

        print("\nFrecuencias Naturales (Hz):")
        print("-" * 25)
        for i, freq in enumerate(local_freqs):
            print(f"  Modo {i+1}: {freq:.2f} Hz")
        print("-" * 25)

        # 8. Visualizar los modos de vibración
        print(f"\nMostrando los primeros {num_modes} modos de vibración...")
        for i in range(num_modes):
            plot_mode_shape(
                local_structure,
                local_modes[:, i],
                title=f"Modo {i+1} ({local_freqs[i]:.2f} Hz)",
                deformation_scale=0.5 # Factor de escala para la deformada
            )
        
        return local_structure, local_freqs, local_modes

    except Exception as e:
        print(f"\nOcurrió un error durante el análisis: {e}")
        return None, None, None

# Llama a la función directamente a nivel de módulo para poblar las variables globales
_structure, _freqs, _modes = ejemplo_edificio_portico_2d()
structure = _structure
freqs = _freqs
modes = _modes

if __name__ == "__main__":
    # Este bloque se ejecuta solo si el script se corre directamente
    if structure is not None and freqs is not None and modes is not None:
        print("\nEjemplo vacio.py ejecutado exitosamente. Variables globales (structure, freqs, modes) pobladas.")
    else:
        print("\nEjemplo vacio.py ejecutado, pero las variables globales no se poblaron correctamente.")

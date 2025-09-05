import numpy as np
from analisis_modal_3d.analysis import modal_analysis
from analisis_modal_3d.structures import Structure
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
from analisis_modal_3d.visualization.plotter import plot_mode_shape
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info

# Global variables to store results
structure = None
freqs = None
modes = None
harmonic_displacement_history = None # Not used in this example, but kept for consistency

def run_example():
    global structure, freqs, modes, harmonic_displacement_history

    # Inicializar structure
    structure = Structure()

    # ==============================================================================
    # Geometría avanzada del puente
    # ==============================================================================
    # Parámetros principales
    main_span = 400  # metros (luz principal)
    back_span = 200  # metros (luz trasera)
    tower_height = 150  # metros (altura de pilonos)
    deck_width = 35  # metros (ancho del tablero)
    n_cables = 20  # número de tirantes por lado

    # ==============================================================================
    # Nodos del tablero (coordenadas X,Y,Z)
    # ==============================================================================
    # Nodos principales del tablero
    deck_nodes = []
    for x in np.linspace(-back_span, main_span, 100):
        deck_nodes.append(structure.add_node(x, 0, 0))

    # Nodos laterales para rigidez torsional
    for i, n in enumerate(deck_nodes):
        structure.add_node(n.x, deck_width / 2, 0)
        structure.add_node(n.x, -deck_width / 2, 0)

    # ==============================================================================
    # Pilones principales
    # ==============================================================================
    # Geometría de pilones en forma de diamante
    tower_nodes = []
    for z in np.linspace(0, tower_height, 20):
        # Sección transversal variable con la altura
        y_width = deck_width * (1 - z / tower_height) + 5
        tower_nodes.extend(
            [
                structure.add_node(main_span / 2, y_width, z),
                structure.add_node(main_span / 2, -y_width, z),
            ]
        )

    # ==============================================================================
    # Tirantes
    # ==============================================================================
    cable_anchors = []
    for i in range(n_cables):
        x_pos = main_span * (i + 1) / (n_cables + 1)
        cable_anchors.extend(
            [
                structure.add_node(x_pos, deck_width / 2, 0),
                structure.add_node(x_pos, -deck_width / 2, 0),
            ]
        )

    # ==============================================================================
    # Propiedades de materiales
    # ==============================================================================
    materials = {
        "deck_concrete": {"E": 35e9, "G": 15e9, "rho": 2500, "nu": 0.2},
        "tower_steel": {"E": 210e9, "G": 80e9, "rho": 7850, "nu": 0.3},
        "cables": {
            "E": 200e9,
            "G": 80e9,
            "rho": 8500,
            "nu": 0.3,
            "pretension": 500e3,  # Pretensado inicial (N)
        },
    }

    # ==============================================================================
    # Propiedades de secciones
    # ==============================================================================
    sections = {
        "deck": {
            "type": "box_girder",
            "A": 12.5,  # m²
            "Ix": 85.2,  # m⁴
            "Iy": 320.5,  # m⁴
            "Iz": 1500.8,  # m⁴
            "t_web": 0.4,  # m
            "t_flange": 0.6,  # m
        },
        "tower": {
            "type": "I-section",
            "A": 8.2,
            "Ix": 45.3,
            "Iy": 120.7,
            "Iz": 650.4,
            "tf": 0.08,
            "tw": 0.05,
        },
        "cable": {
            "type": "circular",
            "diameter": 0.15,  # m
            "A": np.pi * (0.15 / 2) ** 2,
            "Ix": 1e-4,
            "Iy": 1e-4,
            "Iz": 1e-4,
        },
    }

    # ==============================================================================
    # Creación de elementos
    # ==============================================================================
    # Elementos del tablero (sección cajón multicelular)
    for i in range(len(deck_nodes) - 1):
        structure.add_element(
            deck_nodes[i],
            deck_nodes[i + 1],
            sections["deck"],
            materials["deck_concrete"],
        )

    # Elementos de los pilones (acero de alta resistencia)
    for i in range(len(tower_nodes) - 1):
        structure.add_element(
            tower_nodes[i],
            tower_nodes[i + 1],
            sections["tower"],
            materials["tower_steel"],
        )

    # Tirantes (elementos de cable pretensado)
    for i in range(n_cables):
        top_node = tower_nodes[-2 if i % 2 == 0 else -1]  # Alternar entre torres
        structure.add_element(
            cable_anchors[2 * i],
            top_node,
            sections["cable"],
            materials["cables"],
            element_type="cable",
        )

    # ==============================================================================
    # Restricciones y condiciones de apoyo
    # ==============================================================================
    # Apoyos del tablero
    structure.add_constraint(deck_nodes[0], ["uy", "uz", "rx", "ry", "rz"])  # Fijo
    structure.add_constraint(deck_nodes[-1], ["uz", "rx", "ry", "rz"])  # Móvil

    # Base de los pilones
    for node in tower_nodes[:4]:
        structure.add_constraint(node, ["ux", "uy", "uz", "rx", "ry", "rz"])

    # Plot the structure with info
    plot_structure_with_info(structure, title="Estructura de Puente Atirantado")

    # ==============================================================================
    # Análisis modal
    # ==============================================================================
    try:
        K_global, M_global = assemble_global_matrices(structure)
        freqs, modes = modal_analysis(
            K_global, M_global, structure,
            num_modes=10,
            mass_matrix_type="consistent",
            solver_options={"max_iter": 1000, "tolerance": 1e-8},
        )

        # Resultados
        print("\nModos de Vibración del Puente Atirantado:")
        print("-" * 45)
        for i, freq in enumerate(freqs[:5], 1):
            print(f"Modo {i}: {freq:.2f} Hz")

        # Visualización 3D
        for i in range(min(len(freqs), 3)): # Plot first 3 modes for brevity
            plot_mode_shape(
                structure,
                modes[:, i],
                title=f"Modo {i+1} - {freqs[i]:.2f} Hz",
                deformation_scale=50,
                view_angle=("isometric"),
            )

    except Exception as e:
        print(f"Error en el análisis: {e}")

# Call run_example directly when the module is imported
run_example()

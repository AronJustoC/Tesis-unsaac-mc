from src.structures import Structure
from src.analysis import modal_analysis
from src.visualization import plot_mode_shape
import numpy as np


def create_complex_bridge():
    # Inicializar estructura
    bridge = Structure()

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
        deck_nodes.append(bridge.add_node(x, 0, 0))

    # Nodos laterales para rigidez torsional
    for i, n in enumerate(deck_nodes):
        bridge.add_node(n.x, deck_width / 2, 0)
        bridge.add_node(n.x, -deck_width / 2, 0)

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
                bridge.add_node(main_span / 2, y_width, z),
                bridge.add_node(main_span / 2, -y_width, z),
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
                bridge.add_node(x_pos, deck_width / 2, 0),
                bridge.add_node(x_pos, -deck_width / 2, 0),
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
        bridge.add_element(
            deck_nodes[i],
            deck_nodes[i + 1],
            sections["deck"],
            materials["deck_concrete"],
        )

    # Elementos de los pilones (acero de alta resistencia)
    for i in range(len(tower_nodes) - 1):
        bridge.add_element(
            tower_nodes[i],
            tower_nodes[i + 1],
            sections["tower"],
            materials["tower_steel"],
        )

    # Tirantes (elementos de cable pretensado)
    for i in range(n_cables):
        top_node = tower_nodes[-2 if i % 2 == 0 else -1]  # Alternar entre torres
        bridge.add_element(
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
    bridge.add_constraint(deck_nodes[0], ["uy", "uz", "rx", "ry", "rz"])  # Fijo
    bridge.add_constraint(deck_nodes[-1], ["uz", "rx", "ry", "rz"])  # Móvil

    # Base de los pilones
    for node in tower_nodes[:4]:
        bridge.add_constraint(node, ["ux", "uy", "uz", "rx", "ry", "rz"])

    # ==============================================================================
    # Análisis modal
    # ==============================================================================
    try:
        constrained_dofs = bridge.get_constrained_dofs()
        freqs, modes = modal_analysis(
            bridge,
            num_modes=10,
            constrained_dofs=constrained_dofs,
            mass_matrix_type="consistent",
            solver_options={"max_iter": 1000, "tolerance": 1e-8},
        )

        # Resultados
        print("\nModos de Vibración del Puente Atirantado:")
        print("-" * 45)
        for i, freq in enumerate(freqs[:5], 1):
            print(f"Modo {i}: {freq:.2f} Hz")

        # Visualización 3D
        plot_mode_shape(
            bridge,
            modes[:, 0],
            title=f"Modo Fundamental - {freqs[0]:.2f} Hz",
            deformation_scale=50,
            view_angle=("isometric"),
        )

    except Exception as e:
        print(f"Error en el análisis: {e}")


if __name__ == "__main__":
    create_complex_bridge()

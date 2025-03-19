from src.structures import Structure
from src.analysis import modal_analysis
from src.visualization import plot_mode_shape
from src.visualization import plot_structure
import numpy as np


def main():
    structure = Structure()

    # ========== Definir propiedades de materiales ==========
    materials = {
        "ASTM-A36": {
            "E": 200e9,  # Módulo de elasticidad (Pa)
            "G": 77e9,  # Módulo de corte (Pa)
            "rho": 7850,  # Densidad (kg/m³)
        }
    }

    # ========== Definir propiedades de secciones ==========
    sections = {
        "80x40": {
            "area": 0.08 * 0.04,  # 3200 mm²
            "Ix": 2133333.34e-12,  # Torsion constant
            "Iy": 426666.67e-12,  # Moment of inertia about y-axis
            "Iz": 1706666.67e-12,  # Moment of inertia about z-axis
        },
        "100x80": {
            "area": 0.10 * 0.08,  # 8000 mm²
            "Ix": 10933333.34e-12,  # Torsion constant
            "Iy": 6666666.67e-12,  # Moment of inertia about y-axis
            "Iz": 4266666.67e-12,  # Moment of inertia about z-axis
        },
        "80x80": {
            "area": 0.08 * 0.08,  # 6400 mm²
            "Ix": 6826666.66e-12,  # Torsion constant
            "Iy": 3413333.33e-12,  # Moment of inertia about y-axis
            "Iz": 3413333.33e-12,  # Moment of inertia about z-axis
        },
        "H420x180": {  # H-section
            "area": 0.42 * 0.02 + 2 * 0.18 * 0.02,  # Web + 2 Flanges
            "Ix": 399386666.66e-12,  # Torsion constant
            "Iy": 379693333.33e-12,  # Major axis moment of inertia
            "Iz": 19693333.33e-12,  # Minor axis moment of inertia
        },
    }

    # ========== Agregar nodos ==========
    node_coords = {}
    for row in [
        # ID: (x, y, z) en metros (convertidos de mm)
        (1, 0, 0, 0),
        (2, 0, 0, 1100),
        (3, 0, 0, 2200),
        (4, 762.5, 0, 0),
        (5, 762.5, 0, 2200),
        (6, 1525, 0, 0),
        (7, 1525, 0, 1100),
        (8, 1525, 0, 2200),
        (9, 2287.5, 0, 0),
        (10, 2287.5, 0, 2200),
        (11, 3050, 0, 0),
        (12, 3050, 0, 1100),
        (13, 3050, 0, 2200),
        (14, 0, -700, 0),  # (74, 0, -700, 0),
        (15, 3050, -700, 0),  # (75, 3050, -700, 0),
        (16, 0, 5000, 0),  # (82, 0, 5000, 0),
        (17, 0, 5000, 1100),  # (83, 0, 5000, 1100),
        (18, 0, 5000, 2200),  # (84, 0, 5000, 2200),
        (19, 762.5, 5000, 0),  # (85, 762.5, 5000, 0),
        (20, 762.5, 5000, 2200),  # (86, 762.5, 5000, 2200),
        (21, 1525, 5000, 0),  # (87, 1525, 5000, 0),
        (22, 1525, 5000, 1100),  # (88, 1525, 5000, 1100),
        (23, 1525, 5000, 2200),  # (89, 1525, 5000, 2200),
        (24, 2287.5, 5000, 0),  # (90, 2287.5, 5000, 0),
        (25, 2287.5, 5000, 2200),  # (91, 2287.5, 5000, 2200),
        (26, 3050, 5000, 0),  # (92, 3050, 5000, 0),
        (27, 3050, 5000, 1100),  # (93, 3050, 5000, 1100),
        (28, 3050, 5000, 2200),  # (94, 3050, 5000, 2200),
        (29, 0, 5700, 0),  # (155, 0, 5700, 0),
        (30, 3050, 5700, 0),  # (156, 3050, 5700, 0),
    ]:
        node_id = row[0]
        coords = (row[1] / 1000, row[2] / 1000, row[3] / 1000)  # Conversión mm -> m
        node_coords[node_id] = structure.add_node(*coords)

    # ========== Agregar elementos ==========
    elements = [
        # (nodo_inicial, nodo_final, sección, material)
        (1, 2, "80x40", "ASTM-A36"),
        (2, 3, "80x40", "ASTM-A36"),
        (1, 4, "100x80", "ASTM-A36"),
        (2, 4, "80x40", "ASTM-A36"),
        (2, 5, "80x40", "ASTM-A36"),
        (3, 5, "100x80", "ASTM-A36"),
        (4, 6, "100x80", "ASTM-A36"),
        (4, 7, "80x40", "ASTM-A36"),
        (5, 7, "80x40", "ASTM-A36"),
        (5, 8, "100x80", "ASTM-A36"),
        (6, 7, "80x40", "ASTM-A36"),
        (7, 8, "80x40", "ASTM-A36"),
        (6, 9, "100x80", "ASTM-A36"),
        (7, 9, "80x40", "ASTM-A36"),
        (7, 10, "80x40", "ASTM-A36"),
        (8, 10, "100x80", "ASTM-A36"),
        (9, 11, "100x80", "ASTM-A36"),
        (9, 12, "80x40", "ASTM-A36"),
        (10, 12, "80x40", "ASTM-A36"),
        (10, 13, "100x80", "ASTM-A36"),
        (11, 12, "80x80", "ASTM-A36"),
        (12, 13, "80x80", "ASTM-A36"),
        (1, 14, "H420x180", "ASTM-A36"),
        (14, 3, "80x40", "ASTM-A36"),
        (11, 15, "H420x180", "ASTM-A36"),
        (15, 13, "80x40", "ASTM-A36"),
        ##########
        (16, 17, "80x40", "ASTM-A36"),
        (17, 18, "80x40", "ASTM-A36"),
        (16, 19, "100x80", "ASTM-A36"),
        (17, 19, "80x40", "ASTM-A36"),
        (17, 20, "80x40", "ASTM-A36"),
        (18, 20, "100x80", "ASTM-A36"),
        (19, 21, "100x80", "ASTM-A36"),
        (19, 22, "80x40", "ASTM-A36"),
        (20, 22, "80x40", "ASTM-A36"),
        (20, 23, "100x80", "ASTM-A36"),
        (21, 22, "80x40", "ASTM-A36"),
        (22, 23, "80x40", "ASTM-A36"),
        (21, 24, "100x80", "ASTM-A36"),
        (22, 24, "80x40", "ASTM-A36"),
        (22, 25, "80x40", "ASTM-A36"),
        (23, 25, "100x80", "ASTM-A36"),
        (24, 26, "100x80", "ASTM-A36"),
        (24, 27, "80x40", "ASTM-A36"),
        (25, 27, "80x40", "ASTM-A36"),
        (25, 28, "100x80", "ASTM-A36"),
        (26, 27, "80x80", "ASTM-A36"),
        (27, 28, "80x80", "ASTM-A36"),
        (16, 29, "H420x180", "ASTM-A36"),
        (29, 18, "80x40", "ASTM-A36"),
        (26, 30, "H420x180", "ASTM-A36"),
        (30, 28, "80x40", "ASTM-A36"),
        (1, 16, "H420x180", "ASTM-A36"),
        (1, 26, "80x40", "ASTM-A36"),
        (11, 16, "80x40", "ASTM-A36"),
        (11, 26, "H420x180", "ASTM-A36"),
    ]

    for el in elements:
        structure.add_element(
            node_coords[el[0]], node_coords[el[1]], sections[el[2]], materials[el[3]]
        )

    # ========== Aplicar restricciones ==========
    constraints = {
        1: [
            "ux",
            "uy",
            "uz",
            "rx",
            "ry",
            "rz",
        ],  # Nodo 1 (ID: 1) debe tener las componentes ux, uy, uz, rx, ry, rz
        16: [
            "ux",
            "uy",
            "uz",
            "rx",
            "ry",
            "rz",
        ],  # Nodo 15 (ID: 15) debe tener las componentes ux, uy, uz, rx, ry, rz
        11: [
            "uy",
            "uz",
            "rx",
            "ry",
            "rz",
        ],  # Nodo 10 (ID: 10) debe tener las componentes ux, uy, uz, rx, ry, rz
        26: [
            "uy",
            "uz",
            "rx",
            "ry",
            "rz",
        ],  # Nodo 25 (ID: 25) debe tener las componentes uy, uz, rx, ry, rz
    }

    for node_id, dofs in constraints.items():
        structure.add_constraint(node_coords[node_id], dofs)
    # Graficar estructura
    plot_structure(structure)

    # ========== Análisis Modal con parámetros robustos ==========
    try:
        constrained_dofs = structure.get_constrained_dofs()
        # Usar shift-invert para evitar matrices singulares
        freqs, modes = modal_analysis(
            structure,
            num_modes=10,
            constrained_dofs=constrained_dofs,
        )
        print("\nNatural Frequencies:")
        print("-" * 30)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # Visualizar los modos
        for i in range(len(freqs)):
            plot_mode_shape(
                structure,
                modes[:, i],
                title=f"Modo {i + 1} - {freqs[i]:.2f} Hz",
                deformation_scale=5,
            )

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")


if __name__ == "__main__":
    main()

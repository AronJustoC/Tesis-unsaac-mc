from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.structures.structure import Structure
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

    structure = Structure()

    # ========== Definir propiedades de materiales ==========
    materials = {
        "ASTM-A36": {
            "E": 200e9,  # Módulo de elasticidad (Pa)
            "G": 77e9,  # Módulo de corte (Pa)
            "rho": 7850,  # Densidad (kg/m³)
        },
        "ASTM-A36+": {
            "E": 200e9,  # Módulo de elasticidad (Pa)
            "G": 77e9,  # Módulo de corte (Pa)
            "rho": 7850 * 6,  # Densidad (kg/m³)
        },
    }

    # ========== Definir propiedades de secciones escla real ==========
    sections = {
        "80x40": {
            "area": (0.008 * 0.004),  # 32 mm²
            "Ix": 2133333.34e-12 / 10000,  # Torsion constant
            "Iy": 426666.67e-12 / 10000,  # Moment of inertia about y-axis
            "Iz": 1706666.67e-12 / 10000,  # Moment of inertia about z-axis
        },
        "100x80": {
            "area": (0.010 * 0.008),  # 80 mm²
            "Ix": 10933333.34e-12 / 10000,  # Torsion constant
            "Iy": 6666666.67e-12 / 10000,  # Moment of inertia about y-axis
            "Iz": 4266666.67e-12 / 10000,  # Moment of inertia about z-axis
        },
        "80x80": {
            "area": (0.008 * 0.008),  # 64 mm²
            "Ix": 6826666.66e-12 / 10000,  # Torsion constant
            "Iy": 3413333.33e-12 / 10000,  # Moment of inertia about y-axis
            "Iz": 3413333.33e-12 / 10000,  # Moment of inertia about z-axis
        },
        "H420x180": {  # H-section
            "area": (0.042 * 0.002 + 2 * 0.018 * 0.002),  # Web + 2 Flanges
            "Ix": 399386666.66e-12 / 10000,  # Torsion constant
            "Iy": 379693333.33e-12 / 10000,  # Major axis moment of inertia
            "Iz": 19693333.33e-12 / 10000,  # Minor axis moment of inertia
        },
    }

    # ========== Agregar nodos ==========
    node_coords = {}
    for row in [
        # ID: (x, y, z) en metros (convertidos de mm)
        (1, 0, 0, 0),
        (2, 0, 0, 110),
        (3, 0, 0, 220),
        (4, 76.25, 0, 0),
        (5, 76.25, 0, 220),
        (6, 152.5, 0, 0),
        (7, 152.5, 0, 110),
        (8, 152.5, 0, 220),
        (9, 228.75, 0, 0),
        (10, 228.75, 0, 220),
        (11, 305, 0, 0),
        (12, 305, 0, 110),
        (13, 305, 0, 220),
        (14, 381.25, 0, 0),
        (15, 381.25, 0, 220),
        (16, 457.5, 0, 0),
        (17, 457.5, 0, 110),
        (18, 457.5, 0, 220),
        (19, 533.75, 0, 0),
        (20, 533.75, 0, 220),
        (21, 610, 0, 0),
        (22, 610, 0, 110),
        (23, 610, 0, 220),
        (24, 686.25, 0, 0),
        (25, 686.25, 0, 220),
        (26, 762.5, 0, 0),
        (27, 762.5, 0, 110),
        (28, 762.5, 0, 220),
        (29, 838.75, 0, 0),
        (30, 838.75, 0, 220),
        (31, 915, 0, 0),
        (32, 915, 0, 110),
        (33, 915, 0, 220),
        (34, 991.25, 0, 0),
        (35, 991.25, 0, 220),
        (36, 1067.5, 0, 0),
        (37, 1067.5, 0, 110),
        (38, 1067.5, 0, 220),
        (39, 1143.75, 0, 0),
        (40, 1143.75, 0, 220),
        (41, 1220, 0, 0),
        (42, 1220, 0, 110),
        (43, 1220, 0, 220),
        (44, 1296.25, 0, 0),
        (45, 1296.25, 0, 220),
        (46, 1372.5, 0, 0),
        (47, 1372.5, 0, 110),
        (48, 1372.5, 0, 220),
        (49, 1448.75, 0, 0),
        (50, 1448.75, 0, 220),
        (51, 1525, 0, 0),
        (52, 1525, 0, 110),
        (53, 1525, 0, 220),
        (54, 1601.25, 0, 0),
        (55, 1601.25, 0, 220),
        (56, 1677.5, 0, 0),
        (57, 1677.5, 0, 110),
        (58, 1677.5, 0, 220),
        (59, 1753.75, 0, 0),
        (60, 1753.75, 0, 220),
        (61, 1830, 0, 0),
        (62, 1830, 0, 110),
        (63, 1830, 0, 220),
        (64, 1906.25, 0, 0),
        (65, 1906.25, 0, 220),
        (66, 1982.5, 0, 0),
        (67, 1982.5, 0, 110),
        (68, 1982.5, 0, 220),
        (69, 2058.75, 0, 0),
        (70, 2058.75, 0, 220),
        (71, 2135, 0, 0),
        (72, 2135, 0, 110),
        (73, 2135, 0, 220),
        (74, 0, -70, 0),
        (75, 305, -70, 0),
        (76, 610, -70, 0),
        (77, 915, -70, 0),
        (78, 1220, -70, 0),
        (79, 1525, -70, 0),
        (80, 1830, -70, 0),
        (81, 2135, -70, 0),
        (82, 0, 500, 0),
        (83, 0, 500, 110),
        (84, 0, 500, 220),
        (85, 76.25, 500, 0),
        (86, 76.25, 500, 220),
        (87, 152.5, 500, 0),
        (88, 152.5, 500, 110),
        (89, 152.5, 500, 220),
        (90, 228.75, 500, 0),
        (91, 228.75, 500, 220),
        (92, 305, 500, 0),
        (93, 305, 500, 110),
        (94, 305, 500, 220),
        (95, 381.25, 500, 0),
        (96, 381.25, 500, 220),
        (97, 457.5, 500, 0),
        (98, 457.5, 500, 110),
        (99, 457.5, 500, 220),
        (100, 533.75, 500, 0),
        (101, 533.75, 500, 220),
        (102, 610, 500, 0),
        (103, 610, 500, 110),
        (104, 610, 500, 220),
        (105, 686.25, 500, 0),
        (106, 686.25, 500, 220),
        (107, 762.5, 500, 0),
        (108, 762.5, 500, 110),
        (109, 762.5, 500, 220),
        (110, 838.75, 500, 0),
        (111, 838.75, 500, 220),
        (112, 915, 500, 0),
        (113, 915, 500, 110),
        (114, 915, 500, 220),
        (115, 991.25, 500, 0),
        (116, 991.25, 500, 220),
        (117, 1067.5, 500, 0),
        (118, 1067.5, 500, 110),
        (119, 1067.5, 500, 220),
        (120, 1143.75, 500, 0),
        (121, 1143.75, 500, 220),
        (122, 1220, 500, 0),
        (123, 1220, 500, 110),
        (124, 1220, 500, 220),
        (125, 1296.25, 500, 0),
        (126, 1296.25, 500, 220),
        (127, 1372.5, 500, 0),
        (128, 1372.5, 500, 110),
        (129, 1372.5, 500, 220),
        (130, 1448.75, 500, 0),
        (131, 1448.75, 500, 220),
        (132, 1525, 500, 0),
        (133, 1525, 500, 110),
        (134, 1525, 500, 220),
        (135, 1601.25, 500, 0),
        (136, 1601.25, 500, 220),
        (137, 1677.5, 500, 0),
        (138, 1677.5, 500, 110),
        (139, 1677.5, 500, 220),
        (140, 1753.75, 500, 0),
        (141, 1753.75, 500, 220),
        (142, 1830, 500, 0),
        (143, 1830, 500, 110),
        (144, 1830, 500, 220),
        (145, 1906.25, 500, 0),
        (146, 1906.25, 500, 220),
        (147, 1982.5, 500, 0),
        (148, 1982.5, 500, 110),
        (149, 1982.5, 500, 220),
        (150, 2058.75, 500, 0),
        (151, 2058.75, 500, 220),
        (152, 2135, 500, 0),
        (153, 2135, 500, 110),
        (154, 2135, 500, 220),
        (155, 0, 570, 0),
        (156, 305, 570, 0),
        (157, 610, 570, 0),
        (158, 915, 570, 0),
        (159, 1220, 570, 0),
        (160, 1525, 570, 0),
        (161, 1830, 570, 0),
        (162, 2135, 570, 0),
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

    # Plot the structure with info
    plot_structure_with_info(structure, title="Estructura de una Sección Bailey")

    # ========== Análisis Modal con parámetros robustos ==========
    try:
        K_global, M_global = assemble_global_matrices(structure)
        freqs, modes = modal_analysis(
            K_global, M_global, structure, num_modes=10
        )
        print("\nFrequencias Naturales:")
        print("-" * 30)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # Visualizar los modos
        for i in range(min(len(freqs), 3)): # Plot first 3 modes for brevity
            plot_mode_shape(
                structure,
                modes[:, i],
                title=f"Modo {i + 1} - {freqs[i]:.2f} Hz",
                deformation_scale=5,
            )

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

# Call run_example directly when the module is imported
run_example()
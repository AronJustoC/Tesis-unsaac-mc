from analisis_modal_3d.analysis.modal import modal_analysis
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
        (14, 3812.5, 0, 0),
        (15, 3812.5, 0, 2200),
        (16, 4575, 0, 0),
        (17, 4575, 0, 1100),
        (18, 4575, 0, 2200),
        (19, 5337.5, 0, 0),
        (20, 5337.5, 0, 2200),
        (21, 6100, 0, 0),
        (22, 6100, 0, 1100),
        (23, 6100, 0, 2200),
        (24, 6862.5, 0, 0),
        (25, 6862.5, 0, 2200),
        (26, 7625, 0, 0),
        (27, 7625, 0, 1100),
        (28, 7625, 0, 2200),
        (29, 8387.5, 0, 0),
        (30, 8387.5, 0, 2200),
        (31, 9150, 0, 0),
        (32, 9150, 0, 1100),
        (33, 9150, 0, 2200),
        (34, 9912.5, 0, 0),
        (35, 9912.5, 0, 2200),
        (36, 10675, 0, 0),
        (37, 10675, 0, 1100),
        (38, 10675, 0, 2200),
        (39, 11437.5, 0, 0),
        (40, 11437.5, 0, 2200),
        (41, 12200, 0, 0),
        (42, 12200, 0, 1100),
        (43, 12200, 0, 2200),
        (44, 12962.5, 0, 0),
        (45, 12962.5, 0, 2200),
        (46, 13725, 0, 0),
        (47, 13725, 0, 1100),
        (48, 13725, 0, 2200),
        (49, 14487.5, 0, 0),
        (50, 14487.5, 0, 2200),
        (51, 15250, 0, 0),
        (52, 15250, 0, 1100),
        (53, 15250, 0, 2200),
        (54, 16012.5, 0, 0),
        (55, 16012.5, 0, 2200),
        (56, 16775, 0, 0),
        (57, 16775, 0, 1100),
        (58, 16775, 0, 2200),
        (59, 17537.5, 0, 0),
        (60, 17537.5, 0, 2200),
        (61, 18300, 0, 0),
        (62, 18300, 0, 1100),
        (63, 18300, 0, 2200),
        (64, 19062.5, 0, 0),
        (65, 19062.5, 0, 2200),
        (66, 19825, 0, 0),
        (67, 19825, 0, 1100),
        (68, 19825, 0, 2200),
        (69, 20587.5, 0, 0),
        (70, 20587.5, 0, 2200),
        (71, 21350, 0, 0),
        (72, 21350, 0, 1100),
        (73, 21350, 0, 2200),
        (74, 0, -700, 0),
        (75, 3050, -700, 0),
        (76, 6100, -700, 0),
        (77, 9150, -700, 0),
        (78, 12200, -700, 0),
        (79, 15250, -700, 0),
        (80, 18300, -700, 0),
        (81, 21350, -700, 0),
        (82, 0, 5000, 0),
        (83, 0, 5000, 1100),
        (84, 0, 5000, 2200),
        (85, 762.5, 5000, 0),
        (86, 762.5, 5000, 2200),
        (87, 1525, 5000, 0),
        (88, 1525, 5000, 1100),
        (89, 1525, 5000, 2200),
        (90, 2287.5, 5000, 0),
        (91, 2287.5, 5000, 2200),
        (92, 3050, 5000, 0),
        (93, 3050, 5000, 1100),
        (94, 3050, 5000, 2200),
        (95, 3812.5, 5000, 0),
        (96, 3812.5, 5000, 2200),
        (97, 4575, 5000, 0),
        (98, 4575, 5000, 1100),
        (99, 4575, 5000, 2200),
        (100, 5337.5, 5000, 0),
        (101, 5337.5, 5000, 2200),
        (102, 6100, 5000, 0),
        (103, 6100, 5000, 1100),
        (104, 6100, 5000, 2200),
        (105, 6862.5, 5000, 0),
        (106, 6862.5, 5000, 2200),
        (107, 7625, 5000, 0),
        (108, 7625, 5000, 1100),
        (109, 7625, 5000, 2200),
        (110, 8387.5, 5000, 0),
        (111, 8387.5, 5000, 2200),
        (112, 9150, 5000, 0),
        (113, 9150, 5000, 1100),
        (114, 9150, 5000, 2200),
        (115, 9912.5, 5000, 0),
        (116, 9912.5, 5000, 2200),
        (117, 10675, 5000, 0),
        (118, 10675, 5000, 1100),
        (119, 10675, 5000, 2200),
        (120, 11437.5, 5000, 0),
        (121, 11437.5, 5000, 2200),
        (122, 12200, 5000, 0),
        (123, 12200, 5000, 1100),
        (124, 12200, 5000, 2200),
        (125, 12962.5, 5000, 0),
        (126, 12962.5, 5000, 2200),
        (127, 13725, 5000, 0),
        (128, 13725, 5000, 1100),
        (129, 13725, 5000, 2200),
        (130, 14487.5, 5000, 0),
        (131, 14487.5, 5000, 2200),
        (132, 15250, 5000, 0),
        (133, 15250, 5000, 1100),
        (134, 15250, 5000, 2200),
        (135, 16012.5, 5000, 0),
        (136, 16012.5, 5000, 2200),
        (137, 16775, 5000, 0),
        (138, 16775, 5000, 1100),
        (139, 16775, 5000, 2200),
        (140, 17537.5, 5000, 0),
        (141, 17537.5, 5000, 2200),
        (142, 18300, 5000, 0),
        (143, 18300, 5000, 1100),
        (144, 18300, 5000, 2200),
        (145, 19062.5, 5000, 0),
        (146, 19062.5, 5000, 2200),
        (147, 19825, 5000, 0),
        (148, 19825, 5000, 1100),
        (149, 19825, 5000, 2200),
        (150, 20587.5, 5000, 0),
        (151, 20587.5, 5000, 2200),
        (152, 21350, 5000, 0),
        (153, 21350, 5000, 1100),
        (154, 21350, 5000, 2200),
        (155, 0, 5700, 0),
        (156, 3050, 5700, 0),
        (157, 6100, 5700, 0),
        (158, 9150, 5700, 0),
        (159, 12200, 5700, 0),
        (160, 15250, 5700, 0),
        (161, 18300, 5700, 0),
        (162, 21350, 5700, 0),
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
        (11, 26, "H420x180", "ASTM-A36")
    ]

    for el in elements:
        structure.add_element(
            node_coords[el[0]], node_coords[el[1]], sections[el[2]], materials[el[3]]
        )

    # ========== Aplicar restricciones ==========
    constraints = {
        1: ["ux", "uy", "uz"],
        82: ["ux", "uy", "uz"],
        71: ["uy", "uz"],
        152: ["uy", "uz"],
    }

    for node_id, dofs in constraints.items():
        structure.add_constraint(node_coords[node_id], dofs)

    # Plot the structure with info
    plot_structure_with_info(structure, title="Estructura Bailey")

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
                deformation_scale=50,
            )

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

# Call run_example directly when the module is imported
run_example()
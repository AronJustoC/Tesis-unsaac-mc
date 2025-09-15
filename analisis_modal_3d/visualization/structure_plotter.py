import pyvista as pv
import numpy as np


def plot_structure_with_info(structure, title="Visualización de Estructura", highlight_coords=None, highlight_label="Nodos de Interés", mass_node_coords=None):
    """
    Visualiza una estructura con un estilo profesional.
    - Resaltado de nodos de interés y nodos con masa.
    """
    # 1. Extraer puntos y líneas
    points = np.array([node.coords for node in structure.nodes])
    lines = np.array([[2, structure.nodes.index(e.nodes[0]), structure.nodes.index(e.nodes[1])] for e in structure.elements])

    # 2. Crear malla y calcular tamaño
    mesh = pv.PolyData(points, lines=lines)
    bounds = mesh.bounds
    diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
    if diag_length == 0: diag_length = 1.0

    # 3. Configurar el plotter
    plotter = pv.Plotter(window_size=(800, 700))
    plotter.set_background("white")

    # 4. Añadir malla de la estructura
    plotter.add_mesh(mesh, color="gray", line_width=2, label="Estructura")

    # 5. Resaltar puntos de medición (cubos magenta)
    if highlight_coords:
        added_cube_label = False
        for coords in highlight_coords:
            # Cubos magenta para puntos de medición de velocidad
            cube_size = diag_length * 0.01
            cube = pv.Cube(center=coords, x_length=cube_size, y_length=cube_size, z_length=cube_size)
            if not added_cube_label:
                plotter.add_mesh(cube, color="magenta", label="Puntos de Medición")
                added_cube_label = True
            else:
                plotter.add_mesh(cube, color="magenta")

    # 6. Resaltar nodos con masa
    if mass_node_coords:
        radius = diag_length * 0.018 # Un poco más grande para la masa
        sphere = pv.Sphere(center=mass_node_coords[0], radius=radius)
        plotter.add_mesh(sphere, color="#606060", label="Masa del Motor") # Gris oscuro

    # 7. Visualizar restricciones
    if structure.constraints:
        symbol_scale = diag_length * 0.025
        offset_val = symbol_scale * 1
        added_labels = set()

        for node_index, dofs in structure.constraints.items():
            pos = points[node_index]
            constrained_trans = [d in dofs for d in range(3)]
            num_constrained = sum(constrained_trans)

            if num_constrained == 3:
                label = "Articulado"
                center = pos - np.array([0, 0, offset_val])
                symbol = pv.Cone(center=center, direction=[0, 0, 1], height=symbol_scale * 1.5, radius=symbol_scale, resolution=4)
                plotter.add_mesh(symbol, color="#0073e6", label=label if label not in added_labels else None)
                added_labels.add(label)

            elif num_constrained == 2:
                label = "Deslizante"
                center = pos - np.array([0, 0, offset_val])
                free_axis_idx = constrained_trans.index(False)
                cyl_direction = np.array([1., 0., 0.]) if free_axis_idx != 0 else np.array([0., 1., 0.])
                symbol = pv.Cylinder(center=center, direction=cyl_direction, radius=symbol_scale*0.7, height=symbol_scale*0.7)
                plotter.add_mesh(symbol, color="red", label=label if label not in added_labels else None)
                added_labels.add(label)

            elif num_constrained == 1:
                label = "Rodillo"
                constrained_axis_idx = constrained_trans.index(True)
                direction = np.zeros(3)
                direction[constrained_axis_idx] = 1.0
                center = pos - (direction * offset_val)
                symbol = pv.Sphere(center=center, radius=symbol_scale * 0.8)
                plotter.add_mesh(symbol, color="#00a86b", label=label if label not in added_labels else None)
                added_labels.add(label)

    # 8. Añadir etiquetas de nodos
    node_labels = [str(node.id) for node in structure.nodes]
    plotter.add_point_labels(points, node_labels, font_size=14, font_family="arial", text_color='#c400c4', shape=None, shadow=False)

    # 9. Añadir ejes, leyenda y título
    plotter.add_axes(xlabel="X", ylabel="Y", zlabel="Z")
    plotter.add_legend(bcolor="white")
    plotter.add_text(title, position="upper_edge", color="black", font_size=14, font="arial")

    # 10. Activar iluminación avanzada
    plotter.enable_lightkit()
 
    # 11. Mostrar
    plotter.show()

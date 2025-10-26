import pyvista as pv
import numpy as np

def plot_response_with_labels(
    structure,
    displacements,
    node_labels,
    nodes_of_interest,
    scale_factor=1.0,
    title="Respuesta de la Estructura"
):
    """
    Visualiza la estructura deformada y añade etiquetas personalizadas a los nodos.

    Args:
        structure (Structure): El objeto de la estructura.
        displacements (np.ndarray): Vector de desplazamientos complejos o reales.
        node_labels (dict): Un diccionario donde las claves son ahora índices de nodos (0-based)
                            y los valores son los strings de las etiquetas a mostrar.
        nodes_of_interest (list): Lista de índices de nodos (0-based) para resaltar con esferas.
        scale_factor (float): Factor de escala para la deformada.
        title (str): Título del gráfico.
    """
    original_points = np.array([node.coords for node in structure.nodes])
    lines = np.array([[2, structure.nodes.index(e.nodes[0]), structure.nodes.index(
        e.nodes[1])] for e in structure.elements])
    original_mesh = pv.PolyData(original_points, lines=lines)

    deformed_points = np.copy(original_points)
    num_nodes = len(structure.nodes)
    reshaped_displacements = displacements.reshape((num_nodes, 6))

    deformed_points += np.real(reshaped_displacements[:, :3]) * scale_factor

    deformed_mesh = pv.PolyData(deformed_points, lines=lines)

    plotter = pv.Plotter(window_size=(1200, 800))
    plotter.set_background("white")

    plotter.add_mesh(original_mesh, color="gray",
                     style='wireframe', line_width=2, label="Original")
    plotter.add_mesh(deformed_mesh, color="blue", line_width=4,
                     label=f"Deformada (x{scale_factor})")

    # Añadir esferas en los nodos de interés (ahora son índices)
    if nodes_of_interest:
        sphere_radius = np.linalg.norm(np.array(
            original_mesh.bounds[1::2]) - np.array(original_mesh.bounds[0::2])) * 0.005
        for node_index in nodes_of_interest:
            if node_index < len(original_points):
                plotter.add_mesh(pv.Sphere(radius=sphere_radius,
                                 center=original_points[node_index]), color='red')

    # Añadir etiquetas personalizadas (claves son índices)
    labels = []
    label_points = []
    for node_index, label_text in node_labels.items():
        if node_index < len(original_points):
            point = original_points[node_index]
            labels.append(label_text)
            label_points.append(point)

    if labels:
        plotter.add_point_labels(label_points, labels, font_size=10, font_family="arial", text_color='black',
                                 point_color='red', point_size=6, render_points_as_spheres=False,
                                 always_visible=True, shadow=False, shape_opacity=0.7)

    plotter.add_axes(xlabel="X", ylabel="Y", zlabel="Z")
    plotter.add_legend(bcolor="white")
    plotter.add_text(title, position="upper_edge",
                     color="black", font_size=14, font="arial")
    plotter.enable_lightkit()
    plotter.view_isometric()
    plotter.show()
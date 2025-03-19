import pyvista as pv
import numpy as np


def plot_structure(structure):
    # Configuración global para mejorar rendimiento
    pv.global_theme.render_lines_as_tubes = False
    pv.global_theme.smooth_shading = False

    plotter = pv.Plotter(window_size=[800, 600])
    plotter.set_background("black")

    # Dibujar elementos estructurales
    for element in structure.elements:
        points = np.array([node.coords for node in element.nodes], dtype=np.float32)
        line = pv.Line(points[0], points[1])
        plotter.add_mesh(line, color="cyan", line_width=2)

    # Dibujar nodos y etiquetas
    nodes = np.array([node.coords for node in structure.nodes], dtype=np.float32)
    node_ids = [str(node.id + 1) for node in structure.nodes]

    # Crear PolyData para etiquetas
    points = pv.PolyData(nodes)
    points["labels"] = node_ids

    # Añadir etiquetas de nodos
    plotter.add_point_labels(
        points,
        "labels",
        font_size=14,
        text_color="white",
        font_family="arial",
        shadow=True,
        shape_color=(0, 0, 0, 0.5),
        shape="rounded_rect",
        margin=2,
        always_visible=True,
    )

    # # Añadir puntos como esferas
    # plotter.add_mesh(
    #     points, color="red", point_size=8, render_points_as_spheres=True, pickable=False
    # )

    plotter.show(auto_close=True)

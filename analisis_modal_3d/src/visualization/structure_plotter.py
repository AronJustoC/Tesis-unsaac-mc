import pyvista as pv
import numpy as np

def plot_structure(structure):
    plotter = pv.Plotter(window_size=[1024, 768])
    plotter.set_background('black')
    
    # Dibujar elementos
    for i, element in enumerate(structure.elements):
        points = np.array([node.coords for node in element.nodes])
        line = pv.Line(points[0], points[1])
        plotter.add_mesh(line, color='cyan', line_width=2)
        mid_point = points.mean(axis=0)
        plotter.add_point_labels([mid_point], [f'E{i+1}'], text_color='yellow')
    
    # Dibujar nodos
    nodes = np.array([node.coords for node in structure.nodes])
    point_cloud = pv.PolyData(nodes)
    plotter.add_mesh(point_cloud, color='red', point_size=10)
    
    for i, node in enumerate(nodes):
        plotter.add_point_labels([node], [f'N{i+1}'], text_color='white')
    
    plotter.show()

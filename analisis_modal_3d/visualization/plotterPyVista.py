"""
Módulo para visualización 3D de estructuras y resultados con PyVista.
"""
import pyvista as pv
import numpy as np
from tqdm import tqdm

def animate_harmonic_response(
    structure: "Structure",
    displacement_history: np.ndarray,
    output_filename: str = "graficos_resultados/harmonic_animation.gif",
    scale_factor: float = 10.0,
    n_frames: int = 100
):
    """
    Crea una animación GIF de la respuesta armónica de la estructura.

    Args:
        structure (Structure): El objeto de la estructura original.
        displacement_history (np.ndarray): Matriz de desplazamientos (DOFs x tiempo).
        output_filename (str): Nombre del archivo GIF de salida.
        scale_factor (float): Factor para escalar las deformaciones y hacerlas visibles.
        n_frames (int): Número de fotogramas para la animación.
    """
    print("Iniciando la creación de la animación 3D con PyVista...")

    # 1. Crear la geometría de la estructura sin deformar
    points = np.array([node.coords for node in structure.nodes])
    lines = []
    for elem in structure.elements:
        n1_idx = structure.nodes.index(elem.nodes[0])
        n2_idx = structure.nodes.index(elem.nodes[1])
        lines.append([2, n1_idx, n2_idx])
    
    undeformed_mesh = pv.PolyData(points, lines=lines)

    # 2. Configurar el plotter de PyVista
    plotter = pv.Plotter(off_screen=True) # off_screen para evitar ventanas emergentes
    plotter.add_mesh(undeformed_mesh, style='wireframe', color='gray', line_width=2, label='Original')
    
    # Actor para la malla deformada que se actualizará
    deformed_actor = plotter.add_mesh(undeformed_mesh.copy(), color='dodgerblue', line_width=5, label='Deformada')
    plotter.add_legend()

    # 3. Crear la animación
    print(f"Generando animación en: {output_filename}")
    plotter.open_gif(output_filename)

    # Seleccionar fotogramas del historial de tiempo
    total_time_steps = displacement_history.shape[1]
    frame_indices = np.linspace(0, total_time_steps - 1, n_frames, dtype=int)

    for i in tqdm(frame_indices, desc="Creando fotogramas"): 
        # Obtener el vector de desplazamiento para el fotograma actual
        displacement_vector = displacement_history[:, i]
        
        # Crear los nuevos puntos deformados
        deformed_points = undeformed_mesh.points.copy()
        for node_idx, node in enumerate(structure.nodes):
            # Extraer solo los desplazamientos (ux, uy, uz)
            dx = displacement_vector[node.dofs[0]]
            dy = displacement_vector[node.dofs[1]]
            dz = displacement_vector[node.dofs[2]]
            deformed_points[node_idx, :] += np.array([dx, dy, dz]) * scale_factor
        
        # Actualizar la malla del actor deformado
        plotter.update_coordinates(deformed_points, mesh=deformed_actor.mapper.dataset)
        plotter.write_frame()

    plotter.close()
    print("\nAnimación 3D completada.")
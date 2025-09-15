import pyvista as pv
import numpy as np
import time


def plot_mode_shape(
    structure,
    mode_vector,
    deformation_scale=None,  # Default cambiado a None para activar la escala automática
    title="Visualización de modo",
):
    """
    Visualiza la forma modal con un estilo profesional y simbología de restricciones.
    - Paleta de colores profesional (Grafito, Carmesí, Azul, Magenta, Verde).
    - Iluminación avanzada y renderizado de líneas como tubos.
    - Tipografía limpia (Arial) y composición mejorada.
    """
    # 1. Extraer puntos y líneas
    points = np.array([node.coords for node in structure.nodes], dtype=float)
    lines = np.array([[2, structure.nodes.index(e.nodes[0]), structure.nodes.index(e.nodes[1])] for e in structure.elements])

    # 2. Crear malla original
    original_mesh = pv.PolyData(points, lines=lines)

    # 3. Lógica de escalado dinámico
    if deformation_scale is None:
        bounds = original_mesh.bounds
        diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
        if diag_length == 0: diag_length = 1.0
        # La escala será un 20% de la diagonal del bounding box de la estructura
        deformation_scale = diag_length * 0.1
        print(f"  - Usando escala de deformación automática: {deformation_scale:.2f}")

    # 4. Calcular puntos deformados
    deformed_points = np.copy(points)
    for i, node in enumerate(structure.nodes):
        dofs = node.dofs
        if dofs and max(dofs) < len(mode_vector):
            deformed_points[i, 0] += mode_vector[dofs[0]] * deformation_scale
            deformed_points[i, 1] += mode_vector[dofs[1]] * deformation_scale
            deformed_points[i, 2] += mode_vector[dofs[2]] * deformation_scale
    deformed_mesh = pv.PolyData(deformed_points, lines=lines)

    # 5. Configurar el plotter
    plotter = pv.Plotter(window_size=(800, 700))
    plotter.set_background("white")

    # 6. Añadir mallas con estilo profesional
    plotter.add_mesh(original_mesh, color="gray", line_width=1, label="Original")
    plotter.add_mesh(deformed_mesh, color="#dc143c", style='wireframe', line_width=3, label="Modo")

    # 7. Visualizar restricciones
    if structure.constraints:
        bounds = original_mesh.bounds
        diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
        if diag_length == 0: diag_length = 1.0
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
                plotter.add_mesh(symbol, color="#c400c4", label=label if label not in added_labels else None)
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

    # 8. Añadir ejes, leyenda y título
    plotter.add_axes(xlabel="X", ylabel="Y", zlabel="Z")
    plotter.add_legend(bcolor="white")
    plotter.add_text(title, position="upper_edge", color="black", font_size=12, font="arial")

    # 9. Activar iluminación avanzada
    plotter.enable_lightkit()

    # 10. Mostrar o guardar
    plotter.show(title=title)


def animate_mode_shape(
    structure,
    mode_vector,
    deformation_scale=None,
    title="Animación de modo",
    filename=None,
    n_frames=30,
    fps=10,
):
    """
    Anima la forma modal y la guarda como un GIF.
    """
    points = np.array([node.coords for node in structure.nodes], dtype=float) # MODIFICADO: dtype=float
    lines = np.array(
        [
            [2, structure.nodes.index(e.nodes[0]), structure.nodes.index(e.nodes[1])]
            for e in structure.elements
        ]
    )
    original_mesh = pv.PolyData(points, lines=lines)

    plotter = pv.Plotter(off_screen=True, window_size=(800, 700))
    plotter.set_background("white")
    plotter.add_mesh(original_mesh, color="gray", line_width=1, label="Original")

    # Configurar la cámara
    plotter.camera_position = "iso"

    # Calculate dynamic deformation scale only if not provided
    if deformation_scale is None:
        bounds = original_mesh.bounds
        diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
        if diag_length == 0: diag_length = 1.0
        
        # Set deformation_scale to be proportional to the structure's size
        # You might need to adjust the multiplier (e.g., 0.5) based on desired visual effect
        deformation_scale = diag_length * 0.02 

    # Abrir el archivo GIF
    if filename:
        plotter.open_gif(filename, fps=fps)

    # Bucle de animación
    for phase in np.linspace(0, 2 * np.pi, n_frames, endpoint=False):
        deformed_points = np.copy(points)
        for i, node in enumerate(structure.nodes):
            dofs = node.dofs
            if dofs and max(dofs) < len(mode_vector):
                displacement = mode_vector[dofs[0:3]] * np.sin(phase)
                deformed_points[i] += displacement * deformation_scale

        deformed_mesh = pv.PolyData(deformed_points, lines=lines)
        plotter.add_mesh(
            deformed_mesh,
            color="#dc143c",
            style="wireframe",
            line_width=3,
            name="deformed",
        )
        plotter.add_text(
            title, position="upper_edge", color="black", font_size=12, font="arial"
        )
        plotter.write_frame()
        plotter.remove_actor("deformed")

    plotter.close()

def animate_mode_interactive(structure, mode_vector, **kwargs):
    print("La función 'animate_mode_interactive' ha sido deshabilitada.")
    pass

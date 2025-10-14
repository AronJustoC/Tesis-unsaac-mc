import pyvista as pv
import numpy as np

def plot_deformed_structure(structure, u, scale_factor=1.0, title="Estructura Deformada vs. Original", mass_node_id=None, axial_forces=None):
    """
    Visualiza la estructura original y la deformada una sobre la otra,
    con estilo similar a la visualización modal.

    Args:
        structure (Structure): El objeto de la estructura original.
        u (np.ndarray): El vector de desplazamiento nodal global.
        scale_factor (float): Factor para escalar las deformaciones para una mejor visualización.
        title (str): Título del gráfico.
        mass_node_id (int, optional): ID del nodo donde se aplica una masa. Usado para resaltarlo.
        axial_forces (list, optional): Lista de fuerzas axiales para cada elemento. Usado para colorear.
    """
    # 1. Crear puntos y líneas para la estructura original
    original_points = np.array([node.coords for node in structure.nodes])
    lines = np.array([[2, structure.nodes.index(e.nodes[0]), structure.nodes.index(e.nodes[1])] for e in structure.elements])
    original_mesh = pv.PolyData(original_points, lines=lines)

    # 2. Calcular las coordenadas de los nodos deformados
    deformed_points = np.copy(original_points)
    num_nodes = len(structure.nodes)
    displacements = u.reshape((num_nodes, 6))
    
    deformed_points += displacements[:, :3] * scale_factor
    deformed_mesh = pv.PolyData(deformed_points, lines=lines)

    # 3. Configurar el plotter
    plotter = pv.Plotter(window_size=(1000, 800))
    plotter.set_background("white")

    # 4. Añadir mallas al plotter
    # Estructura original en gris
    plotter.add_mesh(original_mesh, color="gray", style='wireframe', line_width=2, label="Original")
    
    # Estructura deformada en color primario (azul)
    # If axial_forces are provided, color the deformed mesh by axial force
    if axial_forces is not None and len(axial_forces) == len(structure.elements):
        # Create a PyVista mesh for the elements to color them
        element_lines = np.array([[2, structure.nodes.index(e.nodes[0]), structure.nodes.index(e.nodes[1])] for e in structure.elements])
        element_mesh = pv.PolyData(deformed_points, lines=element_lines)
        
        # Add scalar data (axial forces) to the mesh
        element_mesh["Axial Force"] = np.array(axial_forces)
        
        # Plot the elements with a colormap
        plotter.add_mesh(element_mesh, cmap="viridis", line_width=8, scalars="Axial Force",
                         show_scalar_bar=True, scalar_bar_args={'title': 'Fuerza Axial (N)'},
                         label=f"Deformada (x{scale_factor}) - Fuerza Axial")
    else:
        plotter.add_mesh(deformed_mesh, color="blue", line_width=4, label=f"Deformada (x{scale_factor})")

    # 5. Resaltar nodo con masa (si existe)
    if mass_node_id is not None:
        node_coords_map = {node.id: node for node in structure.nodes}
        if mass_node_id in node_coords_map:
            mass_coords = node_coords_map[mass_node_id].coords
            bounds = original_mesh.bounds
            diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
            radius = diag_length * 0.018 # Un poco más grande para la masa
            sphere = pv.Sphere(center=mass_coords, radius=radius)
            plotter.add_mesh(sphere, color="#606060", label="Masa del Motor") # Gris oscuro

    # 6. Visualizar restricciones (similar a structure_plotter)
    if structure.constraints:
        bounds = original_mesh.bounds
        diag_length = np.sqrt((bounds[1]-bounds[0])**2 + (bounds[3]-bounds[2])**2 + (bounds[5]-bounds[4])**2)
        if diag_length == 0: diag_length = 1.0
        
        # Aumentar el tamaño de los símbolos de restricción para mayor visibilidad
        symbol_scale = diag_length * 0.025 * 5 # Multiplicar por 5
        offset_val = symbol_scale * 1 * 5 # Multiplicar por 5
        added_labels = set()

        for node_index, dofs in structure.constraints.items():
            node_obj = structure.nodes[node_index]
            pos = np.array(node_obj.coords)
            constrained_trans = [d in dofs for d in ['ux', 'uy', 'uz']]
            num_constrained = sum(constrained_trans)

            if num_constrained == 3: # Empotramiento o articulación fija
                label = "Articulado"
                center = pos - np.array([0, 0, offset_val])
                symbol = pv.Cone(center=center, direction=[0, 0, 1], height=symbol_scale * 1.5, radius=symbol_scale, resolution=4)
                plotter.add_mesh(symbol, color="#0073e6", label=label if label not in added_labels else None)
                added_labels.add(label)

            elif num_constrained == 2: # Deslizante en un plano
                label = "Deslizante"
                center = pos - np.array([0, 0, offset_val])
                # Determinar el eje libre para la dirección del cilindro
                free_axis_idx = -1
                if not constrained_trans[0]: free_axis_idx = 0
                elif not constrained_trans[1]: free_axis_idx = 1
                elif not constrained_trans[2]: free_axis_idx = 2

                cyl_direction = np.zeros(3)
                if free_axis_idx != -1: cyl_direction[free_axis_idx] = 1.0
                else: cyl_direction = [0,0,1] # Fallback

                symbol = pv.Cylinder(center=center, direction=cyl_direction, radius=symbol_scale*0.7, height=symbol_scale*0.7)
                plotter.add_mesh(symbol, color="red", label=label if label not in added_labels else None)
                added_labels.add(label)

            elif num_constrained == 1: # Rodillo
                label = "Rodillo"
                constrained_axis_idx = constrained_trans.index(True)
                direction = np.zeros(3)
                direction[constrained_axis_idx] = 1.0
                center = pos - (direction * offset_val)
                symbol = pv.Sphere(center=center, radius=symbol_scale * 0.8)
                plotter.add_mesh(symbol, color="#00a86b", label=label if label not in added_labels else None)
                added_labels.add(label)

    # 7. Añadir etiquetas de nodos
    node_labels = [str(node.id) for node in structure.nodes]
    plotter.add_point_labels(original_points, node_labels, font_size=14, font_family="arial", text_color='#c400c4', shape=None, shadow=False)

    # 8. Añadir información adicional
    plotter.add_axes(xlabel="X", ylabel="Y", zlabel="Z")
    plotter.add_legend(bcolor="white")
    plotter.add_text(title, position="upper_edge", color="black", font_size=14, font="arial")

    # 9. Activar iluminación avanzada
    plotter.enable_lightkit()
 
    # 10. Configurar cámara y mostrar
    plotter.view_isometric() # Usar vista isométrica
    plotter.camera.SetParallelProjection(False) # Asegurar perspectiva
    plotter.show()

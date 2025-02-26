import pyvista as pv


def plot_mode_shape(
    structure,
    mode_vector,
    deformation_scale=100,
    title="Mode Shape Visualization",
    filename=None,
):
    """
    Visualiza la forma modal (mode shape) de una estructura utilizando PyVista.

    Se dibujan tanto la estructura original (en blanco) como la deformada (en rojo),
    y se fuerza un escalado 1:1 para visualizar correctamente las dimensiones.

    Parámetros:
        structure: objeto que contiene la estructura con una lista de elementos.
                   Cada elemento debe tener un atributo 'elements', donde cada elemento tiene
                   una lista de nodos en 'nodes'. Cada nodo debe tener:
                       - node.coords: lista o tupla con las coordenadas [x, y, z].
                       - node.dofs: lista de índices para acceder a las componentes del mode_vector.
        mode_vector: vector (lista, array, etc.) con los desplazamientos modales.
        deformation_scale: factor de escala para amplificar la deformación.
        title: título de la visualización.
        filename: si se especifica, se guarda una captura de pantalla en este archivo.
    """

    # Crear el plotter con fondo negro y tamaño de ventana adecuado.
    plotter = pv.Plotter(window_size=(1000, 800))
    plotter.set_background("black")

    # Listas para calcular la caja de límites (bounding box)
    all_x, all_y, all_z = [], [], []

    # Dibujar la estructura original (líneas en color blanco)
    for element in structure.elements:
        # Extraer coordenadas de los nodos
        pts = [node.coords for node in element.nodes]
        # Acumular puntos para la caja de límites
        for pt in pts:
            all_x.append(pt[0])
            all_y.append(pt[1])
            all_z.append(pt[2])
        # Crear la línea entre nodos (se asume que el elemento es de dos nodos)
        line = pv.Line(pts[0], pts[1])
        plotter.add_mesh(line, color="white", line_width=2, label="Original")

    # Dibujar la estructura deformada (líneas en color rojo)
    for element in structure.elements:
        n1, n2 = element.nodes
        # Calcular coordenadas deformadas para cada nodo
        pt1_def = [
            n1.coords[i] + mode_vector[n1.dofs[i]] * deformation_scale for i in range(3)
        ]
        pt2_def = [
            n2.coords[i] + mode_vector[n2.dofs[i]] * deformation_scale for i in range(3)
        ]
        # Acumular puntos deformados para la caja de límites
        for pt in [pt1_def, pt2_def]:
            all_x.append(pt[0])
            all_y.append(pt[1])
            all_z.append(pt[2])
        # Crear la línea deformada
        deformed_line = pv.Line(pt1_def, pt2_def)
        actor = plotter.add_mesh(
            deformed_line, color="red", line_width=2, label="Deformed"
        )
        try:
            # Intentar aplicar un patrón de línea discontinua (puede requerir versión compatible de VTK)
            actor.GetProperty().SetLineStipplePattern(0xF0F0)
            actor.GetProperty().SetLineStippleRepeatFactor(1)
        except Exception:
            # Si no es compatible, se ignora y se muestra como línea continua.
            pass

    # Calcular la caja de límites para forzar una escala 1:1
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    min_z, max_z = min(all_z), max(all_z)
    max_range = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
    mid_x = (max_x + min_x) * 0.5
    mid_y = (max_y + min_y) * 0.5
    mid_z = (max_z + min_z) * 0.5

    # Crear una caja invisible que abarca los límites calculados para mantener el aspect ratio 1:1
    dummy = pv.Box(
        bounds=[
            mid_x - max_range,
            mid_x + max_range,
            mid_y - max_range,
            mid_y + max_range,
            mid_z - max_range,
            mid_z + max_range,
        ]
    )
    plotter.add_mesh(dummy, opacity=0)

    # Agregar ejes con color blanco (usando add_axes en lugar de show_axes)
    plotter.add_axes(color="white")

    # Agregar leyenda para identificar las líneas originales y deformadas
    plotter.add_legend(
        labels=[("Original", "white"), ("Deformed", "red")], bcolor="black"
    )

    # Agregar título en la ventana del plotter
    plotter.add_text(title, position="upper_edge", color="white", font_size=14)

    # Mostrar o guardar la visualización
    if filename:
        # Guardar una captura de pantalla y cerrar la ventana
        plotter.show(screenshot=filename, title=title)
    else:
        plotter.show(title=title)

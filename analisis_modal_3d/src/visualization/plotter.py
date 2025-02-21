import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_mode_shape(structure, mode_vector, scale_factor=100, title="Mode Shape Visualization", filename=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    
    # Configuraciones de la figura
    ax.set_box_aspect([1, 1, 2])
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    plt.title(title)

    # Dibujar estructura original
    for element in structure.elements:
        x = [node.coords[0] for node in element.nodes]
        y = [node.coords[1] for node in element.nodes]
        z = [node.coords[2] for node in element.nodes]
        ax.plot(x, y, z, "k-", lw=2, label="Original")

    # Dibujar estructura deformada
    for element in structure.elements:
        n1, n2 = element.nodes
        dx1, dy1, dz1 = mode_vector[n1.dofs[0]] * scale_factor, mode_vector[n1.dofs[1]] * scale_factor, mode_vector[n1.dofs[2]] * scale_factor
        dx2, dy2, dz2 = mode_vector[n2.dofs[0]] * scale_factor, mode_vector[n2.dofs[1]] * scale_factor, mode_vector[n2.dofs[2]] * scale_factor
        
        ax.plot(
            [n1.coords[0] + dx1, n2.coords[0] + dx2],
            [n1.coords[1] + dy1, n2.coords[1] + dy2],
            [n1.coords[2] + dz1, n2.coords[2] + dz2],
            "r--", lw=2, label="Deformed"
        )

    # Manejar leyendas y guardar/mostrar
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys())
    
    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
    else:
        plt.show()
    
    plt.close()
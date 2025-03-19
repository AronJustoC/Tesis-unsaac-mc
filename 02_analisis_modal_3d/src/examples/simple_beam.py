from src.structures import Structure
from src.analysis import modal_analysis
from src.visualization import plot_mode_shape
import numpy as np
import matplotlib.pyplot as plt

def plot_structure(structure):
    """Genera una figura de la estructura con numeración y fondo negro."""
    fig = plt.figure(facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Configurar colores y estilo
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')
    ax.tick_params(colors='white')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, color='gray', alpha=0.3)
    
    # Dibujar elementos
    for i, element in enumerate(structure.elements):
        x = [node.coords[0] for node in element.nodes]
        y = [node.coords[1] for node in element.nodes]
        z = [node.coords[2] for node in element.nodes]
        ax.plot(x, y, z, 'cyan', linewidth=2)
        # Añadir número de elemento en el centro
        mid_x = sum(x) / 2
        mid_y = sum(y) / 2
        mid_z = sum(z) / 2
        ax.text(mid_x, mid_y, mid_z, f'E{i+1}', color='yellow', fontsize=8)
    
    # Dibujar nodos
    for i, node in enumerate(structure.nodes):
        ax.scatter(node.coords[0], node.coords[1], node.coords[2], 
                  color='red', s=100, marker='o')
        ax.text(node.coords[0], node.coords[1], node.coords[2], 
                f'N{i+1}', color='white', fontsize=10)
    
    plt.title('Estructura 3D', color='white', pad=20)
    fig.tight_layout()
    plt.show()

def main():
    # Configurar backend interactivo (opcional)
    # import matplotlib
    # matplotlib.use('TkAgg')  # Descomentar para visualización local
    
    structure = Structure()

    # Añadir nodos
    n1 = structure.add_node(0, 0, 0)
    n2 = structure.add_node(5, 0, 0)
    n3 = structure.add_node(10, 0, 0)
    n4 = structure.add_node(0, 5, 0)
    n5 = structure.add_node(5, 5, 0)
    n6 = structure.add_node(10, 5, 0)
    n7 = structure.add_node(5, 2.5, 5)

    # Propiedades de sección y material
    section = {"area": 0.015, "Ix": 8.5e-5, "Iy": 1.25e-4, "Iz": 5.8e-5}
    material = {"E": 210e9, "G": 80e9, "rho": 7850}

    # Crear elementos
    structure.add_element(n1, n2, section, material)
    structure.add_element(n2, n3, section, material)
    structure.add_element(n4, n5, section, material)
    structure.add_element(n5, n6, section, material)
    structure.add_element(n1, n4, section, material)
    structure.add_element(n2, n5, section, material)
    structure.add_element(n3, n6, section, material)
    structure.add_element(n1, n7, section, material)
    structure.add_element(n2, n7, section, material)
    structure.add_element(n3, n7, section, material)
    structure.add_element(n4, n7, section, material)
    structure.add_element(n5, n7, section, material)
    structure.add_element(n6, n7, section, material)

    # Restricciones
    structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n3, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n4, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n6, ["ux", "uy", "uz", "rx", "ry", "rz"])

    # Graficar estructura
    plot_structure(structure)

    try:
        constrained_dofs = structure.get_constrained_dofs()
        freqs, modes = modal_analysis(structure, num_modes=5, constrained_dofs=constrained_dofs)
        
        print("\nNatural Frequencies:")
        print("-" * 30)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # Graficar y guardar modos
        for i in range(5):
            plot_mode_shape(
                structure, 
                modes[:, i], 
                title=f"Mode {i+1} - {freqs[i]:.2f} Hz",
                filename=f"mode_shape_{i+1}.png",
                scale_factor=50
            )
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
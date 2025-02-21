from src.structures import Structure
from src.analysis import modal_analysis
from src.visualization import plot_mode_shape
import numpy as np

def main():
    # Configurar backend interactivo (opcional)
    # import matplotlib
    # matplotlib.use('TkAgg')  # Descomentar para visualización local
    
    structure = Structure()

    # Añadir nodos
    n1 = structure.add_node(0, 0, 0)
    n2 = structure.add_node(0, 0, 5)
    n3 = structure.add_node(0, 0, 10)

    # Propiedades de sección y material
    section = {"area": 0.015, "Ix": 8.5e-5, "Iy": 1.25e-4, "Iz": 5.8e-5}
    material = {"E": 210e9, "G": 80e9, "rho": 7850}

    # Crear elementos
    structure.add_element(n1, n2, section, material)
    structure.add_element(n2, n3, section, material)

    # Restricciones
    structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])

    try:
        constrained_dofs = structure.get_constrained_dofs()
        freqs, modes = modal_analysis(structure, num_modes=3, constrained_dofs=constrained_dofs)
        
        print("\nNatural Frequencies:")
        print("-" * 30)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # Graficar y guardar modos
        for i in range(3):
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
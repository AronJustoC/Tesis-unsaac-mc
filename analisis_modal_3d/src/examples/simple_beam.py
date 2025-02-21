from src.structures import Structure
from src.analysis import modal_analysis
from src.visualization import plot_mode_shape
import numpy as np

def main():
    # Create new structure
    structure = Structure()

    # Add nodes (x, y, z coordinates in meters)
    n1 = structure.add_node(0, 0, 0)
    n2 = structure.add_node(0, 0, 5)
    n3 = structure.add_node(0, 0, 10)

    # Define HEB 300 section properties
    section = {
        "area": 0.015,  # m²
        "Ix": 8.5e-5,  # m⁴ (torsion constant)
        "Iy": 1.25e-4,  # m⁴ (strong axis moment of inertia)
        "Iz": 5.8e-5,  # m⁴ (weak axis moment of inertia)
    }

    # Define material properties (Steel)
    material = {
        "E": 210e9,  # Pa (Young's modulus)
        "G": 80e9,   # Pa (Shear modulus)
        "rho": 7850, # kg/m³ (density)
    }

    # Create beam elements
    structure.add_element(n1, n2, section, material)
    structure.add_element(n2, n3, section, material)

    # Fix base node (all DOFs constrained)
    structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])

    try:
        # Get constrained DOFs for modal analysis
        constrained_dofs = structure.get_constrained_dofs()
        
        # Perform modal analysis
        freqs, modes = modal_analysis(structure, num_modes=3, constrained_dofs=constrained_dofs)

        # Print natural frequencies
        print("\nNatural Frequencies:")
        print("-" * 20)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # Plot each mode shape
        for i in range(3):
            plot_mode_shape(structure, modes[:, i], 
                          title=f"Mode {i+1} - {freqs[i]:.2f} Hz")
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()

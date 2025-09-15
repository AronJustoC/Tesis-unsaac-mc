from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
from analisis_modal_3d.visualization.plotter import animate_mode_shape
import numpy as np
import os

def generate_gifs_for_all_modes():
    structure = Structure()

    # Add nodes (from simple_beam.py)
    n1 = structure.add_node(0, 0, 0)
    n2 = structure.add_node(5, 0, 0)
    n3 = structure.add_node(10, 0, 0)
    n4 = structure.add_node(0, 5, 0)
    n5 = structure.add_node(5, 5, 0)
    n6 = structure.add_node(10, 5, 0)
    n7 = structure.add_node(5, 2.5, 5)

    # Section and material properties (from simple_beam.py)
    section = {"area": 0.015, "Ix": 8.5e-5, "Iy": 1.25e-4, "Iz": 5.8e-5}
    material = {"E": 210e9, "G": 80e9, "rho": 7850}

    # Create elements (from simple_beam.py)
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

    # Constraints (from simple_beam.py)
    structure.add_constraint(n1, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n3, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n4, ["ux", "uy", "uz", "rx", "ry", "rz"])
    structure.add_constraint(n6, ["ux", "uy", "uz", "rx", "ry", "rz"])

    try:
        K_global, M_global = assemble_global_matrices(structure)
        # Get all modes (or a reasonable number, e.g., 10 or 20)
        # The number of modes should not exceed the number of DOFs minus constraints.
        # Let's try to get 10 modes, or fewer if not available.
        num_dofs = structure.num_dofs
        num_constraints = sum(len(c) for c in structure.constraints.values())
        max_modes = num_dofs - num_constraints
        
        # Ensure num_modes is positive
        num_modes_to_get = min(10, max_modes) if max_modes > 0 else 1

        freqs, modes = modal_analysis(
            K_global, M_global, structure, num_modes=num_modes_to_get
        )

        if len(modes) > 0:
            output_dir = "/home/aron/Aron/08_TesisUnsaac/graficos_resultados/modo_animacion/"
            os.makedirs(output_dir, exist_ok=True) # Ensure directory exists

            for i in range(modes.shape[1]): # Iterate through all available modes
                mode_vector = modes[:, i]
                output_filename = os.path.join(output_dir, f"mode_{i+1}_animation.gif")
                
                print(f"Generating GIF for mode {i+1} to: {output_filename}")
                animate_mode_shape(
                    structure,
                    mode_vector,
                    title=f"Mode {i+1} - {freqs[i]:.2f} Hz",
                    filename=output_filename,
                    n_frames=60, # More frames for smoother animation
                    fps=20 # Faster frame rate
                )
                print(f"GIF for mode {i+1} generation complete.")
        else:
            print("No modes found to animate.")

    except Exception as e:
        print(f"Error during GIF generation: {str(e)}")

if __name__ == "__main__":
    generate_gifs_for_all_modes()

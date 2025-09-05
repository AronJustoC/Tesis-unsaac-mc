from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
import multiprocessing
from analisis_modal_3d.visualization.plotter import plot_mode_shape
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info

# Global variables to store results
structure = None
freqs = None
modes = None
harmonic_displacement_history = None

def run_example():
    global structure, freqs, modes, harmonic_displacement_history

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

    # Plot the structure with info
    plot_structure_with_info(structure, title="Estructura de Viga Simple")

    try:
        K_global, M_global = assemble_global_matrices(structure)
        freqs, modes = modal_analysis(
            K_global, M_global, structure, num_modes=5
        )

        print("\nNatural Frequencies:")
        print("-" * 30)
        for i, freq in enumerate(freqs, 1):
            print(f"Mode {i}: {freq:.2f} Hz")

        # --- Visualización de Modos en Procesos Separados ---
        plot_processes = []
        print("\nLanzando ventanas de visualización de modos. Cierre cada ventana para continuar.")

        for i in range(min(len(freqs), 3)): # Plot first 3 modes for brevity
            title = f"Modo {i+1} - {freqs[i]:.2f} Hz"
            # Crear un proceso para cada ventana de ploteo
            plot_process = multiprocessing.Process(
                target=plot_mode_shape,
                args=(structure, modes[:, i]),
                kwargs={"title": title, "deformation_scale": 50}
            )
            plot_processes.append(plot_process)
            plot_process.start()

        # Esperar a que todos los procesos de ploteo terminen (ventanas cerradas)
        for p in plot_processes:
            p.join()

    except Exception as e:
        print(f"Error: {str(e)}")

# Call run_example directly when the module is imported
run_example()
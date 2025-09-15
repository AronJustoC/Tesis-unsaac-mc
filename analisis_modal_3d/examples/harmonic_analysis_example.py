import numpy as np

from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.structures.node import Node
from analisis_modal_3d.structures.element import Element
from analisis_modal_3d.analysis import assembler, modal
from analisis_modal_3d.analysis.damping import rayleigh_damping_matrix
from analisis_modal_3d.analysis.forced_vibration import harmonic_analysis_superposition
from analisis_modal_3d.visualization.plotterPyVista import animate_harmonic_response
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info

# Global variables to store results
structure = None
freqs = None
modes = None
harmonic_displacement_history = None

def run_example():
    global structure, freqs, modes, harmonic_displacement_history

    # 1. Definición de la Estructura (Viga en voladizo)
    # -----------------------------------------------------
    print("1. Definiendo la estructura...")

    # Crear el objeto structure
    structure = Structure()

    # Añadir nodos a la structure
    nodo_0 = structure.add_node(0, 0, 0)  # Nodo 0 en el origen
    nodo_1 = structure.add_node(1, 0, 0)   # Nodo 1 a 1m de distancia en x

    # Propiedades del material (Acero)
    material_props = {
        'E': 210e9,  # Módulo de Young (Pa)
        'G': 80e9,   # Módulo de Cortante (Pa)
        'rho': 7850 # Densidad (kg/m^3)
    }

    # Propiedades de la sección (viga IPE 100)
    seccion_props = {
        'area': 10.3e-4,     # Área (m^2)
        'Iy': 34.9e-8,    # Inercia en y (m^4) - OJO: Iy y Iz pueden estar intercambiadas dependiendo de la convención
        'Iz': 171e-8,     # Inercia en z (m^4)
        'Ix': 1.07e-8      # Inercia Torsional (m^4) - OJO: A veces se usa J
    }

    # Añadir elemento a la structure
    structure.add_element(nodo_0, nodo_1, seccion_props, material_props)

    # Fijar el nodo 0 (empotramiento)
    structure.add_constraint(nodo_0, ['ux', 'uy', 'uz', 'rx', 'ry', 'rz'])

    # Aplicar la fuerza en el nodo 1, en dirección Y
    force_amplitude = 1000  # Amplitud de la fuerza (N)
    force_node_index = 1
    dof_index = 1  # 0:x, 1:y, 2:z, 3:rx, 4:ry, 5:rz

    # Definir nodos de interés para visualización
    # El nodo de interés es donde se aplica la fuerza
    interest_node_coords = [structure.nodes[force_node_index].coords]
    
    # El nodo con masa es el mismo en este caso
    mass_node_coords = [structure.nodes[force_node_index].coords]

    # Plot the structure with info
    plot_structure_with_info(
        structure,
        title="Estructura de Viga en Voladizo",
        highlight_coords=interest_node_coords,
        mass_node_coords=mass_node_coords
    )

    # 2. Ensamblaje y Análisis Modal
    # -----------------------------------------------------
    print("2. Realizando análisis modal...")
    K_global, M_global = assembler.assemble_global_matrices(structure)

    # Resolver el problema de valores propios
    freqs, modes, _ = modal.modal_analysis(K_global, M_global, structure)

    # Convertir frecuencias a rad/s
    frecuencias_rad = freqs * 2 * np.pi

    print(f"Frecuencias naturales (Hz): {freqs[:5]}")

    # 3. Definición del Amortiguamiento
    # -----------------------------------------------------
    print("3. Definiendo la matriz de amortiguamiento...")
    # Coeficientes de Rayleigh (ejemplo)
    # Estos valores dependen del material y la structure, aquí son ilustrativos
    alpha = 0.1
    beta = 0.001
    C_global = rayleigh_damping_matrix(M_global, K_global, alpha, beta)

    # 4. Definición de la Carga Armónica
    # -----------------------------------------------------
    print("4. Definiendo la carga armónica...")
    # Frecuencia de la fuerza (cercana a la primera frecuencia natural para ver resonancia)
    # ¡PRECAUCIÓN! Si es exactamente igual, la respuesta puede ser infinita sin amortiguamiento.
    force_frequency_hz = freqs[0] * 0.9 # 90% de la primera frecuencia natural
    force_frequency_rad = force_frequency_hz * 2 * np.pi

    # Crear el vector de fuerza F0
    num_dofs = K_global.shape[0]
    F0 = np.zeros(num_dofs)
    F0[force_node_index * 6 + dof_index] = force_amplitude

    # 5. Solución de la Vibración Forzada
    # -----------------------------------------------------
    print("5. Resolviendo el análisis de vibración forzada...")
    # Definir el tiempo de simulación
    # Simular durante 50 ciclos de la fuerza aplicada
    num_cycles = 50
    duration = num_cycles / force_frequency_hz
    time_steps = 1000
    time_array = np.linspace(0, duration, time_steps)

    # Calcular la respuesta
    harmonic_displacement_history = harmonic_analysis_superposition(
        natural_frequencies_rad=frecuencias_rad,
        mode_shapes=modes,
        M=M_global,
        K=K_global,
        C=C_global,
        force_vector=F0,
        force_frequency_rad=force_frequency_rad,
        time_array=time_array
    )

    # Diagnóstico de la respuesta
    print("\n--- Diagnóstico de la Respuesta ---")
    print(f"Forma de la matriz de desplazamientos (harmonic_displacement_history): {harmonic_displacement_history.shape}")
    print(f"Valor máximo del desplazamiento: {np.max(harmonic_displacement_history)}")
    print(f"Valor mínimo del desplazamiento: {np.min(harmonic_displacement_history)}")
    print(f"Valor medio del desplazamiento: {np.mean(harmonic_displacement_history)}")
    print("------------------------------------\n")

    # 6. Visualización de Resultados
    # -----------------------------------------------------
    print("6. Generando animación 3D de la respuesta...")
    animate_harmonic_response(
        structure=structure,
        displacement_history=harmonic_displacement_history,
        scale_factor=5000,  # Aumentar si la deformación no es visible
        n_frames=100
    )

# Call run_example directly when the module is imported
run_example()
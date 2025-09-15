import numpy as np
import matplotlib.pyplot as plt

from analisis_modal_3d.structures.structure import Structure
from analisis_modal_3d.analysis import assembler, modal
from analisis_modal_3d.analysis.damping import rayleigh_damping_matrix
from analisis_modal_3d.analysis.frequency_response import direct_frequency_response


def run_frequency_sweep_example():
    """
    Ejemplo completo de análisis de barrido de frecuencia para una estructura,
    incluyendo la generación de una tabla de velocidades en nodos específicos.
    """

    # 1. Definición de la Estructura (Viga simplemente apoyada)
    # ------------------------------------------------------------------
    print("1. Definiendo la estructura...")
    structure = Structure()
    
    # Nodos (viga de 10 metros)
    num_elements = 10
    length = 10.0
    nodes = [structure.add_node(x, 0, 0) for x in np.linspace(0, length, num_elements + 1)]

    # Propiedades (Acero)
    material = {'E': 210e9, 'G': 80e9, 'rho': 7850}
    section = {'area': 0.05, 'Iy': 8.33e-5, 'Iz': 8.33e-5, 'Ix': 1.67e-4}

    # Elementos
    for i in range(num_elements):
        structure.add_element(nodes[i], nodes[i+1], section, material)

    # Restricciones (Simplemente apoyada)
    structure.add_constraint(nodes[0], ['ux', 'uy', 'uz', 'rx']) # Apoyo fijo
    structure.add_constraint(nodes[-1], ['uy', 'uz']) # Apoyo móvil


    # 2. Ensamblaje y Análisis Modal (necesario para el amortiguamiento)
    # ------------------------------------------------------------------
    print("2. Realizando análisis modal...")
    K, M = assembler.assemble_global_matrices(structure)
    freqs_hz, modes = modal.modal_analysis(K, M, structure)
    freqs_rad = freqs_hz * 2 * np.pi
    print(f"Primeras 5 frecuencias naturales (Hz): {freqs_hz[:5]}")


    # 3. Definición del Amortiguamiento de Rayleigh
    # ------------------------------------------------------------------
    print("3. Calculando coeficientes de amortiguamiento de Rayleigh...")
    # Objetivo: 2% de amortiguamiento (ζ=0.02) en el modo 1 y 3
    zeta_target = 0.02
    mode_i, mode_j = 0, 2 # Usar el primer y tercer modo

    # Sistema de ecuaciones para alpha y beta
    A = np.array([
        [1, freqs_rad[mode_i]**2],
        [1, freqs_rad[mode_j]**2]
    ])
    B = np.array([
        2 * zeta_target * freqs_rad[mode_i],
        2 * zeta_target * freqs_rad[mode_j]
    ])
    alpha, beta = np.linalg.solve(A, B)
    print(f"Coeficientes calculados: alpha={alpha:.4f}, beta={beta:.6f}")

    # Construir matriz de amortiguamiento
    C = rayleigh_damping_matrix(M, K, alpha, beta)


    # 4. Definición de la Carga y el Análisis
    # ------------------------------------------------------------------
    print("4. Definiendo la carga del motor y los parámetros de análisis...")
    # Parámetros del motor desbalanceado
    motor_node_index = len(nodes) // 2  # Colocar el motor en el nodo central
    unbalanced_mass_product = 1.0  # kg*m (producto de masa excéntrica y radio)
    force_direction_dof = 2 # Aplicar fuerza en dirección Z (vertical)

    # Crear el vector de dirección de la fuerza
    num_dofs = K.shape[0]
    F_direction = np.zeros(num_dofs)
    F_direction[motor_node_index * 6 + force_direction_dof] = 1.0

    # Rango de frecuencias para el análisis
    # Para este ejemplo, solo nos interesa 15 Hz
    target_freq_hz = 15.0
    freq_range = np.array([target_freq_hz])


    # 5. Ejecución del Análisis de Respuesta en Frecuencia
    # ------------------------------------------------------------------
    print("5. Ejecutando el análisis de respuesta en frecuencia...")
    complex_displacements = direct_frequency_response(
        K=K,
        M=M,
        C=C,
        force_vector_amplitude=F_direction,
        frequency_range_hz=freq_range,
        is_unbalanced_force=True,
        unbalanced_mass_product=unbalanced_mass_product
    )


    # 6. Post-procesamiento y Generación de Tabla de Velocidades
    # ------------------------------------------------------------------
    print("6. Generando tabla de velocidades para nodos de interés...")
    
    # Nodos que quieres inspeccionar (índices de nodo)
    nodes_of_interest = [1, 2, 3, 4, 5, 6, 7, 8, 9] 

    # Extraer la respuesta a la frecuencia objetivo (en nuestro caso, la única calculada)
    U_complex = complex_displacements[0]
    omega = 2 * np.pi * target_freq_hz

    # Calcular velocidades complejas: V = i*ω*U
    V_complex = 1j * omega * U_complex

    # Calcular amplitudes de velocidad en m/s
    V_peak_mps = np.abs(V_complex)
    V_rms_mps = V_peak_mps / np.sqrt(2)

    # Convertir a mm/s
    V_peak_mmps = V_peak_mps * 1000
    V_rms_mmps = V_rms_mps * 1000

    # Imprimir la cabecera de la tabla
    print("\n--- VELOCIDADES DE VIBRACIÓN A {:.2f} Hz ---".format(target_freq_hz))
    print("{:<5} | {:^20} | {:^20}".format("Punto", "Vrms [mm/s]", "Vpk [mm/s]"))
    print("{:<5} | {:^6} {:^6} {:^6} | {:^6} {:^6} {:^6}".format("", "X", "Y", "Z", "X", "Y", "Z"))
    print("-" * 51)

    # Imprimir los resultados para cada nodo de interés
    for node_idx in nodes_of_interest:
        # Índices de los grados de libertad de traslación (ux, uy, uz)
        dof_x = node_idx * 6 + 0
        dof_y = node_idx * 6 + 1
        dof_z = node_idx * 6 + 2

        # Extraer valores
        vrms_vals = [V_rms_mmps[dof_x], V_rms_mmps[dof_y], V_rms_mmps[dof_z]]
        vpk_vals = [V_peak_mmps[dof_x], V_peak_mmps[dof_y], V_peak_mmps[dof_z]]

        print("{:<5} | {:>6.2f} {:>6.2f} {:>6.2f} | {:>6.2f} {:>6.2f} {:>6.2f}".format(
            node_idx,
            vrms_vals[0], vrms_vals[1], vrms_vals[2],
            vpk_vals[0], vpk_vals[1], vpk_vals[2]
        ))

if __name__ == '__main__':
    run_frequency_sweep_example()

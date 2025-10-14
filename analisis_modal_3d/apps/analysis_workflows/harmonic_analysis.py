import numpy as np
import importlib.util
import sys
from pathlib import Path

from analisis_modal_3d.apps.model_builder import build_structure_from_data, load_data_from_file
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.analysis.damping import rayleigh_damping_matrix
from analisis_modal_3d.analysis.frequency_response import direct_frequency_response
from analisis_modal_3d.visualization.results_processor import (
    print_velocity_tables
)
from analisis_modal_3d.visualization.static_plotter import plot_deformed_structure



def run(data_file_path):
    print("DEBUG: Inicio de la función run.")
    """
    Orquesta el flujo de trabajo de análisis de respuesta armónica.
    """
    # 1. OBTENER Y CONSTRUIR
    print(f"Cargando datos desde: {data_file_path}")
    input_data = load_data_from_file(data_file_path)
    settings = input_data['analysis_settings']
    structure, node_coords = build_structure_from_data(input_data)

    # 2. ANÁLISIS MODAL (necesario para el amortiguamiento de Rayleigh)
    print("\nIniciando análisis...")
    K, M = assemble_global_matrices(structure)
    try:
        num_modes = settings['modal_analysis']['num_modes']
        freqs, _, _ = modal_analysis(K, M, structure, num_modes=num_modes)
    except Exception as e:
        print(f"Error crítico durante el análisis modal: {e}")
        return

    # 3. ANÁLISIS DE RESPUESTA EN FRECUENCIA
    print("\nIniciando análisis de respuesta en frecuencia...")
    
    # Coeficientes de amortiguamiento de Rayleigh
    damping_settings = settings['damping']
    zeta_target = damping_settings['zeta_target']
    mode_i, mode_j = [m - 1 for m in damping_settings['rayleigh_modes']] # Convertir a índice base 0
    
    freqs_rad = freqs * 2 * np.pi
    A = np.array([[1, freqs_rad[mode_i]**2], [1, freqs_rad[mode_j]**2]])
    B = np.array([2 * zeta_target * freqs_rad[mode_i], 2 * zeta_target * freqs_rad[mode_j]])
    alpha, beta = np.linalg.solve(A, B)
    C = rayleigh_damping_matrix(M, K, alpha, beta)
    print(f"Coeficientes de amortiguamiento: alpha={alpha:.4f}, beta={beta:.6f}")

    # Definición de la fuerza desbalanceada del motor
    freq_resp_settings = settings['frequency_response']
    force_settings = freq_resp_settings['unbalanced_force']
    mass_node_id = input_data['masses']['node_id']
    motor_node_index = mass_node_id - 1
    
    m_unbal = force_settings['mass']
    e_m = force_settings['eccentricity_mm'] / 1000
    unbalanced_mass_product = m_unbal * e_m
    
    F_direction = np.zeros(K.shape[0], dtype=np.complex128)
    F_direction[motor_node_index * 6 + 2] = 1.0  # Dirección Z
    F_direction[motor_node_index * 6 + 1] = 1.0j # Dirección Y (desfasada 90°)

    # Frecuencias para el análisis
    freq_range_hz = np.array(freq_resp_settings['freq_range_hz'])

    # Ejecución del análisis armónico
    complex_displacements = direct_frequency_response(
        K=K, M=M, C=C,
        force_vector_amplitude=F_direction,
        frequency_range_hz=freq_range_hz,
        is_unbalanced_force=True,
        unbalanced_mass_product=unbalanced_mass_product
    ).T # Transponer para que sea (num_dofs, num_frequencies)

    # 4. POST-PROCESAMIENTO DE RESULTADOS
    nodes_of_interest = settings['post_processing']['nodes_of_interest']
    print_velocity_tables(complex_displacements, freq_range_hz, nodes_of_interest)

    # Visualización de la deformación para todas las frecuencias
    print("\nVisualizando deformaciones para cada frecuencia...")
    for i, freq in enumerate(freq_range_hz):
        displacement_for_freq = complex_displacements[:, i]
        
        # Calcular un factor de escala adaptativo para la visualización de esta frecuencia
        max_disp_amplitude_for_freq = np.max(np.abs(displacement_for_freq))
        
        all_coords = np.array([node.coords for node in structure.nodes])
        max_dim = np.max(all_coords, axis=0)
        min_dim = np.min(all_coords, axis=0)
        structure_length = np.max(max_dim - min_dim) # La dimensión más larga de la estructura

        target_visual_ratio = 0.05 # Queremos que la deformación máxima sea el 5% de la longitud de la estructura
        if max_disp_amplitude_for_freq > 1e-9: # Evitar división por cero o escalado infinito para deformaciones muy pequeñas
            adaptive_scale_factor = (structure_length * target_visual_ratio) / max_disp_amplitude_for_freq
            adaptive_scale_factor = min(adaptive_scale_factor, 1000.0) 
        else:
            adaptive_scale_factor = 0.0 # No hay deformación, no escalar

        print(f"  - Frecuencia: {freq:.2f} Hz, Amplitud Máxima: {max_disp_amplitude_for_freq:.6e} m, Factor de Escala: {adaptive_scale_factor:.2f}")

        plot_deformed_structure(
            structure,
            np.real(displacement_for_freq), # Usar la parte real para la visualización estática
            scale_factor=adaptive_scale_factor,
            title=f"Deformación en {freq:.2f} Hz",
            mass_node_id=mass_node_id
        )
    
    print("\nFlujo de trabajo completado.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run harmonic analysis workflow.")
    parser.add_argument("data_file", type=str, help="Path to the data file (e.g., bailey_bridge_data.py).")
    args = parser.parse_args()

    run(args.data_file)

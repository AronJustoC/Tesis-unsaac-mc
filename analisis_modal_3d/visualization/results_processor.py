"""
Módulo para el post-procesamiento y visualización de resultados del análisis.

Contiene funciones para:
- Graficar la estructura con información relevante.
- Imprimir tablas de resultados modales.
- Visualizar y animar los modos de vibración.
- Imprimir tablas de resultados de respuesta en frecuencia (velocidades).
"""
import numpy as np

# Usamos importaciones relativas dentro del mismo paquete 'visualization'
from .structure_plotter import plot_structure_with_info
from .plotter import plot_mode_shape

def plot_structure_diagram(structure, nodes_of_interest_ids, mass_node_id):
    """
    Grafica la estructura y resalta nodos de interés y la ubicación de la masa.
    """
    print("\nGraficando la estructura...")
    
    node_coords_map = {node.id: node for node in structure.nodes}
    
    coords_to_highlight = [node_coords_map[node_id].coords for node_id in nodes_of_interest_ids if node_id in node_coords_map]
    mass_coords = [node_coords_map[mass_node_id].coords] if mass_node_id in node_coords_map else None

    plot_structure_with_info(
        structure,
        title="Estructura Bailey Escalado con Pasadores",
        highlight_coords=coords_to_highlight,
        highlight_label="Nodos de Medición (Velocidad)",
        mass_node_coords=mass_coords
    )
    print("Gráfico de la estructura generado.")

def print_modal_results(freqs, mass_participation, num_modes_to_print=10):
    """
    Imprime una tabla con los resultados del análisis modal.
    """
    print("\n--- Resultados del Análisis Modal ---")
    print(f"Primeras {num_modes_to_print} frecuencias naturales (Hz): {freqs[:num_modes_to_print]}")
    print("\nFactores de participación de masa (%):")
    print("Modo | Frec (Hz) | X    | Y    | Z")
    print("------------------------------------")
    for i in range(min(len(freqs), num_modes_to_print)):
        print(f"{i+1:<4} | {freqs[i]:<9.2f} | {mass_participation[i, 0]:<8.2e} | {mass_participation[i, 1]:<8.2e} | {mass_participation[i, 2]:<8.2e}")

def visualize_mode_shapes(structure, freqs, modes, num_modes_to_plot=5):
    """
    Muestra los gráficos interactivos de los modos de vibración.
    """
    print(f"\n--- Visualización Interactiva de {num_modes_to_plot} Modos de Vibración ---")
    print("NOTA: Cierre la ventana del gráfico para continuar.")

    for i in range(min(len(freqs), num_modes_to_plot)):
        title = f"Modo de Vibración {i+1} ({freqs[i]:.2f} Hz)"
        print(f"\nMostrando gráfico interactivo para el Modo {i+1}...")
        try:
            plot_mode_shape(structure=structure, mode_vector=modes[:, i], title=title)
        except Exception as e:
            print(f"  No se pudo mostrar el gráfico interactivo. Error: {e}")
            break
    print("\nVisualización de modos completada.")

def print_velocity_tables(complex_displacements, freqs_of_interest_hz, nodes_of_interest_ids):
    """
    Calcula e imprime las tablas de velocidades (RMS y Pico).
    """
    print("\n--- Resultados de Respuesta en Frecuencia (Velocidad) ---")
    
    node_indices = [node_id - 1 for node_id in nodes_of_interest_ids]

    for i, f_target in enumerate(freqs_of_interest_hz):
        omega = 2 * np.pi * f_target
        # U_complex ahora es (num_dofs, num_frequencies), así que seleccionamos la columna de la frecuencia
        U_complex_at_freq = complex_displacements[:, i]
        V_complex = 1j * omega * U_complex_at_freq
        V_peak_mmps = np.abs(V_complex) * 1000
        V_rms_mmps = V_peak_mmps / np.sqrt(2)

        print(f"\nVELOCIDADES DE VIBRACIÓN A {f_target:.0f} Hz")
        print("{:<5} {:^18} {:^18}".format("Punto", "Vrms [mm/s]", "Vpk [mm/s]"))
        print("{:<5} {:^6} {:^6} {:^6} {:^6} {:^6} {:^6}".format("", "X", "Y", "Z", "X", "Y", "Z"))
        print("-" * 70)

        for node_id in nodes_of_interest_ids:
            # Los DOFs son 0-indexed para ux, uy, uz, rx, ry, rz
            # Asumimos que los nodos de interés son 1-indexed en el input_data
            node_base_dof = (node_id - 1) * 6
            
            # Extraer valores para X, Y, Z traslación
            vrms_vals = [
                V_rms_mmps[node_base_dof + 0], # ux
                V_rms_mmps[node_base_dof + 1], # uy
                V_rms_mmps[node_base_dof + 2]  # uz
            ]
            vpk_vals = [
                V_peak_mmps[node_base_dof + 0],
                V_peak_mmps[node_base_dof + 1],
                V_peak_mmps[node_base_dof + 2]
            ]

            print("{:<5} | {:>6.2f} {:>6.2f} {:>6.2f} | {:>6.2f} {:>6.2f} {:>6.2f}".format(
                node_id,
                vrms_vals[0], vrms_vals[1], vrms_vals[2],
                vpk_vals[0], vpk_vals[1], vpk_vals[2]
            ))
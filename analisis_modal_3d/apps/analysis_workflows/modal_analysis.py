import numpy as np
import importlib.util
import sys
from pathlib import Path

from analisis_modal_3d.apps.model_builder import build_structure_from_data
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
from analisis_modal_3d.analysis.modal import modal_analysis
from analisis_modal_3d.visualization.results_processor import (
    print_modal_results,
    visualize_mode_shapes
)

def load_data_from_file(data_file_path):
    """
    Carga dinámicamente la función get_structure_data de un archivo de datos.
    """
    try:
        path = Path(data_file_path).resolve()
        spec = importlib.util.spec_from_file_location("data_module", path)
        data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data_module)
        return data_module.get_structure_data()
    except Exception as e:
        print(f"Error al cargar el archivo de datos '{data_file_path}': {e}")
        sys.exit(1)

def run(data_file_path):
    """
    Orquesta el flujo de trabajo de análisis modal.
    """
    # 1. OBTENER Y CONSTRUIR EL MODELO
    print(f"Cargando datos desde: {data_file_path}")
    input_data = load_data_from_file(data_file_path)
    settings = input_data['analysis_settings']
    structure, node_coords = build_structure_from_data(input_data)

    # 2. ENSAMBLAR MATRICES GLOBALES
    K, M = assemble_global_matrices(structure)

    # 3. EJECUTAR ANÁLISIS MODAL
    print("\nIniciando análisis modal...")
    try:
        num_modes = settings['modal_analysis']['num_modes']
        freqs, modes, mass_participation = modal_analysis(K, M, structure, num_modes=num_modes)
        
        # 4. MOSTRAR RESULTADOS
        visualize_mode_shapes(structure, freqs, modes, num_modes_to_plot=settings['post_processing']['num_modes_to_plot'])
    except Exception as e:
        print(f"Error crítico durante el análisis modal: {e}")
        return

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run modal analysis workflow.")
    parser.add_argument("data_file", type=str, help="Path to the data file (e.g., bailey_bridge_data.py).")
    args = parser.parse_args()

    run(args.data_file)
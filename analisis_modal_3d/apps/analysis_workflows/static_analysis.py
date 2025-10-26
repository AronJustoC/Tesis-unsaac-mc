import numpy as np
import importlib.util
import sys
from pathlib import Path

from analisis_modal_3d.apps.model_builder import build_structure_from_data
from analisis_modal_3d.analysis.assembler import assemble_global_matrices
from analisis_modal_3d.analysis.static import static_analysis
from analisis_modal_3d.visualization.static_plotter import plot_deformed_structure


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
    Orquesta el flujo de trabajo de análisis estático.
    """
    # 1. OBTENER Y CONSTRUIR EL MODELO
    print(f"Cargando datos desde: {data_file_path}")
    input_data = load_data_from_file(data_file_path)
    structure, node_coords = build_structure_from_data(input_data)
    print(f"Estructura cargada: {len(structure.nodes)} nodos y {
          len(structure.elements)} elementos.")
    # Verificar las dimensiones de los nodos para confirmar que es 3D
    if structure.nodes:
        first_node_coords = structure.nodes[0].coords
        print(f"Coordenadas del primer nodo (X, Y, Z): {first_node_coords}")
        if len(first_node_coords) == 3 and any(c != 0 for c in first_node_coords):
            print(
                "Confirmado: La estructura tiene coordenadas 3D y no es plana en el origen.")
        else:
            print(
                "Advertencia: Las coordenadas del primer nodo sugieren una estructura 2D o plana en el origen.")

    # 2. ENSAMBLAR MATRIZ DE RIGIDEZ
    # No necesitamos la matriz de masa para estático
    K, _ = assemble_global_matrices(structure)

    # 3. DEFINIR EL VECTOR DE FUERZAS
    # La definición de la fuerza ahora debería venir de los datos de entrada
    num_dofs = K.shape[0]
    F = np.zeros(num_dofs)

    if 'static_loads' in input_data and input_data['static_loads']:
        print("Aplicando cargas estáticas definidas en el archivo de datos.")
        for load in input_data['static_loads']:
            node_id = load['node_id']
            force_vector = load['force']
            # Asegurarse de que el nodo exista en el mapa de coordenadas
            if node_id in node_coords:
                node_index = structure.nodes.index(node_coords[node_id])
                F[node_index * 6: node_index * 6 + 6] += force_vector
                print(
                    f"  - Carga aplicada en el nodo {node_id}: {force_vector}")
            else:
                print(f"Advertencia: El nodo {
                      node_id} definido en 'static_loads' no existe en la estructura.")
    else:
        print("Advertencia: No se encontraron 'static_loads' en el archivo de datos. El análisis se ejecutará sin cargas externas.")

    # 4. EJECUTAR ANÁLISIS ESTÁTICO
    u = static_analysis(K, F)

    if u is not None:
        # 5. VISUALIZAR RESULTADOS
        print("\nAnálisis estático finalizado.")

        # Calcular fuerzas axiales para cada elemento
        axial_forces = []
        for element in structure.elements:
            axial_forces.append(element.get_axial_force(u))

        # Intentar obtener el factor de escala de los datos, con un valor por defecto
        scale_factor = input_data.get('analysis_settings', {}).get(
            'post_processing', {}).get('scale_factor', 50)

        plot_deformed_structure(structure, u, scale_factor=scale_factor,
                                mass_node_id=input_data['masses']['node_id'], axial_forces=axial_forces)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run static analysis workflow.")
    parser.add_argument("data_file", type=str, nargs='?', default='analisis_modal_3d/apps/data/bailey_bridge_data.py',
                        help="Path to the data file (e.g., bailey_bridge_data.py). Defaults to bailey_bridge_data.py if not provided.")
    args = parser.parse_args()

    run(args.data_file)

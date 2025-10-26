import importlib.util
import sys
from pathlib import Path

from analisis_modal_3d.structures.structure import Structure


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


def build_structure_from_data(data):
    """
    Construye el objeto Structure a partir del diccionario de datos de entrada.
    """
    print("Construyendo la estructura a partir de los datos...")
    structure = Structure()
    node_coords = {}

    # Añadir nodos (y convertir coordenadas de mm a m)
    for node_data in data['nodes']:
        node_id, x, y, z = node_data
        node_coords[node_id] = structure.add_node(x / 1000, y / 1000, z / 1000)

    # Añadir masa puntual
    if 'masses' in data:
        mass_data = data['masses']
        mass_node_id = mass_data['node_id']
        if mass_node_id in node_coords:
            node = node_coords[mass_node_id]
            node.mass += mass_data['mass']
            print(f"Añadida masa de {
                  mass_data['mass']:.2f} kg al nodo {node.id}")

    # Añadir elementos
    for el_data in data['elements']:
        n1_id, n2_id, sec_name, mat_name = el_data
        node1 = node_coords[n1_id]
        node2 = node_coords[n2_id]

        # Lógica para material modificado en elementos horizontales
        if node1.y == node2.y and data["sections"][sec_name] != "H420x180":
            mat_name = "ASTM-A36_modificado"

        structure.add_element(
            node1, node2,
            data['sections'][sec_name],
            data['materials'][mat_name]
        )

    # Añadir restricciones
    for node_id, dofs in data['constraints'].items():
        structure.add_constraint(node_coords[node_id], dofs)

    print("Estructura construida exitosamente.")
    return structure, node_coords
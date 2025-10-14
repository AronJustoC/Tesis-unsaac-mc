import numpy as np

from analisis_modal_3d.structures.structure import Structure


def assemble_global_matrices(structure: Structure):
    """Ensambla las matrices de rigidez y masa globales de la estructura.

    Esta función itera sobre todos los elementos de la estructura y ensambla
    sus matrices de rigidez y masa globales en las matrices globales
    correspondientes de la estructura. Los grados de libertad (DOFs)
    restringidos se incluyen en las matrices ensambladas.

    Args:
        structure (Structure): El objeto Structure que contiene los nodos y
                               elementos de la estructura.

    Returns:
        tuple[np.ndarray, np.ndarray]: Una tupla que contiene:
            - K (np.ndarray): La matriz de rigidez global ensamblada.
            - M (np.ndarray): La matriz de masa global ensamblada.
    """
    num_dofs = structure.num_dofs
    K = np.zeros((num_dofs, num_dofs))
    M = np.zeros((num_dofs, num_dofs))

    for element in structure.elements:
        k_global = element.k_global
        m_global = element.m_global

        # Obtener índices de DOFs del elemento
        dof_indices = []
        for node in element.nodes:
            dof_indices.extend(node.dofs)

        # Ensamblar en matrices globales
        for i, dof_i in enumerate(dof_indices):
            for j, dof_j in enumerate(dof_indices):
                K[dof_i, dof_j] += k_global[i, j]
                M[dof_i, dof_j] += m_global[i, j]

    # Agregar masas nodales a la matriz de masa global
    for node in structure.nodes:
        if node.mass > 0:
            # Añadir masa a los grados de libertad de traslación (ux, uy, uz)
            for i in range(3):
                dof_index = node.dofs[i]
                M[dof_index, dof_index] += node.mass

    print("DEBUG: M diagonal after mass addition (first 100 elements):")
    print(M.diagonal()[:100])

    # Aplicar restricciones (Penalty Method)
    # Un valor grande para la penalización
    penalty_value = 1e12 * np.max(np.abs(K)) # Basado en la rigidez máxima
    if penalty_value == 0: penalty_value = 1e12 # Evitar cero si K es cero

    for node_index, local_dofs_constrained in structure.constraints.items():
        node_obj = structure.nodes[node_index]
        for dof_local_index in local_dofs_constrained:
            dof_global_index = node_obj.dofs[dof_local_index]
            K[dof_global_index, dof_global_index] += penalty_value
            M[dof_global_index, dof_global_index] += penalty_value # También penalizar la masa para evitar problemas numéricos

    return K, M

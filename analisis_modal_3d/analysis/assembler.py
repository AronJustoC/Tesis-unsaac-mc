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

    return K, M  # Matrices completas (sin eliminar restricciones)

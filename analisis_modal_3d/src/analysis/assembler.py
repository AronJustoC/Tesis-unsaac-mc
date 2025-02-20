import numpy as np


def assemble_global_matrices(structure):
    total_dof = len(structure.nodes) * 6
    K = np.zeros((total_dof, total_dof))
    M = np.zeros((total_dof, total_dof))

    for element in structure.elements:
        # Obtencion de indeces de DOF
        dofs = element.nodes[0].dofs + element.nodes[1].dofs

import numpy as np
from .assembler import assemble_global_matrices
from scipy.linalg import eigh

def is_positive_definite(matrix):
    """Verifica si una matriz es definida positiva."""
    return np.all(np.linalg.eigvals(matrix) > 0)

def modal_analysis(structure, num_modes=5, constrained_dofs=None):
    """
    Realiza análisis modal expandiendo modos al espacio completo.
    """
    # Ensamblar matrices completas
    K_full, M_full = assemble_global_matrices(structure)
    
    # Obtener DOFs libres
    all_dofs = np.arange(K_full.shape[0])
    free_dofs = np.setdiff1d(all_dofs, constrained_dofs)
    
    # Reducir matrices
    K_red = K_full[np.ix_(free_dofs, free_dofs)]
    M_red = M_full[np.ix_(free_dofs, free_dofs)]
    
    # Resolver autovalores
    eigvals, eigvecs_red = eigh(K_red, M_red, subset_by_index=(0, num_modes-1))
    
    # Expandir modos al espacio completo
    mode_shapes = np.zeros((K_full.shape[0], num_modes))
    mode_shapes[free_dofs, :] = eigvecs_red[:, :num_modes]
    
    # Calcular frecuencias
    frequencies = np.sqrt(np.abs(eigvals)) / (2 * np.pi)
    
    return frequencies, mode_shapes
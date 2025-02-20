import numpy as np
from .assembler import assemble_global_matrices
from scipy.linalg import eigh


def modal_analysis(structure, num_modes=5):
    K, M = assemble_global_matrices(structure)

    # Resolver problema de autovalores
    eigvals, eigvecs = eigh(K, M, subset_by_index=(0, num_modes - 1))

    # Calcular frecuencias
    frequencies = np.sqrt(eigvals) / (2 * np.pi)

    # Normalizar modos
    for i in range(eigvecs.shape[1]):
        eigvecs[:, i] /= np.sqrt(eigvecs[:, i] @ M @ eigvecs[:, i])

    return frequencies, eigvecs

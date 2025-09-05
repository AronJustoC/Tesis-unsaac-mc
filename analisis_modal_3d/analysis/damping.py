"""
Módulo para calcular la matriz de amortiguamiento de la estructura.
"""
import numpy as np

def rayleigh_damping_matrix(M: np.ndarray, K: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """
    Calcula la matriz de amortiguamiento de Rayleigh (C).

    El amortiguamiento de Rayleigh es una forma de amortiguamiento viscoso proporcional
    a la masa y la rigidez del sistema.

    Args:
        M (np.ndarray): Matriz de masa global de la estructura.
        K (np.ndarray): Matriz de rigidez global de la estructura.
        alpha (float): Coeficiente de amortiguamiento proporcional a la masa.
        beta (float): Coeficiente de amortiguamiento proporcional a la rigidez.

    Returns:
        np.ndarray: Matriz de amortiguamiento de Rayleigh (C).
    """
    C = alpha * M + beta * K
    return C

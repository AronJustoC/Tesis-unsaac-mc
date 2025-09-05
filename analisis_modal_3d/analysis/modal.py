import numpy as np
from scipy.linalg import eigh


def modal_analysis(
    K: np.ndarray,
    M: np.ndarray,
    structure: "Structure",
    num_modes=6,
):
    """Realiza un análisis modal usando un solucionador de valores propios denso.

    Este método es robusto y calcula todos los modos posibles, devolviendo los
    primeros `num_modes`.

    Args:
        K (np.ndarray): Matriz de rigidez global.
        M (np.ndarray): Matriz de masa global.
        structure (Structure): El objeto Structure para obtener las restricciones.
        num_modes (int): Número de modos a calcular.

    Returns:
        tuple[np.ndarray, np.ndarray]: Tupla con las frecuencias (Hz) y las formas modales.
    """
    # Obtener los grados de libertad restringidos
    constrained_dofs = structure.get_constrained_dofs()
    free_dofs = np.setdiff1d(np.arange(K.shape[0]), constrained_dofs)

    # Extraer submatrices para los grados de libertad libres
    # y convertirlas a formato denso para el solucionador eigh.
    try:
        K_red_dense = K[free_dofs, :][:, free_dofs].toarray()
        M_red_dense = M[free_dofs, :][:, free_dofs].toarray()
    except AttributeError:
        # Las matrices ya son densas
        K_red_dense = K[free_dofs, :][:, free_dofs]
        M_red_dense = M[free_dofs, :][:, free_dofs]

    # Resolver el problema de valores propios generalizado: K*v = w^2*M*v
    # eigh es para matrices hermitianas y devuelve los valores propios en orden ascendente.
    # Se añade una pequeña cantidad a la diagonal de la matriz de masa para asegurar que sea positiva definida.
    M_red_dense += np.eye(M_red_dense.shape[0]) * 1e-6
    eigvals, eigvecs_red = eigh(K_red_dense, M_red_dense)

    # Tomar el número de modos solicitado (los más bajos)
    eigvals = eigvals[:num_modes]
    eigvecs_red = eigvecs_red[:, :num_modes]

    # Reconstruir los vectores propios en el tamaño original de la estructura
    mode_shapes = np.zeros((K.shape[0], num_modes))
    mode_shapes[free_dofs, :] = eigvecs_red

    # Normalizar los modos (opcional, pero buena práctica)
    for i in range(num_modes):
        norm = np.linalg.norm(mode_shapes[:, i])
        if norm > 1e-9:
            mode_shapes[:, i] /= norm

    # Calcular frecuencias en Hz desde los valores propios (w^2)
    # Se manejan valores propios negativos pequeños que pueden surgir de errores numéricos
    frequencies = np.sqrt(np.maximum(eigvals, 0)) / (2 * np.pi)

    return frequencies, mode_shapes
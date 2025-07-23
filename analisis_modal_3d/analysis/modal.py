import numpy as np
from scipy.sparse import eye as sparse_eye
from scipy.sparse.linalg import eigsh

from analisis_modal_3d.analysis.assembler import assemble_global_matrices


def modal_analysis(
    structure,
    num_modes=5,
    constrained_dofs=None,
    solver="lanczos",
    sigma=1.0,
    max_iter=1000,
    tol=1e-8,
    shift=0.1,
    regularization=1e-6,
):
    """Realiza un análisis modal para determinar las frecuencias naturales y las formas modales de una estructura.

    Esta función ensambla las matrices de rigidez y masa globales, aplica
    restricciones de grados de libertad y resuelve el problema de valores
    propios generalizado para obtener las frecuencias y modos de vibración.

    Args:
        structure (Structure): El objeto Structure que contiene los nodos y
                               elementos de la estructura.
        num_modes (int, optional): El número de modos de vibración a calcular.
                                   Por defecto es 5.
        constrained_dofs (list[int] or None, optional): Una lista de índices de
                                                        grados de libertad que
                                                        están restringidos (fijos).
                                                        Si es None, no se aplican
                                                        restricciones.
                                                        Por defecto es None.
        solver (str, optional): El método de solución a utilizar para el problema
                                de valores propios. Puede ser 'lanczos' o
                                'shift-invert'. Por defecto es 'lanczos'.
        sigma (float, optional): El desplazamiento espectral para métodos iterativos.
                                 Por defecto es 1.0.
        max_iter (int, optional): El número máximo de iteraciones para el solver.
                                  Por defecto es 1000.
        tol (float, optional): La tolerancia de convergencia para el solver.
                               Por defecto es 1e-8.
        shift (float, optional): Un valor de desplazamiento inicial utilizado en
                                 caso de que el solver falle con el sigma inicial.
                                 Por defecto es 0.1.
        regularization (float, optional): Un factor de regularización aplicado a
                                          las matrices de rigidez y masa para
                                          mejorar la estabilidad numérica.
                                          Por defecto es 1e-6.

    Returns:
        tuple[np.ndarray, np.ndarray]: Una tupla que contiene:
            - frequencies (np.ndarray): Un array de las frecuencias naturales
                                        de la estructura en Hz.
            - mode_shapes (np.ndarray): Una matriz donde cada columna representa
                                        una forma modal (vector propio).
    """
    # Ensamblar matrices globales con formato disperso
    K, M = assemble_global_matrices(structure)

    # Aplicar regularización numérica
    K_reg = K + regularization * sparse_eye(K.shape[0])
    M_reg = M + regularization * sparse_eye(M.shape[0])

    # Manejar grados de libertad restringidos
    free_dofs = np.setdiff1d(np.arange(K.shape[0]), constrained_dofs)

    # Extraer submatrices libres
    K_red = K_reg[free_dofs, :][:, free_dofs]
    M_red = M_reg[free_dofs, :][:, free_dofs]

    # Configurar parámetros del solver
    solver_params = {
        "k": num_modes,
        "sigma": sigma,
        "maxiter": max_iter,
        "tol": tol,
        "which": "LM",
        "mode": "buckling" if solver == "shift-invert" else "normal",
    }

    # Resolver problema de autovalores generalizado
    try:
        eigvals, eigvecs_red = eigsh(K_red, M=M_red, **solver_params)
    except np.linalg.LinAlgError:
        # Reintentar con desplazamiento diferente si falla
        solver_params["sigma"] = shift
        eigvals, eigvecs_red = eigsh(K_red, M=M_red, **solver_params)

    # Expandir vectores modales al espacio completo
    mode_shapes = np.zeros((K.shape[0], num_modes))
    mode_shapes[free_dofs, :] = eigvecs_red

    # Calcular frecuencias naturales (Hz)
    frequencies = np.sqrt(np.abs(eigvals)) / (2 * np.pi)

    return frequencies, mode_shapes

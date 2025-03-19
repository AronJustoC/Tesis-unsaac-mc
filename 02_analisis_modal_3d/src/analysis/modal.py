import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse import eye as sparse_eye
from .assembler import assemble_global_matrices


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
    """
    Análisis modal robusto para grandes sistemas con parámetros avanzados.

    Args:
        structure: Objeto de la estructura
        num_modes: Número de modos a calcular
        constrained_dofs: Grados de libertad restringidos
        solver: Método de solución ('lanczos', 'shift-invert')
        sigma: Desplazamiento espectral para métodos iterativos
        max_iter: Máximo de iteraciones
        tol: Tolerancia de convergencia
        shift: Valor de desplazamiento inicial
        regularization: Factor de regularización para matrices

    Returns:
        frequencies: Frecuencias naturales (Hz)
        mode_shapes: Vectores modales
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


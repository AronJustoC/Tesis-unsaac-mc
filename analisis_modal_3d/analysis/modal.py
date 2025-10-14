import numpy as np
from scipy.linalg import eigh


def modal_analysis(
    K: np.ndarray,
    M: np.ndarray,
    structure: "Structure",
    num_modes=6,
):
    """Realiza un análisis modal y calcula los factores de participación de masa.

    Args:
        K (np.ndarray): Matriz de rigidez global.
        M (np.ndarray): Matriz de masa global.
        structure (Structure): El objeto Structure para obtener las restricciones.
        num_modes (int): Número de modos a calcular.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Frecuencias (Hz), 
                                                   formas modales y 
                                                   factores de participación de masa (%).
    """
    num_dofs = K.shape[0]
    constrained_dofs = structure.get_constrained_dofs()
    free_dofs = np.setdiff1d(np.arange(num_dofs), constrained_dofs)

    try:
        K_red_dense = K[free_dofs, :][:, free_dofs].toarray()
        M_red_dense = M[free_dofs, :][:, free_dofs].toarray()
    except AttributeError:
        K_red_dense = K[free_dofs, :][:, free_dofs]
        M_red_dense = M[free_dofs, :][:, free_dofs]

    M_red_dense += np.eye(M_red_dense.shape[0]) * 1e-6
    eigvals, eigvecs_red = eigh(K_red_dense, M_red_dense)

    eigvals = eigvals[:num_modes]
    eigvecs_red = eigvecs_red[:, :num_modes]

    mode_shapes = np.zeros((num_dofs, num_modes))
    mode_shapes[free_dofs, :] = eigvecs_red

    # Normalización de masa modal a 1 (M_modal = I)
    for i in range(num_modes):
        phi_i = mode_shapes[:, i]
        m_modal = phi_i.T @ M @ phi_i
        if m_modal > 1e-9:
            mode_shapes[:, i] /= np.sqrt(m_modal)

    frequencies = np.sqrt(np.maximum(eigvals, 0)) / (2 * np.pi)

    # --- Cálculo de Participación de Masa ---
    mass_participation = np.zeros((num_modes, 3)) # X, Y, Z
    
    # 1. Vector de influencia (R)
    R = np.zeros((num_dofs, 3))
    R[0::6, 0] = 1 # Dirección X
    R[1::6, 1] = 1 # Dirección Y
    R[2::6, 2] = 1 # Dirección Z

    # 2. Masa total en cada dirección
    M_diag = M.diagonal()
    total_mass_X = np.sum(M_diag[0::6])
    total_mass_Y = np.sum(M_diag[1::6])
    total_mass_Z = np.sum(M_diag[2::6])
    total_mass_vector = np.array([total_mass_X, total_mass_Y, total_mass_Z])

    # 3. Factor de participación modal (L)
    L = mode_shapes.T @ M @ R # Shape: (num_modes, 3)

    # 4. Masa modal efectiva (M_eff = L^2, ya que M_modal es 1)
    effective_modal_mass = L**2

    # 5. Porcentaje de participación
    for i in range(3):
        if total_mass_vector[i] > 1e-9:
            mass_participation[:, i] = (effective_modal_mass[:, i] / total_mass_vector[i]) * 100

    print(f"DEBUG: mass_participation shape: {mass_participation.shape}")
    print(f"DEBUG: mass_participation (first 5 modes):\n{mass_participation[:5]}")

    return frequencies, mode_shapes, mass_participation
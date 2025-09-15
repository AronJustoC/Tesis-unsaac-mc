"""
Módulo para el análisis de respuesta en frecuencia de estructuras.
"""
import numpy as np
from tqdm import tqdm

def direct_frequency_response(
    K: np.ndarray,
    M: np.ndarray,
    C: np.ndarray,
    force_vector_amplitude: np.ndarray,
    frequency_range_hz: np.ndarray,
    is_unbalanced_force: bool = False,
    unbalanced_mass_product: float = 0.0
) -> np.ndarray:
    """
    Calcula la respuesta en estado estacionario (amplitudes y fases) de una estructura
    a lo largo de un rango de frecuencias utilizando el método directo.

    Resuelve la ecuación: (K - ω^2*M + i*ω*C) * U(ω) = F(ω)

    Args:
        K (np.ndarray): Matriz de rigidez global.
        M (np.ndarray): Matriz de masa global.
        C (np.ndarray): Matriz de amortiguamiento global.
        force_vector_amplitude (np.ndarray): Vector de amplitud de la fuerza (F0).
            Si is_unbalanced_force es True, este vector indica la DIRECCIÓN de la fuerza,
            y su magnitud se ignora.
        frequency_range_hz (np.ndarray): Vector de frecuencias a analizar (en Hz).
        is_unbalanced_force (bool): Si es True, la magnitud de la fuerza será proporcional
            al cuadrado de la frecuencia (F = (m*e) * ω^2).
        unbalanced_mass_product (float): El producto de la masa desbalanceada por la
            excentricidad (m*e). Requerido si is_unbalanced_force es True.

    Returns:
        np.ndarray: Matriz de respuestas complejas U(ω). Cada fila corresponde a una
                    frecuencia, cada columna a un grado de libertad.
    """
    num_dofs = K.shape[0]
    num_freqs = len(frequency_range_hz)
    
    # Normalizar el vector de dirección de la fuerza si es necesario
    if is_unbalanced_force:
        norm = np.linalg.norm(force_vector_amplitude)
        if norm > 1e-9:
            force_direction = force_vector_amplitude / norm
        else:
            # Si el vector de fuerza es cero, no hay nada que hacer
            return np.zeros((num_freqs, num_dofs), dtype=np.complex128)
    
    # Array para almacenar los resultados complejos de desplazamiento U(ω)
    complex_displacements = np.zeros((num_freqs, num_dofs), dtype=np.complex128)

    print("Iniciando barrido de frecuencias...")
    for i, freq_hz in enumerate(tqdm(frequency_range_hz, desc="Frequency Sweep")):
        omega = 2 * np.pi * freq_hz

        # Construir la matriz de impedancia dinámica Z(ω)
        Z = (K - omega**2 * M) + 1j * (omega * C)

        # Definir el vector de fuerza F(ω)
        if is_unbalanced_force:
            # Fuerza de desbalance: F = (m*e) * ω^2
            force_magnitude = unbalanced_mass_product * omega**2
            F = force_direction * force_magnitude
        else:
            # Fuerza de amplitud constante
            F = force_vector_amplitude

        # Resolver el sistema de ecuaciones lineales Z * U = F
        try:
            U = np.linalg.solve(Z, F)
            complex_displacements[i, :] = U
        except np.linalg.LinAlgError:
            print(f"Advertencia: Matriz singular para la frecuencia {freq_hz:.2f} Hz. La respuesta puede ser infinita (resonancia pura).")
            # Asignar un valor grande o NaN para indicar la resonancia
            complex_displacements[i, :] = np.nan

    print("Barrido de frecuencias completado.")
    return complex_displacements

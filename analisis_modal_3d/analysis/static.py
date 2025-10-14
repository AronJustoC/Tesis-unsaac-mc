
import numpy as np

def static_analysis(K, F):
    """
    Resuelve el problema estático [K]{u} = {F} para encontrar los desplazamientos {u}.

    Args:
        K (np.ndarray): Matriz de rigidez global ensamblada.
        F (np.ndarray): Vector de fuerzas nodales globales.

    Returns:
        np.ndarray: Vector de desplazamientos nodales globales.
    """
    print("Iniciando análisis estático...")
    try:
        # Soluciona el sistema de ecuaciones lineales
        u = np.linalg.solve(K, F)
        print("Análisis estático completado exitosamente.")
        return u
    except np.linalg.LinAlgError:
        print("Error: La matriz de rigidez es singular. La estructura puede ser inestable.")
        # Considera usar np.linalg.pinv (pseudo-inversa) para casos inestables si es apropiado
        # u = np.linalg.pinv(K) @ F
        # print("Se utilizó la pseudo-inversa para encontrar una solución.")
        # return u
        return None

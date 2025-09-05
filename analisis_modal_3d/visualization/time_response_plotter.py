"""
Módulo para visualizar la respuesta en el tiempo de la estructura.
"""
import matplotlib
matplotlib.use('Agg')  # Usar el backend no interactivo Agg
import matplotlib.pyplot as plt
import numpy as np

def plot_time_response(
    time_array: np.ndarray,
    displacement_history: np.ndarray,
    node_index: int,
    dof_index: int,
    title: str = None,
    output_filename: str = None
):
    """
    Grafica el desplazamiento de un grado de libertad (DOF) específico a lo largo del tiempo.

    Args:
        ...
        output_filename (str, optional): Si se proporciona, guarda el gráfico en esta ruta.
                                         Si es None, muestra el gráfico interactivamente.
    """
    # ... (el resto de la función sigue igual)
    ...
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Desplazamiento (m) o Rotación (rad)')
    
    if output_filename:
        plt.savefig(output_filename)
        print(f"Gráfico guardado en: {output_filename}")
    else:
        plt.show()
    
    plt.close() # Cierra la figura para liberar memoria
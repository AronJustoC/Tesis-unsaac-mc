

from analisis_modal_3d.apps.analysis_workflows import static_analysis, modal_analysis, harmonic_analysis
import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
# para permitir importaciones relativas desde fuera del paquete.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main_menu():
    """
    Muestra el menú principal y maneja la selección del usuario.
    """
    # --- CONFIGURACIÓN DEL ARCHIVO DE DATOS ---
    # Modifica esta variable para apuntar a tu propio archivo de datos.
    # La ruta debe ser relativa a la raíz del proyecto.
    data_file = "analisis_modal_3d/apps/data/bailey_bridge_data.py"
    # ------------------------------------------

    data_file_path = os.path.join(project_root, data_file)

    while True:
        print("\n--- Menú Principal de Análisis Estructural ---")
        print(f"Usando archivo de datos: {data_file}")
        print("Seleccione el tipo de análisis que desea realizar:")
        print("1. Análisis Estático")
        print("2. Análisis Modal")
        print("3. Análisis de Respuesta Armónica")
        print("4. Salir")

        choice = input("Ingrese su opción (1-4): ")

        if choice == '1':
            print("\n--- Iniciando Flujo de Trabajo: Análisis Estático ---")
            static_analysis.run(data_file_path)
        elif choice == '2':
            print("\n--- Iniciando Flujo de Trabajo: Análisis Modal ---")
            modal_analysis.run(data_file_path)
        elif choice == '3':
            print("\n--- Iniciando Flujo de Trabajo: Análisis de Respuesta Armónica ---")
            harmonic_analysis.run(data_file_path)
        elif choice == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main_menu()

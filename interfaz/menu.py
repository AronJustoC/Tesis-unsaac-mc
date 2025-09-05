import os
import importlib.util
import multiprocessing
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info
from analisis_modal_3d.visualization.plotter import animate_mode_shape
from analisis_modal_3d.visualization.plotterPyVista import animate_harmonic_response

def plot_in_separate_process(structure):
    """Función auxiliar para ejecutar el plotter en un proceso separado."""
    plot_structure_with_info(structure)

class AppState:
    """Manages the application state to avoid global variables."""
    def __init__(self):
        self.structure = None
        self.freqs = None
        self.modes = None
        self.harmonic_data = None

    def load_results(self, module):
        """Loads analysis results from a given module."""
        self.structure = getattr(module, 'structure', None)
        self.freqs = getattr(module, 'freqs', None)
        self.modes = getattr(module, 'modes', None)
        self.harmonic_data = getattr(module, 'harmonic_displacement_history', None)
        if self.structure and self.freqs is not None and self.modes is not None:
            print("Ejemplo ejecutado exitosamente. Resultados cargados.")
        else:
            print("El ejemplo no produjo los resultados esperados (estructura, frecuencias, modos).")

class MainMenu:
    """Handles the main user interface and application flow."""
    def __init__(self):
        self.state = AppState()
        self.examples_path = "analisis_modal_3d/examples"

    def _get_validated_input(self, prompt, valid_options):
        while True:
            choice = input(prompt).strip()
            if choice in valid_options:
                return choice
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

    def _get_validated_int_input(self, prompt, min_val, max_val):
        while True:
            try:
                choice = int(input(prompt).strip())
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"Número fuera de rango. Por favor, ingrese un número entre {min_val} y {max_val}.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número.")

    def display_main_menu(self):
        print("\n--- Menú Principal ---")
        print("1. Seleccionar y Ejecutar Ejemplo")
        print("2. Visualizar Estructura con Información")
        print("3. Generar GIFs de Modos de Vibración")
        print("4. Salir")
        return self._get_validated_input("Ingrese su elección (1-4): ", ['1', '2', '3', '4'])

    def run_example(self):
        example_files = [f for f in os.listdir(self.examples_path) if f.endswith(".py") and f != "__init__.py"]
        if not example_files:
            print("No se encontraron ejemplos.")
            return

        print("\n--- Ejemplos Disponibles ---")
        for i, filename in enumerate(example_files):
            print(f"{i + 1}. {filename.replace('.py', '')}")

        try:
            choice = self._get_validated_int_input(f"Seleccione un ejemplo para ejecutar (1-{len(example_files)}): ", 1, len(example_files))
            selected_example = example_files[choice - 1]
            print(f"Ejecutando {selected_example}...")
            
            spec = importlib.util.spec_from_file_location("example_module", os.path.join(self.examples_path, selected_example))
            example_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(example_module)

            self.state.load_results(example_module)
        except Exception as e:
            print(f"Ocurrió un error al ejecutar el ejemplo: {e}")

    def generate_gifs(self):
        if not self.state.structure or self.state.freqs is None or self.state.modes is None:
            print("No hay una estructura cargada o resultados de análisis modal. Por favor, ejecute un ejemplo primero.")
            return

        print("\n--- Generar GIFs ---")
        print("1. Animar Modos de Vibración (GIF)")
        options = ['1', '0']
        if self.state.harmonic_data is not None:
            print("2. Animar Respuesta Armónica (GIF)")
            options.append('2')
        print("0. Volver al Menú Principal")

        choice = self._get_validated_input("Ingrese su elección: ", options)

        if choice == '1':
            self._animate_modes()
        elif choice == '2' and self.state.harmonic_data is not None:
            self._animate_harmonic_response()
        elif choice == '0':
            pass # Volver al menú principal

    def _animate_modes(self):
        while True:
            num_modes_to_plot_str = input(f"Ingrese el número de modos a visualizar (1-{len(self.state.freqs)}) o 't' para todos: ").strip().lower()
            if num_modes_to_plot_str == 't':
                num_modes_to_plot = len(self.state.freqs)
                break
            try:
                num_modes_to_plot = int(num_modes_to_plot_str)
                if 1 <= num_modes_to_plot <= len(self.state.freqs):
                    break
                else:
                    print("Número de modos inválido. Intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número o 't'.")
        
        output_dir = "graficos_resultados/modo_animacion"
        os.makedirs(output_dir, exist_ok=True)
        for i in range(num_modes_to_plot):
            filename = os.path.join(output_dir, f"modo_{i + 1}.gif")
            animate_mode_shape(
                self.state.structure,
                self.state.modes[:, i],
                title=f"Modo {i + 1} - {self.state.freqs[i]:.2f} Hz",
                filename=filename,
            )
        print(f"Se guardaron {num_modes_to_plot} animaciones de los modos en '{output_dir}'.")

    def _animate_harmonic_response(self):
        output_filename = "graficos_resultados/respuesta_armonica_animacion/harmonic_animation.gif"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        animate_harmonic_response(
            structure=self.state.structure,
            displacement_history=self.state.harmonic_data,
            output_filename=output_filename
        )
        print(f"Animación de respuesta armónica guardada en '{output_filename}'.")

    def run(self):
        while True:
            choice = self.display_main_menu()
            if choice == '1':
                self.run_example()
            elif choice == '2':
                if self.state.structure:
                    # Usar multiprocessing para evitar que la GUI bloquee el menú CLI
                    plot_process = multiprocessing.Process(target=plot_in_separate_process, args=(self.state.structure,))
                    plot_process.start()
                    plot_process.join()  # Espera a que la ventana de visualización se cierre
                else:
                    print("No hay una estructura cargada. Por favor, ejecute un ejemplo primero.")
            elif choice == '3':
                self.generate_gifs()
            elif choice == '4':
                print("Saliendo del programa.")
                break
            else:
                # This else block should ideally not be reached due to _get_validated_input
                print("Opción no válida.")


if __name__ == "__main__":
    # Es importante para multiprocessing en algunos sistemas operativos (Windows, macOS)
    multiprocessing.freeze_support()
    app = MainMenu()
    app.run()

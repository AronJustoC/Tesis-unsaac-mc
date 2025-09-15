import sys
import os
import importlib.util
import multiprocessing
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QTextEdit, QLabel, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont

# Importaciones de tu proyecto
from analisis_modal_3d.visualization.structure_plotter import plot_structure_with_info
from analisis_modal_3d.visualization.plotter import animate_mode_shape
# from analisis_modal_3d.visualization.plotterPyVista import animate_harmonic_response # Descomentar si se usa

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
            return True
        else:
            return False

class Worker(QObject):
    """Worker to run long tasks in a separate thread (e.g., example execution)."""
    finished = pyqtSignal(bool, str) # True for success, False for error, and message
    log_message = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._stdout_original = sys.stdout # Almacenar stdout original

    def run(self):
        try:
            sys.stdout = self # Redirigir stdout a esta instancia del Worker
            self.log_message.emit(f"Iniciando tarea: {self.func.__name__}...")
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(True, "Tarea completada.")
        except Exception as e:
            self.finished.emit(False, f"Error en la tarea: {e}")
        finally:
            sys.stdout = self._stdout_original # Restaurar stdout original

    # Métodos write y flush para la redirección de sys.stdout
    def write(self, text):
        self.log_message.emit(text.strip()) # Emitir la señal
    
    def flush(self):
        pass

class StructuralAnalysisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análisis Estructural con PyQt6")
        self.setGeometry(100, 100, 900, 700) # Aumentar tamaño de ventana

        self.state = AppState()
        self.examples_path = "analisis_modal_3d/examples"
        self.example_files = []
        self.selected_example_file = None

        self._create_widgets()
        self._load_example_files()

    def _create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Título de la aplicación
        title_label = QLabel("Herramienta de Análisis Estructural Modal")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Sección de selección de ejemplo
        example_frame = QFrame()
        example_frame.setFrameShape(QFrame.Shape.StyledPanel)
        example_layout = QVBoxLayout(example_frame)
        example_layout.addWidget(QLabel("Seleccionar Ejemplo:"))

        self.example_combobox = QComboBox()
        self.example_combobox.currentIndexChanged.connect(self._on_example_selected)
        example_layout.addWidget(self.example_combobox)

        self.run_example_button = QPushButton("Ejecutar Ejemplo")
        self.run_example_button.clicked.connect(self._run_selected_example)
        example_layout.addWidget(self.run_example_button)
        main_layout.addWidget(example_frame)

        # Sección de acciones
        actions_frame = QFrame()
        actions_frame.setFrameShape(QFrame.Shape.StyledPanel)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.addWidget(QLabel("Acciones:"))

        self.plot_structure_button = QPushButton("Visualizar Estructura")
        self.plot_structure_button.clicked.connect(self._plot_structure)
        actions_layout.addWidget(self.plot_structure_button)

        self.generate_gifs_button = QPushButton("Generar GIFs")
        self.generate_gifs_button.clicked.connect(self._generate_gifs)
        actions_layout.addWidget(self.generate_gifs_button)
        main_layout.addWidget(actions_frame)

        # Sección de salida (log)
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.Shape.StyledPanel)
        log_layout = QVBoxLayout(log_frame)
        log_layout.addWidget(QLabel("Salida:"))

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_frame, 1) # Expandir verticalmente

        # Botón de salir
        exit_button = QPushButton("Salir")
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button)

    def _log_message(self, message):
        self.log_text.append(message)

    def _load_example_files(self):
        self.example_files = [f for f in os.listdir(self.examples_path) if f.endswith(".py") and f != "__init__.py"]
        self.example_files.sort() # Ordenar alfabéticamente
        self.example_combobox.addItems([f.replace('.py', '') for f in self.example_files])
        if self.example_files:
            self.selected_example_file = self.example_files[0]

    def _on_example_selected(self, index):
        selected_name = self.example_combobox.currentText()
        self.selected_example_file = selected_name + ".py"
        self._log_message(f"Ejemplo seleccionado: {selected_name}")

    def _run_selected_example(self):
        if not self.selected_example_file:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un ejemplo primero.")
            return

        self._log_message(f"Ejecutando {self.selected_example_file}...")
        
        # Deshabilitar botones durante la ejecución
        self.run_example_button.setEnabled(False)
        self.plot_structure_button.setEnabled(False)
        self.generate_gifs_button.setEnabled(False)

        # Ejecutar el ejemplo en un hilo separado para no bloquear la GUI
        self.worker_thread = QThread()
        self.worker = Worker(self._execute_example_logic)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_example_finished)
        self.worker.log_message.connect(self._log_message)
        self.worker_thread.start()

    def _execute_example_logic(self):
        # Esta función se ejecuta en el hilo del worker
        try:
            spec = importlib.util.spec_from_file_location("example_module", os.path.join(self.examples_path, self.selected_example_file))
            example_module = importlib.util.module_from_spec(spec)
            # sys.stdout = self # Esta línea se maneja ahora en Worker.run()
            spec.loader.exec_module(example_module)
            # sys.stdout = sys.__stdout__ # Esta línea se maneja ahora en Worker.run()

            if self.state.load_results(example_module):
                self.worker.log_message.emit("Ejemplo ejecutado exitosamente. Resultados cargados.")
            else:
                self.worker.log_message.emit("El ejemplo no produjo los resultados esperados (estructura, frecuencias, modos).")
                raise Exception("Resultados no cargados.")

        except Exception as e:
            self.worker.log_message.emit(f"Ocurrió un error al ejecutar el ejemplo: {e}")
            raise # Re-lanzar para que el worker.finished capture el error

    def _on_example_finished(self, success, message):
        self._log_message(message)
        if not success:
            QMessageBox.critical(self, "Error de Ejecución", message)
        
        # Re-habilitar botones
        self.run_example_button.setEnabled(True)
        self.plot_structure_button.setEnabled(True)
        self.generate_gifs_button.setEnabled(True)
        self.worker_thread.quit()
        self.worker_thread.wait()

    def _plot_structure(self):
        if not self.state.structure:
            QMessageBox.warning(self, "Advertencia", "No hay una estructura cargada. Por favor, ejecute un ejemplo primero.")
            return
        self._log_message("Visualizando estructura...")
        # Ejecutar en un proceso separado para no bloquear la GUI
        p = multiprocessing.Process(target=plot_structure_with_info, args=(self.state.structure,))
        p.start()

    def _generate_gifs(self):
        if not self.state.structure or self.state.freqs is None or self.state.modes is None:
            QMessageBox.warning(self, "Advertencia", "No hay resultados de análisis modal. Por favor, ejecute un ejemplo primero.")
            return
        
        # Aquí se podría añadir una interfaz para pedir el modo y el factor de escala
        # Por simplicidad, generaremos el primer modo con un factor de escala fijo
        self._log_message("Generando GIF del primer modo...")
        try:
            # Asumiendo que queremos el primer modo y un factor de escala de 0.5
            mode_index = 0
            deformation_scale = 0.5
            output_filename = os.path.join("graficos_resultados", "modo_animacion", "gui_mode_1.gif")
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)

            # Ejecutar en un proceso separado para no bloquear la GUI
            p = multiprocessing.Process(target=animate_mode_shape, args=(
                self.state.structure,
                self.state.modes[:, mode_index],
                deformation_scale,
                f"Modo {mode_index + 1} - {self.state.freqs[mode_index]:.2f} Hz",
                output_filename
            ))
            p.start()
            self._log_message(f"GIF generado en: {output_filename}")
        except Exception as e:
            self._log_message(f"Error al generar GIF: {e}")
            QMessageBox.critical(self, "Error GIF", f"Error: {e}")


if __name__ == "__main__":
    multiprocessing.freeze_support() # Necesario para multiprocessing en Windows/macOS
    app = QApplication(sys.argv)
    gui = StructuralAnalysisGUI()
    gui.show()
    sys.exit(app.exec())

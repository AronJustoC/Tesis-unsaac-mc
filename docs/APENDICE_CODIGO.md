# Apéndice: Fragmentos de Código de Implementación

Evalenloveiste apéndice presenta fragmentos de código clave que ilustran la implementación del software de análisis estructural desarrollado para esta tesis. El código está escrito en Python y utiliza librerías como NumPy para los cálculos matriciales.

## 1. Análisis Modal

El análisis modal se realiza para determinar las frecuencias naturales y las formas modales de la estructura, que son propiedades dinámicas intrínsecas.

### 1.1. Ejemplo de Definición de Datos de Entrada

El siguiente código muestra un extracto de la estructura del diccionario de Python utilizado para definir el modelo del puente Bailey. Este enfoque permite una definición de la estructura desacoplada de la lógica de análisis.

```python
# Contenido de: analisis_modal_3d/apps/data/data_bailey_pasadores.py (extracto)

def get_data():
    """Retorna un diccionario con la definición completa del modelo."""
    data = {
        # Definición de Nodos (Coordenadas en metros)
        'nodes': {
            1: {'coords': [0.0, 0.0, 0.0]},
            2: {'coords': [1.524, 0.0, 0.0]},
            # ... (se omiten más de 300 nodos para brevedad)
        },

        # Definición de Elementos (Vigas)
        'elements': {
            1: {'type': 'BEAM', 'nodes': [1, 2],
                'material_id': 1, 'section_id': 1},
            # ... (se omiten más de 500 elementos para brevedad)
        },

        # Definición de Materiales (Acero)
        'materials': {
            1: {'E': 2.1e11, 'G': 8.07e10, 'rho': 7850},
        },

        # Definición de Secciones Transversales
        'sections': {
            1: {'area': 0.004, 'I_y': 1.e-5, 'I_z': 1.e-5, 'J': 2.e-5},
            # ... (se definen múltiples secciones)
        },

        # Definición de Restricciones (Apoyos)
        'constraints': {
            1: {'dof': [0, 1, 2, 3, 4, 5], 'value': 0}, # Apoyo empotrado
            # ... (se definen otros apoyos)
        },

        # Configuración específica del análisis
        'analysis_settings': {
            'modal_analysis': {
                'num_modes': 10
            },
        }
    }
    return data
```

### 1.2. Lógica del Flujo de Trabajo Principal

Este script orquesta el análisis modal, desde la carga de datos hasta la visualización de resultados.

```python
# --- Fragmento para Tesis: Flujo de Trabajo del Análisis Modal ---

# 1. Definir el archivo de datos que describe la estructura
data_file_path = "analisis_modal_3d/apps/data/data_bailey_pasadores.py"

# 2. Cargar los datos y construir el objeto 'Structure'
input_data = load_data_from_file(data_file_path)
structure = build_structure_from_data(input_data)

# 3. Ensamblar las matrices globales de Rigidez (K) y Masa (M)
K, M = assemble_global_matrices(structure)

# 4. Ejecutar el solucionador de análisis modal
#    Resuelve el problema de valores propios: (K - ω²M)φ = 0
num_modes_a_calcular = 10
natural_frequencies, mode_shapes, mass_participation = modal_analysis(
    K, M, structure, num_modes=num_modes_a_calcular
)

# 5. Post-procesamiento de resultados
#    Genera las tablas y las visualizaciones 3D de los modos de vibración.
print_modal_results_table(natural_frequencies, mass_participation)
visualize_interactive_modes(structure, mode_shapes)
```

## 2. Análisis de Respuesta Armónica

Este análisis calcula la respuesta de la estructura en estado estacionario ante una excitación armónica.

### 2.1. Ejemplo de Definición de Datos de Entrada (Adicional)

Para el análisis armónico, se añaden las siguientes configuraciones al diccionario de `analysis_settings` en el archivo de datos.

```python
# ... dentro de 'analysis_settings' en el archivo de datos ...
'damping': {
    'zeta_target': 0.04,      # 4% de amortiguamiento crítico
    'rayleigh_modes': [1, 5]  # Modos para anclar la curva de Rayleigh
},
'frequency_response': {
    'freq_range_hz': [60],   # Frecuencia(s) a analizar
    'unbalanced_force': {
        'mass': 0.1,
        'eccentricity_mm': 50
    }
}
```

### 2.2. Lógica del Flujo de Trabajo Principal

Este script muestra el proceso completo, que incluye el análisis modal como paso previo.

```python
# --- Fragmento para Tesis: Flujo de Trabajo del Análisis de Respuesta Armónica ---

# === PASO PREVIO: ANÁLISIS MODAL ===
# Se ejecutan los pasos 1-4 del flujo de trabajo modal para obtener:
# - Matriz de Rigidez [K]
# - Matriz de Masa [M]
# - Frecuencias naturales (necesarias para el amortiguamiento)

# === INICIO DEL ANÁLISIS ARMÓNICO ===

# 5. Definir y construir la Matriz de Amortiguamiento [C] de Rayleigh
C = calculate_rayleigh_damping(
    M=M,
    K=K,
    modal_frequencies=natural_frequencies,
    zeta_target=0.04,
    modes_to_use=(1, 5)
)

# 6. Definir la Fuerza de Excitación Armónica
force_properties = {'node_id': 163, 'mass': 0.1, 'eccentricity': 0.05}
F_direction_vector = define_rotational_force_vector(structure, force_properties["node_id"])
unbalanced_product = force_properties["mass"] * force_properties["eccentricity"]

# 7. Definir el rango de frecuencias para el barrido del análisis
frequency_range_hz = np.array([60])

# 8. Ejecutar el solucionador de respuesta en frecuencia directa
complex_displacements = direct_frequency_response(
    K, M, C,
    force_vector_amplitude=F_direction_vector,
    frequency_range_hz=frequency_range_hz,
    is_unbalanced_force=True,
    unbalanced_mass_product=unbalanced_product
)

# 9. Post-procesamiento de resultados
print_velocity_results(complex_displacements, frequency_range_hz, nodes_of_interest)
```

### 2.3. Lógica Interna del Solucionador

Los siguientes fragmentos detallan los cálculos clave que ocurren dentro de las funciones de análisis.

#### Cálculo de Coeficientes de Rayleigh

```python
# 1. Definir el amortiguamiento crítico objetivo y los modos a usar
zeta_target = 0.04
omega_i = freqs_rad[0]  # Frecuencia del modo 1
omega_j = freqs_rad[4]  # Frecuencia del modo 5

# 2. Resolver el sistema de ecuaciones para alpha y beta
alpha = 2 * zeta_target * (omega_i * omega_j) / (omega_i + omega_j)
beta = 2 * zeta_target / (omega_i + omega_j)

# 3. Construir la matriz de amortiguamiento C
C = alpha * M + beta * K
```

#### Solución en el Dominio de la Frecuencia

```python
# Bucle que se ejecuta para cada frecuencia 'omega' en el rango de análisis
for omega in frequency_range_rad:

    # 1. Construir la matriz de impedancia dinámica Z(ω)
    Z_omega = K - (omega**2 * M) + (1j * omega * C)

    # 2. Calcular la magnitud de la fuerza para esta frecuencia: F(ω) = (m*e*ω²) * F_direction
    F_omega = (unbalanced_mass_product * omega**2) * F_direction

    # 3. Resolver el sistema Z*U = F para obtener los desplazamientos complejos
    U_complex = np.linalg.solve(Z_omega, F_omega)

    # 4. Calcular las velocidades: V = jωU
    V_complex = (1j * omega) * U_complex
```

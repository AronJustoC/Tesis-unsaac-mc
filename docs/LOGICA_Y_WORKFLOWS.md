# Resumen de Lógica y Workflows del Proyecto de Análisis Estructural 3D

Este documento proporciona un resumen completo de la lógica, la estructura y los flujos de trabajo principales del proyecto de análisis estructural 3D.

## 1. Descripción General del Proyecto

El proyecto es una herramienta basada en Python para realizar análisis estructurales de elementos tipo viga en 3D. Permite determinar el comportamiento de estructuras bajo cargas estáticas, así como sus características dinámicas intrínsecas (frecuencias y modos de vibración) y su respuesta a excitaciones armónicas. El proyecto está diseñado con una clara separación de responsabilidades entre la definición de la estructura, el análisis y la visualización.

## 2. Estructura de Directorios Clave

-   **`src/analisis_modal_3d/structures/`**: Define los componentes básicos de una estructura:
    -   `node.py`: Representa un nodo con sus coordenadas y grados de libertad.
    -   `element.py`: Define un elemento estructural (viga) con sus propiedades de material y sección.
    -   `structure.py`: Agrupa nodos y elementos para formar la estructura completa.
-   **`src/analisis_modal_3d/analysis/`**: Contiene los módulos para realizar los diferentes tipos de análisis:
    -   `assembler.py`: Ensambla las matrices globales de rigidez (K) y masa (M) a partir de los elementos.
    -   `static.py`: Resuelve el problema de análisis estático.
    -   `modal.py`: Realiza el análisis modal (cálculo de frecuencias y modos de vibración).
    -   `damping.py`: Implementa la creación de la matriz de amortiguamiento (ej. amortiguamiento de Rayleigh).
    -   `frequency_response.py`: Calcula la respuesta de la estructura a excitaciones armónicas.
-   **`src/analisis_modal_3d/visualization/`**: Módulos para graficar y visualizar los resultados:
    -   `static_plotter.py`: Visualiza estructuras deformadas estáticamente.
    -   `mode_plotter.py`: Grafica los modos de vibración.
    -   `time_response_plotter.py`: (Sugerido en `GEMINI.md`) Para visualizar respuestas en el tiempo.
    -   `results_processor.py`: Procesa y presenta resultados numéricos (ej. tablas de velocidades).
-   **`src/analisis_modal_3d/data/`**: Contiene scripts Python que definen los datos de entrada para diferentes ejemplos de estructuras (geometría, materiales, secciones, cargas, restricciones).
-   **`examples/analysis_workflows/`**: Scripts de alto nivel que orquestan los diferentes tipos de análisis, mostrando cómo usar las librerías del proyecto.
-   **`app/trame_app.py`**: Contiene la implementación de una interfaz gráfica de usuario (GUI) utilizando el framework Trame, permitiendo la interacción visual con los análisis.
-   **`docs/`**: Documentación detallada sobre los fundamentos teóricos y la implementación de cada tipo de análisis.

## 3. Conceptos Fundamentales

El proyecto se basa en el Método de Elementos Finitos (MEF) para el análisis de estructuras. Los conceptos clave incluyen:

-   **Nodos y Grados de Libertad (GDL)**: Cada nodo tiene 6 GDL (3 traslaciones y 3 rotaciones).
-   **Elementos Tipo Viga 3D**: Modelados con 12 GDL (6 por nodo).
-   **Matrices de Rigidez Local y Global (K)**: Representan la resistencia de la estructura a la deformación.
-   **Matrices de Masa Local y Global (M)**: Representan la inercia de la estructura.
-   **Matrices de Amortiguamiento (C)**: Representan la disipación de energía (ej. amortiguamiento de Rayleigh).
-   **Vector de Fuerzas (F)**: Cargas externas aplicadas a la estructura.
-   **Vector de Desplazamientos (u)**: Deformaciones de la estructura.

## 4. Lógica Principal y Flujos de Trabajo de Análisis

La lógica general para cualquier análisis sigue un patrón común:

1.  **Definición del Modelo**: Cargar datos de la estructura (nodos, elementos, propiedades, restricciones, cargas) desde un archivo de datos y construir un objeto `Structure`.
2.  **Ensamblaje de Matrices**: Ensamblar las matrices globales de rigidez (K) y masa (M) de la estructura, aplicando las condiciones de contorno (restricciones).
3.  **Ejecución del Análisis**: Resolver el sistema de ecuaciones correspondiente al tipo de análisis.
4.  **Post-procesamiento y Visualización**: Interpretar los resultados numéricos y visualizarlos gráficamente.

A continuación, se detallan los flujos de trabajo para cada tipo de análisis implementado:

### 4.1. Análisis Estático

-   **Propósito**: Determinar desplazamientos, fuerzas internas y tensiones bajo cargas que no varían con el tiempo.
-   **Ecuación Fundamental**: $\mathbf{K} \mathbf{u} = \mathbf{F}$
-   **Flujo de Trabajo (`examples/analysis_workflows/static_analysis.py`)**:
    1.  Cargar datos de la estructura y construir el objeto `Structure`.
    2.  Ensamblar la matriz de rigidez global `K`.
    3.  Definir el vector de fuerzas `F` a partir de los datos de entrada.
    4.  Resolver el sistema lineal $\mathbf{K} \mathbf{u} = \mathbf{F}$ para obtener los desplazamientos `u`.
    5.  Calcular fuerzas axiales en los elementos.
    6.  Visualizar la estructura deformada utilizando `static_plotter.py`.
-   **Archivos Clave**: `analysis/static.py`, `analysis/assembler.py`, `visualization/static_plotter.py`.

### 4.2. Análisis Modal

-   **Propósito**: Determinar las frecuencias naturales y los modos de vibración intrínsecos de la estructura. Es un análisis de vibración libre y no amortiguada.
-   **Ecuación Fundamental**: $(\mathbf{K} - \omega^2 \mathbf{M}) \mathbf{\phi} = \mathbf{0}$ (problema de autovalores).
-   **Flujo de Trabajo (`examples/analysis_workflows/modal_analysis.py`)**:
    1.  Cargar datos de la estructura y construir el objeto `Structure`.
    2.  Ensamblar las matrices globales de rigidez `K` y masa `M`.
    3.  Resolver el problema de autovalores para obtener las frecuencias naturales (`freqs`) y los modos de vibración (`modes`).
    4.  Calcular la participación de masa modal.
    5.  Visualizar los modos de vibración utilizando `mode_plotter.py`.
-   **Archivos Clave**: `analysis/modal.py`, `analysis/assembler.py`, `visualization/mode_plotter.py`, `visualization/results_processor.py`.

### 4.3. Análisis de Respuesta Armónica (Vibración Forzada)

-   **Propósito**: Calcular la respuesta (desplazamientos, velocidades) de la estructura cuando es sometida a una excitación armónica (ej. un motor desbalanceado). Considera el amortiguamiento.
-   **Ecuación Fundamental**: $(\mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C}) \mathbf{U} = \mathbf{F}_0$ (solución directa en el dominio de la frecuencia).
-   **Flujo de Trabajo (`examples/analysis_workflows/harmonic_analysis.py`)**:
    1.  Cargar datos de la estructura y construir el objeto `Structure`.
    2.  Ensamblar las matrices globales de rigidez `K` y masa `M`.
    3.  Realizar un análisis modal preliminar para obtener las frecuencias necesarias para el cálculo del amortiguamiento de Rayleigh.
    4.  Calcular la matriz de amortiguamiento `C` (usando coeficientes de Rayleigh `alpha` y `beta`).
    5.  Definir la fuerza de excitación armónica (ej. fuerza desbalanceada de un motor) y el rango de frecuencias a analizar.
    6.  Para cada frecuencia en el rango, resolver el sistema de ecuaciones complejas para obtener los desplazamientos complejos `U`.
    7.  Calcular las amplitudes de velocidad a partir de los desplazamientos complejos.
    8.  Imprimir tablas de velocidades y visualizar la deformación de la estructura para cada frecuencia utilizando `static_plotter.py` (adaptado para mostrar la parte real de la deformación compleja).
-   **Archivos Clave**: `analysis/frequency_response.py`, `analysis/damping.py`, `analysis/assembler.py`, `visualization/results_processor.py`, `visualization/static_plotter.py`.

## 5. Interfaz Gráfica de Usuario (GUI)

El proyecto incluye una interfaz gráfica de usuario (`app/trame_app.py`) construida con el framework Trame. Esta GUI permite a los usuarios interactuar visualmente con el modelo, definir parámetros de análisis y visualizar los resultados de una manera más intuitiva, extendiendo la funcionalidad de los scripts de línea de comandos.

## 6. Instalación y Uso Básico (desde `README.md`)

### Requisitos

-   Python >= 3.8
-   numpy >= 1.21.0
-   scipy >= 1.7.0
-   matplotlib >= 3.4.0

### Instalación

1.  Clonar el repositorio:
    ```bash
    git clone https://github.com/usuario/analisis-modal-3d.git
    cd analisis-modal-3d
    ```
2.  Crear y activar entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

### Uso de los Workflows de Ejemplo

Para ejecutar un análisis, se utilizan los scripts en `examples/analysis_workflows/` junto con un archivo de datos de la carpeta `src/analisis_modal_3d/data/`.

Ejemplo de análisis modal:
```bash
python examples/analysis_workflows/modal_analysis.py src/analisis_modal_3d/data/simple_beam_data.py
```

Ejemplo de análisis estático:
```bash
python examples/analysis_workflows/static_analysis.py src/analisis_modal_3d/data/bailey_bridge_data.py
```

Ejemplo de análisis armónico:
```bash
python examples/analysis_workflows/harmonic_analysis.py src/analisis_modal_3d/data/frequency_sweep_example_data.py
```

## 7. Conclusión

Este proyecto proporciona una herramienta robusta para el análisis estructural 3D, cubriendo análisis estáticos, modales y de vibración forzada. Su diseño modular facilita la extensión y el mantenimiento, mientras que la integración de una GUI mejora la experiencia del usuario.

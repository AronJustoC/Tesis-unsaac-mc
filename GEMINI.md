# Espacio de Trabajo de Gemini `GEMINI.md`

Este documento proporciona una descripción general de la estructura y la
lógica del proyecto para guiar a Gemini en las tareas de desarrollo.

## Descripción General del Proyecto

Este proyecto parece ser una herramienta basada en Python para realizar
análisis modales de estructuras 3D. La lógica principal de la aplicación se
encuentra en el directorio `02_analisis_modal_3d/src`. El proyecto también
incluye un directorio para la documentación.

## Estructura de Directorios

```
/
├── 01_Docs/
│   ├── fabricacion.md
│   └── TESIS_Rev.1.docx
├── 02_analisis_modal_3d/
│   ├── README.md
│   └── src/
│       ├── analysis/
│       │   ├── assembler.py
│       │   └── modal.py
│       ├── examples/
│       │   ├── bailey.py
│       │   ├── baileyEscalado.py
│       │   ├── no_simple_beam.py
│       │   ├── one_secction_bailey.py
│       │   └── simple_beam.py
│       ├── structures/
│       │   ├── element.py
│       │   ├── node.py
│       │   └── structure.py
│       └── visualization/
│           ├── mode_plotter.py
│           ├── plotter.py
│           └── structure_plotter.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Descripción de Directorios

- **`01_Docs/`**: Contiene la documentación del proyecto, incluyendo
  `fabricacion.md` y un documento de tesis.
- **`02_analisis_modal_3d/`**: El núcleo del proyecto, que contiene la
  herramienta de análisis modal.
  - **`src/`**: El código fuente de Python para la herramienta de análisis.
    - **`analysis/`**: Módulos para realizar el análisis estructural.
      - `assembler.py`: Ensambla las matrices globales de rigidez y
        masa.
      - `modal.py`: Realiza el análisis modal (calcula los valores y
        vectores propios).
    - **`examples/`**: Scripts de ejemplo que demuestran cómo usar la
      herramienta.
    - **`structures/`**: Módulos para definir los componentes de una
      estructura.
      - `node.py`: Define un nodo en la estructura.
      - `element.py`: Define un elemento estructural (p. ej., una
        viga).
      - `structure.py`: Define la estructura general compuesta por
        nodos y elementos.
    - **`visualization/`**: Módulos para graficar y visualizar los
      resultados.
      - `structure_plotter.py`: Grafica la estructura.
      - `mode_plotter.py`: Grafica los modos de vibración.
- **`venv/`**: Entorno virtual de Python.
- **`.gitignore`**: Especifica los archivos y directorios que Git debe
  ignorar.
- **`README.md`**: El archivo README principal del proyecto.
- **`requirements.txt`**: Enumera las dependencias de Python para el
  proyecto.

## Lógica Principal

La lógica principal de la aplicación en `02_analisis_modal_3d` es la
siguiente:

1. **Definir una Estructura**: El usuario define una estructura utilizando
   las clases del directorio `structures`. Esto implica la creación de
   objetos `Node` y `Element` y su combinación en un objeto `Structure`.
   Los ejemplos del directorio `examples` muestran cómo se hace.
2. **Ensamblar Matrices**: El módulo `assembler.py` toma el objeto
   `Structure` y ensambla las matrices globales de rigidez y masa.
3. **Realizar Análisis Modal**: El módulo `modal.py` utiliza las matrices
   ensambladas para resolver el problema de valores propios, obteniendo las
   frecuencias naturales y los modos de vibración de la estructura.
4. **Visualizar Resultados**: Los módulos de `visualization` se utilizan para
   graficar la estructura original y sus modos de vibración.

Al trabajar en este proyecto, preste atención a la separación de
responsabilidades entre los paquetes `structures`, `analysis` y
`visualization`.

## Análisis de Vibración Forzada (Masa Desbalanceada)

Para simular el comportamiento de la estructura ante un motor con masa
desbalanceada, se requiere implementar un análisis de vibración forzada.
Dado que el análisis modal ya está implementado, el método más eficiente
es la **Superposición Modal**.

### Características y Módulos Necesarios

1. **Definición de la Fuerza de Excitación:**

    - Modelar la fuerza generada por la masa desbalanceada como una función
      del tiempo (amplitud, frecuencia, punto de aplicación, dirección).
    - Posiblemente una nueva clase o función en `analysis/`.

2. **Matriz de Amortiguamiento (`C`):**

    - Implementar la creación de la matriz de amortiguamiento global.
    - Se puede considerar el amortiguamiento de Rayleigh (`C = αM + βK`)
      o un amortiguamiento modal.
    - Ubicación sugerida: `analysis/damping.py` o extensión de `assembler.py`.

3. **Solución Dinámica (Superposición Modal):**

    - Un nuevo módulo que tome como entrada las matrices `M`, `K`, `C`,
      las frecuencias y formas modales (del análisis modal), y la fuerza
      de excitación `F(t)`.
    - Resolver las ecuaciones de movimiento desacopladas para obtener la
      respuesta de la estructura en el dominio del tiempo (`u(t)`).
    - Ubicación sugerida: `analysis/forced_vibration.py`.

4. **Visualización de la Respuesta en el Tiempo:**

    - Funciones para graficar los desplazamientos, velocidades o
      aceleraciones de nodos específicos en función del tiempo.
    - Ubicación sugerida: `visualization/time_response_plotter.py` o extensión de `plotter.py`.

5. **Animación de la Vibración Forzada:**
    - Capacidad para animar la deformación de la estructura a lo largo del
      tiempo bajo la acción de la fuerza forzada.
    - Ubicación sugerida: Extensión de `mode_plotter.py` o `plotter.py`
      para incluir animación temporal.

Estos pasos permitirán extender la funcionalidad del programa para realizar
análisis dinámicos más complejos y relevantes para aplicaciones de ingeniería.

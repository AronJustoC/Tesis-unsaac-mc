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

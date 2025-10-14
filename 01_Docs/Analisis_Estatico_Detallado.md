# Análisis Estático: Guía Detallada

Este documento explica en detalle el análisis estático, su propósito y cómo se implementa en este proyecto.

## 1. ¿Qué es el Análisis Estático?

El análisis estático es una rama de la mecánica estructural que se ocupa del comportamiento de las estructuras bajo cargas que no varían con el tiempo (cargas estáticas). En este tipo de análisis, se asume que las aceleraciones y velocidades de la estructura son despreciables, lo que simplifica la ecuación fundamental del movimiento.

El objetivo principal del análisis estático es determinar los desplazamientos, las fuerzas internas (axiales, cortantes, momentos) y las tensiones en los elementos de una estructura cuando está en equilibrio bajo la acción de cargas aplicadas.

## 2. Propósito del Análisis Estático

El análisis estático es fundamental en el diseño y la evaluación de estructuras por varias razones:

*   **Dimensionamiento de Elementos:** Permite calcular las fuerzas y momentos que actúan sobre los diferentes componentes estructurales, lo que es esencial para seleccionar las dimensiones y materiales adecuados para que la estructura soporte las cargas sin fallar.
*   **Verificación de la Resistencia y Estabilidad:** Ayuda a asegurar que la estructura sea lo suficientemente resistente para soportar las cargas aplicadas y que sea estable (no colapse ni se deforme excesivamente).
*   **Cálculo de Desplazamientos:** Determina cuánto se deforma la estructura bajo carga, lo cual es importante para cumplir con los límites de servicio (por ejemplo, que un piso no se flexione demasiado).
*   **Base para Análisis Posteriores:** Los resultados del análisis estático (como las fuerzas internas) a menudo se utilizan como punto de partida para análisis más complejos, como el diseño de conexiones o el análisis de fatiga.

## 3. Ecuación Fundamental del Equilibrio Estático

La ecuación fundamental del movimiento para un sistema estructural es:

$$
\mathbf{M} \ddot{\mathbf{u}}(t) + \mathbf{C} \dot{\mathbf{u}}(t) + \mathbf{K} \mathbf{u}(t) = \mathbf{F}(t)
$$

En el análisis estático, se asume que las aceleraciones ($\ddot{\mathbf{u}}(t)$) y las velocidades ($\dot{\mathbf{u}}(t)$) son cero, y que las cargas ($\mathbf{F}(t)$) son constantes en el tiempo ($\mathbf{F}$). Esto simplifica la ecuación a:

$$
\mathbf{K} \mathbf{u} = \mathbf{F}
$$

Donde:
*   $\mathbf{K}$: Matriz de Rigidez global de la estructura.
*   $\mathbf{u}$: Vector de desplazamientos nodales (incógnitas).
*   $\mathbf{F}$: Vector de fuerzas nodales externas aplicadas.

Este es un sistema de ecuaciones lineales que se resuelve para encontrar los desplazamientos nodales $\mathbf{u}$. Una vez que se conocen los desplazamientos, se pueden calcular las fuerzas internas y las tensiones en cada elemento.

## 4. Implementación en el Código

El análisis estático en este proyecto se implementa principalmente en los siguientes archivos:

*   **`analisis_modal_3d/apps/analysis_workflows/static_analysis.py`**: Orquesta el flujo de trabajo del análisis estático.
*   **`analisis_modal_3d/analysis/assembler.py`**: Ensambla la matriz de rigidez global ($\mathbf{K}$) de la estructura. Es crucial que las restricciones (condiciones de contorno) se apliquen correctamente en esta etapa para obtener un sistema soluble y físicamente significativo. En este proyecto, se utiliza el método de penalización para aplicar las restricciones.
*   **`analisis_modal_3d/analysis/static.py`**: Contiene la lógica principal para resolver el sistema de ecuaciones lineales $\mathbf{K} \mathbf{u} = \mathbf{F}$. Utiliza funciones de librerías numéricas (como `numpy.linalg.solve` en Python).

### Flujo de Trabajo Típico:

1.  **Definición de la Estructura:** Se define la geometría (nodos y elementos), propiedades de materiales y secciones, las condiciones de contorno (restricciones) y las cargas aplicadas. Esto se carga desde un archivo de datos (ej., `bailey_bridge_data.py`) y se construye el objeto `Structure` (`analisis_modal_3d/apps/model_builder.py`).
2.  **Ensamblaje de la Matriz de Rigidez:** La matriz global $\mathbf{K}$ se ensambla a partir de los elementos individuales. Durante este proceso, se aplican las restricciones para eliminar los grados de libertad restringidos o para hacerlos muy rígidos (`analisis_modal_3d/analysis/assembler.py`).
3.  **Definición del Vector de Fuerzas:** Se construye el vector $\mathbf{F}$ que contiene todas las cargas externas aplicadas en los grados de libertad correspondientes de los nodos.
4.  **Resolución del Sistema:** Se resuelve el sistema de ecuaciones lineales $\mathbf{K} \mathbf{u} = \mathbf{F}$ para obtener los desplazamientos nodales $\mathbf{u}$.
5.  **Post-procesamiento y Visualización:** Los desplazamientos obtenidos se utilizan para calcular las fuerzas internas (como las fuerzas axiales en los elementos) y para visualizar la estructura deformada. Esto se realiza utilizando módulos de visualización como `analisis_modal_3d/visualization/static_plotter.py`.

Este análisis es la base para comprender cómo una estructura reacciona a cargas permanentes o de larga duración, siendo esencial para su diseño seguro y eficiente.
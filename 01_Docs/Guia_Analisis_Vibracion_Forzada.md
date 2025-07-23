# Guía para Análisis de Vibración Forzada con Carga Armónica

Este documento describe el propósito y el método para implementar un análisis
de vibración forzada en el proyecto, para simular el efecto de un motor
con desbalance en una estructura.

## ¿Para qué sirve un Análisis de Vibración Forzada?

Agregar un motor desbalanceado permite simular y analizar cómo se
comportará la estructura bajo la influencia de una carga dinámica.
Los objetivos principales son:

1. **Análisis de Respuesta en Frecuencia:** Permite analizar cómo vibra la
   estructura a diferentes velocidades (frecuencias) de operación del motor.
   El resultado es un gráfico de "Amplitud vs. Frecuencia" que muestra la
   sensibilidad de la estructura a diferentes excitaciones.

2. **Identificación de Resonancia:** Es el objetivo más crítico. Si la
   frecuencia de operación del motor se acerca a una de las frecuencias
   naturales de la estructura, las vibraciones pueden amplificarse
   masivamente, llevando a una posible falla. Este análisis permite
   predecir y evitar estas condiciones de operación peligrosas.

3. **Determinar Amplitudes y Esfuerzos:** Permite calcular los
   desplazamientos, velocidades, aceleraciones y esfuerzos resultantes en
   la estructura cuando opera a una velocidad de motor constante.

## ¿Cómo Implementarlo en el Proyecto?

El proyecto actual está configurado para un **análisis modal**, que resuelve
la ecuación de movimiento no amortiguado y sin fuerzas externas:

`M*x'' + K*x = 0`

Para un **análisis de vibración forzada**, debemos resolver la ecuación
completa del movimiento:

`M*x'' + C*x' + K*x = F(t)`

Donde:

- `C`: Es la matriz de **amortiguamiento**. Es fundamental para obtener
  resultados realistas, ya que limita la amplitud de la vibración en
  resonancia.
- `F(t)`: Es el **vector de fuerza** dependiente del tiempo, que representa
  la excitación externa (p. ej., la fuerza generada por el motor).

### Plan de Implementación Sugerido

1. **Crear un Nuevo Módulo de Análisis:**

   - Para mantener la separación de responsabilidades, crea un nuevo archivo
     en `02_analisis_modal_3d/src/analysis/`, por ejemplo,
     `harmonic_analysis.py`.

2. **Definir la Fuerza del Motor `F(t)`:**

   - Un motor con masa desbalanceada `m` a una excentricidad `e` girando a
     una frecuencia `Ω` (rad/s) produce una fuerza senoidal con una
     amplitud `F₀ = m * e * Ω²`.
   - El vector `F(t)` contendrá esta fuerza en los grados de libertad
     correspondientes al nodo donde se aplica el motor.

3. **Implementar el Amortiguamiento (Matriz `C`):**

   - Un método común es el **amortiguamiento de Rayleigh**, que define `C` como
     una combinación lineal de las matrices de masa `M` y rigidez `K`:
     `C = α*M + β*K`.
   - Los coeficientes `α` y `β` se calculan a partir de los ratios de
     amortiguamiento deseados en dos frecuencias específicas.

4. **Implementar el Solucionador de Respuesta en Frecuencia:**

   - Dentro de `harmonic_analysis.py`, crea una función que resuelva la
     ecuación de movimiento para un rango de frecuencias de excitación `Ω`.
   - Usando el **método de respuesta en frecuencia**, la ecuación se
     transforma en un sistema de ecuaciones algebraicas para cada `Ω`:
     `(-Ω²*M + i*Ω*C + K) * X(Ω) = F₀`.
   - El proceso para cada frecuencia es:
     a. Construir la matriz dinámica `D(Ω) = (-Ω²*M + i*Ω*C + K)`.
     b. Definir el vector de amplitud de fuerza `F₀`.
     c. Resolver `D(Ω) * X(Ω) = F₀` para obtener la respuesta compleja `X(Ω)`.

5. **Actualizar la Visualización:**

   - Crear nuevas funciones de ploteo (p. ej., en
     `visualization/response_plotter.py`) para graficar la amplitud de la
     respuesta de un nodo vs. la frecuencia de excitación `Ω`.

6. **Crear un Nuevo Ejemplo:**
   - Añadir un script en `examples/` (p. ej., `beam_with_motor.py`) que
     demuestre el flujo de trabajo completo.


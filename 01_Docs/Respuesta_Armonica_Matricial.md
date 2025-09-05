# Guía de Implementación: Análisis de Respuesta Armónica Forzada

Este documento describe el procedimiento paso a paso para calcular la respuesta en estado estacionario de una estructura sometida a una excitación armónica, como la producida por una masa rotativa desbalanceada. El método descrito es la **Solución Directa en el Dominio de la Frecuencia**.

## Ecuación Fundamental del Movimiento

La ecuación que gobierna la dinámica de un sistema estructural es:

$$
\mathbf{M} \ddot{\mathbf{u}}(t) + \mathbf{C} \dot{\mathbf{u}}(t) + \mathbf{K} \mathbf{u}(t) = \mathbf{F}(t)
$$

Donde:
- $\mathbf{M}$: Matriz de Masa global.
- $\mathbf{K}$: Matriz de Rigidez global.
- $\mathbf{C}$: Matriz de Amortiguamiento global.
- $\mathbf{F}(t)$: Vector de fuerzas externas dependientes del tiempo.
- $\mathbf{u}(t)$: Vector de desplazamientos nodales.

---


## Paso 1: Obtener las Matrices de Rigidez (K) y Masa (M)

Estas matrices se asumen ya ensambladas a partir del análisis estático y modal previo. Son la base para el análisis dinámico.

---

## Paso 2: Generación de la Matriz de Amortiguamiento (C)

El amortiguamiento en una estructura real es complejo de modelar. Un método práctico y ampliamente utilizado es el **Amortiguamiento de Rayleigh**. Este método asume que la matriz de amortiguamiento es una combinación lineal de las matrices de masa y rigidez:

$$ 
\mathbf{C} = \alpha \mathbf{M} + \beta \mathbf{K} 
$$ 

Donde $\alpha$ y $\beta$ son constantes que se determinan a partir del comportamiento de amortiguamiento deseado en dos frecuencias específicas.

### ¿Cómo calcular $\alpha$ y $\beta$?

1.  **Selecciona dos frecuencias**: Generalmente se eligen dos frecuencias naturales ($\omega_i$ y $\omega_j$) obtenidas del análisis modal. Por ejemplo, la primera y la tercera frecuencia natural.

2.  **Asigna relaciones de amortiguamiento ($\zeta$)**: Para cada frecuencia seleccionada, se asigna una relación de amortiguamiento modal. Por ejemplo, $\zeta_i = 0.02$ (2% de amortiguamiento) y $\zeta_j = 0.02$ (2%).

3.  **Resuelve el sistema de ecuaciones**: La relación entre $\zeta_r$, $\alpha$ y $\beta$ para una frecuencia natural $\omega_r$ es:

    $$ 
    2 \zeta_r \omega_r = \alpha + \beta \omega_r^2 
    $$ 

    Planteando esto para nuestras dos frecuencias seleccionadas ($\omega_i, \omega_j$), obtenemos un sistema de 2x2:

    $$ 
    \begin{bmatrix} 1 & \omega_i^2 \\ 1 & \omega_j^2 \end{bmatrix} 
    \begin{Bmatrix} \alpha \\ \beta \end{Bmatrix}
    = 
    \begin{Bmatrix} 2 \zeta_i \omega_i \\ 2 \zeta_j \omega_j \end{Bmatrix}
    $$ 

4.  **Despeja $\alpha$ y $\beta$**: Resolviendo el sistema anterior (analítica o numéricamente), se obtienen los coeficientes para construir la matriz $\mathbf{C}$.

---

## Paso 3: Definición del Vector de Fuerza por Desbalance Rotativo

Un motor con una masa desbalanceada $m_e$ girando a una velocidad angular $\omega$ con una excentricidad (distancia del centro de giro a la masa) $e$, produce una fuerza centrífuga de magnitud constante:

$$ F_{mag} = m_e e \omega^2 $$

Esta fuerza gira con el motor. Sus componentes en coordenadas cartesianas son:

$$ F_x(t) = F_{mag} \cos(\omega t) 
\\ F_y(t) = F_{mag} \sin(\omega t) 
$$

Para el análisis en el dominio de la frecuencia, representamos la fuerza usando notación compleja: $\mathbf{F}(t) = \mathbf{F}_0 e^{i\omega t}$. El vector de amplitudes complejas $\mathbf{F}_0$ es un vector columna donde la mayoría de sus elementos son cero.

### Aplicación en la mitad de la estructura:

Supongamos que el motor se ubica en el **nodo `k`**, que está a la mitad de la viga.
- El grado de libertad (GDL) para el desplazamiento en X de ese nodo es `dof_x`.
- El GDL para el desplazamiento en Y es `dof_y`.

El vector $\mathbf{F}_0$ se construye de la siguiente manera:
- La componente `dof_x` del vector $\mathbf{F}_0$ será $m_e e \omega^2$.
- La componente `dof_y` del vector $\mathbf{F}_0$ será $m_e e \omega^2 e^{i\pi/2} = i \cdot (m_e e \omega^2)$. Esto representa la fuerza en Y desfasada 90 grados.
- Todos los demás elementos de $\mathbf{F}_0$ son cero.

**Nota importante**: Para un análisis de barrido en frecuencia, el término $\omega^2$ en la magnitud de la fuerza hace que la amplitud de la excitación varíe con la frecuencia de análisis.

---

## Paso 4: Cálculo de la Respuesta Armónica (Solución Directa)

Asumimos que la respuesta del sistema también será armónica y con la misma frecuencia de la excitación: $\mathbf{u}(t) = \mathbf{U} e^{i\omega t}$. Al sustituir esta solución en la ecuación de movimiento, obtenemos una ecuación algebraica:

$$ 
\left( \mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C} \right) \mathbf{U} = \mathbf{F}_0 
$$ 

Definimos la **Matriz de Rigidez Dinámica** (o Matriz de Impedancia) como:

$$ 
\mathbf{Z}(\omega) = \mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C} 
$$ 

El problema se reduce a resolver el siguiente sistema de ecuaciones lineales complejas para cada frecuencia de excitación $\omega$ de interés:

$$ 
\mathbf{Z}(\omega) \mathbf{U} = \mathbf{F}_0 
$$ 

La solución $\mathbf{U}$ es un vector de **amplitudes de desplazamiento complejas**.

### Interpretación de la solución compleja U:

Para cada GDL `j`:
- La **amplitud del desplazamiento** es el módulo del número complejo: $A_j = |\mathbf{U}_j|$.
- La **fase del desplazamiento** (respecto a la fuerza) es el argumento del número complejo: $\phi_j = \arg(\mathbf{U}_j)$.

El desplazamiento físico en el tiempo es: $u_j(t) = A_j \cos(\omega t + \phi_j)$.

---

## Resumen del Proceso (Guía para el Código)

1.  **Inicialización**:
    - Tener las matrices $\mathbf{M}$ y $\mathbf{K}$ ya construidas.
    - Definir los parámetros del desbalance: $m_e$ y $e$.
    - Definir los parámetros de amortiguamiento: seleccionar dos pares $(\omega_i, \zeta_i)$ y $(\omega_j, \zeta_j)$.

2.  **Cálculo de Amortiguamiento**:
    - Calcular los coeficientes $\alpha$ y $\beta$ de Rayleigh.
    - Construir la matriz de amortiguamiento: $\mathbf{C} = \alpha \mathbf{M} + \beta \mathbf{K}$.

3.  **Barrido en Frecuencia**:
    - Definir un rango de frecuencias de excitación para analizar (ej: `np.linspace(0, 100, 500)`).
    - Crear un arreglo para almacenar los resultados (ej: amplitudes de un nodo de interés).

4.  **Bucle de Solución**:
    - Para cada frecuencia $\omega$ en el rango:
        a. **Construir el vector de fuerza $\mathbf{F}_0$**:
           - Calcular la magnitud $F_{mag} = m_e e \omega^2$.
           - Crear el vector $\mathbf{F}_0$ y asignar las componentes complejas en los GDL correspondientes al nodo de aplicación.
        b. **Construir la matriz de rigidez dinámica $\mathbf{Z}(\omega)$**:
           - $\mathbf{Z}(\omega) = \mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C}$.
        c. **Resolver el sistema lineal**:
           - $\mathbf{U} = \text{np.linalg.solve}(\mathbf{Z}(\omega), \mathbf{F}_0)$.
        d. **Almacenar resultados**:
           - Extraer la amplitud del desplazamiento en el GDL de interés (ej: `np.abs(U[dof_interes])`) y guardarla.

5.  **Visualización**:
    - Graficar las amplitudes almacenadas en función del rango de frecuencias $\omega$. El gráfico resultante es la **Función de Respuesta en Frecuencia (FRF)**, que mostrará los picos de resonancia.
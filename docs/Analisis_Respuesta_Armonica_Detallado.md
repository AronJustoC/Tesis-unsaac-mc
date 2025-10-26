# Teoría de la Respuesta a la Excitación Armónica

Este documento detalla la teoría fundamental para calcular la respuesta de una estructura sometida a una excitación armónica, con un enfoque en la obtención de las amplitudes de desplazamiento y velocidad.

## 1. Sistema de 1 Grado de Libertad (SDOF)

El sistema más simple para entender el fenómeno es el de un único grado de libertad, compuesto por una masa, un resorte y un amortiguador.

### Ecuación del Movimiento

El comportamiento del sistema se describe por la siguiente ecuación diferencial:

$$
m \ddot{x}(t) + c \dot{x}(t) + k x(t) = F(t)
$$

Donde:

- `m`: Masa
- `c`: Coeficiente de amortiguamiento
- `k`: Rigidez
- `x(t)`: Desplazamiento en función del tiempo `t`
- `\dot{x}(t)`: Velocidad
- `\ddot{x}(t)`: Aceleración
- `F(t)`: Fuerza de excitación externa

### Excitación y Respuesta Armónica

Cuando la fuerza es armónica, tiene la forma `F(t) = F_0 \cos(\omega t)`. La solución de estado estacionario (la que permanece después de que la parte transitoria se disipa) también es armónica, con la misma frecuencia `\omega` pero con un desfase `\phi`:

$$
 x_p(t) = X \cos(\omega t - \phi)
$$

#### Amplitud del Desplazamiento (X)

La amplitud del desplazamiento `X` se calcula con la fórmula:

$$
 X = \frac{F_0}{\sqrt{(k - m\omega^2)^2 + (c\omega)^2}}
$$

El ángulo de fase `\phi` se calcula como:

$$
 \phi = \arctan\](\frac{c\omega}{k - m\omega^2})
$$

#### Amplitud de la Velocidad (V)

La velocidad es la primera derivada del desplazamiento. Derivando la respuesta estacionaria `x_p(t)`:

$$
 v(t) = \dot{x}_p(t) = \frac{d}{dt} [X \cos(\omega t - \phi)] = -X\omega \sin(\omega t - \phi)
$$

La amplitud de la velocidad `V` es el valor máximo de `v(t)`, que ocurre cuando el seno es `\pm 1`:

$$
 V = X \omega
$$

Sustituyendo la expresión para `X`, obtenemos la fórmula directa para la amplitud de la velocidad:

$$
 V = \frac{F_0 \omega}{\sqrt{(k - m\omega^2)^2 + (c\omega)^2}}
$$

### Fórmulas Normalizadas

Para un análisis más general, se utilizan parámetros adimensionales:

- **Frecuencia natural no amortiguada:** `\omega_n = \sqrt{k/m}`
- **Razón de amortiguamiento:** `\zeta = c / (2\sqrt{km})`
- **Razón de frecuencias:** `r = \omega / \omega_n`
- **Desplazamiento estático:** `\delta_{st} = F_0 / k`

Con estos parámetros, las amplitudes se expresan como:

- **Magnificación del Desplazamiento:**

  $$
  \frac{X}{\delta_{st}} = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}
  $$

- **Amplitud de Velocidad Normalizada:**
  $$
  \frac{V}{\omega_n \delta_{st}} = \frac{r}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}
  $$

## 2. Sistema de Múltiples Grados de Libertad (MDOF)

Las estructuras reales se modelan como sistemas con múltiples grados de libertad, descritos por matrices.

### Ecuación Matricial del Movimiento

$$
 \mathbf{M} \ddot{\mathbf{u}}(t) + \mathbf{C} \dot{\mathbf{u}}(t) + \mathbf{K} \mathbf{u}(t) = \mathbf{F}(t)
$$

Donde `\mathbf{M}`, `\mathbf{C}`, y `\mathbf{K}` son las matrices globales de masa, amortiguamiento y rigidez, y `\mathbf{u}(t)` y `\mathbf{F}(t)` son los vectores de desplazamiento y fuerza.

Existen dos métodos principales para resolver esta ecuación en el dominio de la frecuencia.

### Método 1: Solución Directa en Frecuencia

Este método resuelve el sistema algebraico directamente para cada frecuencia de excitación `\omega`. Asumiendo una excitación `\mathbf{F}(t) = \mathbf{F}_0 e^{i\omega t}` y una respuesta `\mathbf{u}(t) = \mathbf{U} e^{i\omega t}`, la ecuación se transforma en:

$$
 (\mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C}) \mathbf{U} = \mathbf{F}_0
$$

Se define la **Matriz de Rigidez Dinámica** `\mathbf{Z}(\omega)`:

$$
 \mathbf{Z}(\omega) = \mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C}
$$

Y se resuelve el sistema de ecuaciones lineales complejas para el vector de amplitudes de desplazamiento complejas `\mathbf{U}`:

$$
 \mathbf{U} = [\mathbf{Z}(\omega)]^{-1} \mathbf{F}_0
$$

#### Amplitudes de Desplazamiento y Velocidad

- **Amplitud de Desplazamiento:** Para cada grado de libertad `j`, la amplitud es el módulo del número complejo `U_j`:
  $$
  A_j = |\mathbf{U}_j|
  $$
- **Amplitud de Velocidad:** La respuesta de velocidad en el dominio de la frecuencia es `\mathbf{V} = i\omega \mathbf{U}`. La amplitud de velocidad para el grado de libertad `j` es:
  $$
  V_j = |i\omega \mathbf{U}_j| = \omega |\mathbf{U}_j| = \omega A_j
  $$

Este método es robusto y es el implementado en `analisis_modal_3d/analysis/frequency_response.py`.

### Método 2: Superposición Modal

Este método es computacionalmente más eficiente para sistemas muy grandes.

1. **Análisis Modal:** Primero, se resuelven las frecuencias naturales `\omega_i` y las formas modales `\mathbf{\Phi}_i` del sistema no amortiguado.
2. **Coordenadas Modales:** Se transforma la respuesta de coordenadas físicas `\mathbf{u}(t)` a coordenadas modales `\mathbf{q}(t)` usando la matriz modal `[\mathbf{\Phi}]`:
    $$
    \mathbf{u}(t) = [\mathbf{\Phi}] \mathbf{q}(t)
    $$
3. **Ecuaciones Desacopladas:** Este cambio de base desacopla el sistema matricial en `N` ecuaciones SDOF independientes, una para cada modo `i`:
    $$
    M_i \ddot{q}_i(t) + C_i \dot{q}_i(t) + K_i q_i(t) = F_i(t)
    $$
    Donde `M_i`, `C_i`, `K_i` y `F_i(t)` son la masa, amortiguamiento, rigidez y fuerza modales.
4. **Solución Modal:** Se resuelve cada ecuación SDOF para encontrar la amplitud de velocidad en coordenadas modales `V_{q_i}` usando la fórmula SDOF.
5. **Superposición:** La respuesta de velocidad final en coordenadas físicas se obtiene combinando las contribuciones de cada modo. Es crucial notar que las respuestas modales tienen diferentes fases, por lo que no se pueden sumar sus amplitudes directamente. La combinación se realiza en el dominio del tiempo o usando fasores complejos:
    $$
    \mathbf{v}(t) = \dot{\mathbf{u}}(t) = [\mathbf{\Phi}] \dot{\mathbf{q}}(t)
    $$

## 3. Implementación en el Proyecto

El flujo de trabajo en este proyecto (`harmonic_analysis.py`) utiliza el **Método de Solución Directa**:

1. Ensambla las matrices `\mathbf{K}` y `\mathbf{M}`.
2. Realiza un análisis modal para encontrar las `\omega_n` necesarias para el amortiguamiento.
3. Calcula la matriz de amortiguamiento `\mathbf{C}` (usando el método de Rayleigh).
4. Para un rango de frecuencias de excitación `\omega`:
    a. Define el vector de fuerza `\mathbf{F}_0`.
    b. Construye y resuelve `\mathbf{Z}(\omega) \mathbf{U} = \mathbf{F}_0` para obtener las amplitudes de desplazamiento complejas `\mathbf{U}`.
    c. Calcula las amplitudes de velocidad como `V_j = \omega |\mathbf{U}_j|`.
5. Procesa y visualiza los resultados.


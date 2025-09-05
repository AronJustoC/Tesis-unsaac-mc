# Respuesta Armónica Matricial: Teoría y Desarrollo

## 1. Ecuación General del Sistema

Para un sistema con nn grados de libertad (GDL) sometido a fuerzas armónicas externas:

$$
\mathbf{M} \ddot{\mathbf{u}}(t) + \mathbf{C} \dot{\mathbf{u}}(t) + \mathbf{K} \mathbf{u}(t) = \mathbf{F}(t)
$$

Donde:

- $\mathbf{M}$: Matriz de masa (n×n)
- $\mathbf{C}$: Matriz de amortiguamiento (n×n, asumida nula si no se especifica)
- $\mathbf{K}$: Matriz de rigidez (n×n)
- $\mathbf{u}(t)$: Vector de desplazamientos (n×1)
- $\mathbf{F}(t) = \mathbf{F}_0 e^{i\omega t}$: Fuerza armónica externa, con:
  - $\mathbf{F}_0$: Vector de magnitudes complejas (n×1)
  - $\omega$: Frecuencia de excitación (rad/s)

## 2. Solución Asumida para Respuesta Permanente

Se asume una solución armónica de la misma frecuencia que la fuerza externa:

$$
\mathbf{u}(t) = \mathbf{U} e^{i\omega t}
$$

Donde $\mathbf{U}$ es un vector complejo (n×1) que contiene amplitudes y fases.
Derivando y sustituyendo en la ecuación:

$$
\left( -\omega^2 \mathbf{M} + i\omega \mathbf{C} + \mathbf{K} \right) \mathbf{U} e^{i\omega t} = \mathbf{F}_0 e^{i\omega t}
$$

## 3. Ecuación Algebraica en el Dominio de la Frecuencia

Se obtiene el sistema lineal:

$$
\boxed{\mathbf{Z}(\omega) \mathbf{U} = \mathbf{F}_0}
$$

Donde $\mathbf{Z}(\omega)$ es la matriz de impedancia dinámica:

$$
\mathbf{Z}(\omega) = \mathbf{K} - \omega^2 \mathbf{M} + i\omega \mathbf{C}
$$

## 4. Relación con el Análisis Modal

Si se realizó un análisis modal previo (sin fuerzas externas), se tienen:

- Frecuencias naturales: $\omega_r$ (rad/s)
- Modos de vibración: $\boldsymbol{\Phi} = [\boldsymbol{\phi}_1, \boldsymbol{\phi}_2, \dots, \boldsymbol{\phi}_n]$

Los modos son $\mathbf{M}$-ortonormales:

$$
\boldsymbol{\Phi}^T \mathbf{M} \boldsymbol{\Phi} = \mathbf{I}, \quad \boldsymbol{\Phi}^T \mathbf{K} \boldsymbol{\Phi} = \boldsymbol{\Omega}^2
$$

Con $\boldsymbol{\Omega}^2 = \text{diag}(\omega_1^2, \omega_2^2, \dots, \omega_n^2)$.

## 5. Descomposición Modal de la Respuesta

La solución se expresa como combinación lineal de los modos:

$$
\mathbf{U} = \sum_{r=1}^{n} \eta_r \boldsymbol{\phi}_r = \boldsymbol{\Phi} \boldsymbol{\eta}
$$

Sustituyendo en la ecuación de impedancia y premultiplicando por $\boldsymbol{\Phi}^T$:

$$
\boldsymbol{\Phi}^T \mathbf{Z}(\omega) \boldsymbol{\Phi} \boldsymbol{\eta} = \boldsymbol{\Phi}^T \mathbf{F}_0
$$

## 6. Ecuación Desacoplada (Modos Reales)

Si $\mathbf{C} = 0$ o es proporcional (amortiguamiento Rayleigh), el sistema se desacopla:

$$
\left[ -\omega^2 \mathbf{I} + \boldsymbol{\Omega}^2 \right] \boldsymbol{\eta} = \boldsymbol{\Phi}^T \mathbf{F}_0
$$

Cada modo $r$ tiene una ecuación independiente:

$$
\boxed{(-\omega^2 + \omega_r^2) \eta_r = \phi_r^T \mathbf{F}_0}
$$

## 7. Solución por Modos

La amplitud compleja del modo $r$ es:

$$
\eta_r = \frac{\boldsymbol{\phi}_r^T \mathbf{F}_0}{\omega_r^2 - \omega^2}
$$

Nota: Si $\omega \approx \omega_r$, hay resonancia (amplitud $\eta_r \to \infty$).

## 8. Respuesta Física Total

$$
\mathbf{u}(t) = \Re \left\{ \left( \sum_{r=1}^{n} \eta_r \boldsymbol{\phi}_r \right) e^{i\omega t} \right\}
$$

- $\eta_r$: Amplitud compleja del modo $r$ (incluye fase).
- $\boldsymbol{\phi}_r$: Vector modal del modo $r$.

## 9. Caso con Amortiguamiento No Proporcional

Si $\mathbf{C}$ no es diagonalizable por los modos, se resuelve:

$$
\mathbf{Z}(\omega) \mathbf{U} = \mathbf{F}_0
$$

Requiere:

- Inversión directa: $\mathbf{U} = \mathbf{Z}^{-1}(\omega) \mathbf{F}_0$ (costoso para sistemas grandes).
- Descomposición espectral o métodos iterativos.

## 10. Diagrama de Flujo para Implementación

```mermaid
graph TD
    A[Inicio] --> B{Definir M, K, C, F0, ω};
    B --> C{Análisis Modal};
    C --> D{Obtener ω_r, Φ};
    D --> E{Calcular Fuerza Modal Q = Φ^T * F0};
    E --> F{Para cada modo r};
    F --> G{Calcular η_r = Q_r / (ω_r^2 - ω^2)};
    G --> H{Fin Para};
    H --> I{Calcular U = Σ η_r * φ_r};
    I --> J{Respuesta u(t) = Re(U * e^(iωt))};
    J --> K[Fin];
```

## Ejemplo: Sistema de 3 GDL

$
\mathbf{M} = \begin{bmatrix} 2 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}, \quad
\mathbf{K} = \begin{bmatrix} 300 & -100 & 0 \\ -100 & 200 & -100 \\ 0 & -100 & 100 \end{bmatrix}, \quad
\mathbf{F}_0 = \begin{bmatrix} 10 \\ 0 \\ 0 \end{bmatrix} e^{i \cdot 4t}
$

- **Análisis modal previo (valores asumidos para el ejemplo):**

  - $\omega_1 = 5.0 \ \text{rad/s}, \quad \omega_2 = 10.0 \ \text{rad/s}, \quad \omega_3 = 15.0 \ \text{rad/s}$
  - $\boldsymbol{\phi}_1 = [0.3, 0.6, 0.7]^T, \quad \boldsymbol{\phi}_2 = [0.8, -0.5, -0.3]^T, \quad \boldsymbol{\phi}_3 = [0.5, 0.6, -0.6]^T$

- **Fuerza modal:**

  - $Q_1 = \boldsymbol{\phi}_1^T \mathbf{F}_0 = 0.3 \cdot 10 = 3.0$
  - $Q_2 = \boldsymbol{\phi}_2^T \mathbf{F}_0 = 0.8 \cdot 10 = 8.0$
  - $Q_3 = \boldsymbol{\phi}_3^T \mathbf{F}_0 = 0.5 \cdot 10 = 5.0$

- **Coordenadas modales ($\omega = 4 \ \text{rad/s}$):**

  - $\eta_1 = \frac{3.0}{5^2 - 4^2} = \frac{3.0}{9} = 0.333$
  - $\eta_2 = \frac{8.0}{10^2 - 4^2} = \frac{8.0}{84} = 0.095$
  - $\eta_3 = \frac{5.0}{15^2 - 4^2} = \frac{5.0}{209} = 0.024$

- **Respuesta física:**
  $
\mathbf{U} = \eta_1 \boldsymbol{\phi}_1 + \eta_2 \boldsymbol{\phi}_2 + \eta_3 \boldsymbol{\phi}_3 = 0.333 \begin{bmatrix} 0.3 \\ 0.6 \\ 0.7 \end{bmatrix} + 0.095 \begin{bmatrix} 0.8 \\ -0.5 \\ -0.3 \end{bmatrix} + 0.024 \begin{bmatrix} 0.5 \\ 0.6 \\ -0.6 \end{bmatrix} = \begin{bmatrix} 0.188 \\ 0.167 \\ 0.190 \end{bmatrix}
$

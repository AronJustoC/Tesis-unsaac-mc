# ANÁLISIS VIBRACIONAL DE ESTRUCTURAS MEDIANTE MÉTODO MATRICIAL

## 1. FUNDAMENTOS TEÓRICOS

### 1.1 Introducción
El análisis vibracional permite estudiar el comportamiento dinámico de estructuras mediante la determinación de sus **frecuencias naturales**, **modos de vibración** y respuesta a cargas externas. El método matricial combina teoría de vibraciones con matrices de rigidez y masa para modelar sistemas complejos.

### 1.2 Principios Básicos
- **Compatibilidad**: Continuidad de desplazamientos en la estructura.
- **Equilibrio**: $\sum F = [M]\{\ddot{u}\} + [C]\{\dot{u}\} + [K]\{u\}$.
- **Linealidad**: Validez del principio de superposición.

---

## 2. FORMULACIÓN MATRICIAL

### 2.1 Ecuación del Movimiento
La ecuación dinámica en forma matricial es:

$$
[M]\{\ddot{u}\} + [C]\{\dot{u}\} + [K]\{u\} = \{F(t)\}
$$

**Variables**:
- $[M] \in \mathbb{R}^{n \times n}$: Matriz de masa (diagonal o consistente).
- $[C] \in \mathbb{R}^{n \times n}$: Matriz de amortiguamiento (usualmente Rayleigh: $[C] = \alpha[M] + \beta[K]$).
- $[K] \in \mathbb{R}^{n \times n}$: Matriz de rigidez global.
- $\{u\}$: Vector de desplazamientos nodales ($n \times 1$).

---

### 2.2 Matriz de Rigidez Global

#### Matriz de Rigidez Local (Elemento Frame 3D)
Para un elemento estructural en 3D con 12 GDL:

```math
k_{local} = \begin{bmatrix}
\frac{EA}{L} & 0 & 0 & 0 & 0 & 0 & -\frac{EA}{L} & 0 & 0 & 0 & 0 & 0 \\
0 & \frac{12EI_y}{L^3} & 0 & 0 & 0 & \frac{6EI_y}{L^2} & 0 & -\frac{12EI_y}{L^3} & 0 & 0 & 0 & \frac{6EI_y}{L^2} \\
0 & 0 & \frac{12EI_z}{L^3} & 0 & -\frac{6EI_z}{L^2} & 0 & 0 & 0 & -\frac{12EI_z}{L^3} & 0 & -\frac{6EI_z}{L^2} & 0 \\
0 & 0 & 0 & \frac{GJ}{L} & 0 & 0 & 0 & 0 & 0 & -\frac{GJ}{L} & 0 & 0 \\
0 & 0 & -\frac{6EI_z}{L^2} & 0 & \frac{4EI_z}{L} & 0 & 0 & 0 & \frac{6EI_z}{L^2} & 0 & \frac{2EI_z}{L} & 0 \\
0 & \frac{6EI_y}{L^2} & 0 & 0 & 0 & \frac{4EI_y}{L} & 0 & -\frac{6EI_y}{L^2} & 0 & 0 & 0 & \frac{2EI_y}{L} \\
- \frac{EA}{L} & 0 & 0 & 0 & 0 & 0 & \frac{EA}{L} & 0 & 0 & 0 & 0 & 0 \\
0 & -\frac{12EI_y}{L^3} & 0 & 0 & 0 & -\frac{6EI_y}{L^2} & 0 & \frac{12EI_y}{L^3} & 0 & 0 & 0 & -\frac{6EI_y}{L^2} \\
0 & 0 & -\frac{12EI_z}{L^3} & 0 & \frac{6EI_z}{L^2} & 0 & 0 & 0 & \frac{12EI_z}{L^3} & 0 & \frac{6EI_z}{L^2} & 0 \\
0 & 0 & 0 & -\frac{GJ}{L} & 0 & 0 & 0 & 0 & 0 & \frac{GJ}{L} & 0 & 0 \\
0 & 0 & -\frac{6EI_z}{L^2} & 0 & \frac{2EI_z}{L} & 0 & 0 & 0 & \frac{6EI_z}{L^2} & 0 & \frac{4EI_z}{L} & 0 \\
0 & \frac{6EI_y}{L^2} & 0 & 0 & 0 & \frac{2EI_y}{L} & 0 & -\frac{6EI_y}{L^2} & 0 & 0 & 0 & \frac{4EI_y}{L}
\end{bmatrix}
```

#### Transformación a Coordenadas Globales
$$
[K_{global}] = [T]^T [k_{local}] [T]
$$
- $[T]$: Matriz de transformación (ángulos de orientación del elemento).

---

### 2.3 Matriz de Masa Consistente
Para elementos frame 3D:

```math
[M_e] = \frac{\rho A L}{420}
\begin{bmatrix}
140 & 0 & 0 & 0 & 0 & 0 & 70 & 0 & 0 & 0 & 0 & 0 \\
0 & 156 & 0 & 0 & 0 & 22L & 0 & 54 & 0 & 0 & 0 & -13L \\
0 & 0 & 156 & 0 & -22L & 0 & 0 & 0 & 54 & 0 & -13L & 0 \\
0 & 0 & 0 & 140 & 0 & 0 & 0 & 0 & 0 & 70 & 0 & 0 \\
0 & 0 & -22L & 0 & 4L^2 & 0 & 0 & 0 & -13L & 0 & -3L^2 & 0 \\
0 & 22L & 0 & 0 & 0 & 4L^2 & 0 & 13L & 0 & 0 & 0 & -3L^2 \\
70 & 0 & 0 & 0 & 0 & 0 & 140 & 0 & 0 & 0 & 0 & 0 \\
0 & 54 & 0 & 0 & 0 & 13L & 0 & 156 & 0 & 0 & 0 & -22L \\
0 & 0 & 54 & 0 & -13L & 0 & 0 & 0 & 156 & 0 & -22L & 0 \\
0 & 0 & 0 & 70 & 0 & 0 & 0 & 0 & 0 & 140 & 0 & 0 \\
0 & 0 & -13L & 0 & -3L^2 & 0 & 0 & 0 & -22L & 0 & 4L^2 & 0 \\
0 & -13L & 0 & 0 & 0 & -3L^2 & 0 & -22L & 0 & 0 & 0 & 4L^2
\end{bmatrix}
```

---

## 3. ANÁLISIS MODAL AMPLIADO

### 3.1 Problema de Autovalores
El sistema homogéneo ($\{F(t)\} = 0$) se reduce a:

$$
[K]\{\phi\} = \omega^2 [M]\{\phi\}
$$
- $\omega^2$: Autovalores (cuadrado de las frecuencias angulares).
- $\{\phi\}$: Autovectores (modos de vibración).

### 3.2 Solución del Determinante
Las frecuencias naturales se obtienen resolviendo:

$$
\det\left([K] - \omega^2 [M]\right) = 0
$$

### 3.3 Frecuencias Naturales
Cada autovalor $\omega_i^2$ corresponde a una frecuencia natural:

$$
f_i = \frac{\omega_i}{2\pi} \quad \text{(Hz)}
$$

### 3.4 Modos de Vibración
Los autovectores $\{\phi_i\}$ representan la forma modal asociada a $\omega_i$. Se normalizan con:

$$
\{\phi_i\}^T [M] \{\phi_i\} = 1
$$

### 3.5 Propiedades de Ortogonalidad
- Ortogonalidad en masa: $\{\phi_i\}^T [M] \{\phi_j\} = 0 \quad (i \neq j)$
- Ortogonalidad en rigidez: $\{\phi_i\}^T [K] \{\phi_j\} = 0 \quad (i \neq j)$

### 3.6 Matriz Modal
Agrupando todos los modos:

$$
[\Phi] = \begin{bmatrix} \{\phi_1\} & \{\phi_2\} & \cdots & \{\phi_n\} \end{bmatrix}
$$
- Diagonaliza $[K]$ y $[M]$:

$$
[\Phi]^T [K] [\Phi] = [\Omega^2], \quad [\Phi]^T [M] [\Phi] = [I]
$$

---

## 4. IMPLEMENTACIÓN COMPUTACIONAL

### Pasos Clave:
1. **Discretización**: Dividir la estructura en elementos finitos.
2. **Ensamblaje**:
   - Sumar contribuciones de $[K_{local}]$ y $[M_{local}]$ a las matrices globales.
3. **Aplicación de Restricciones**:
   - Eliminar filas/columnas correspondientes a GDL restringidos.
4. **Solución Modal**:
   - Métodos: Iteración inversa, Jacobi, Lanczos.
5. **Postproceso**:
   - Visualización de modos.
   - Cálculo de participación modal.

---

## 5. ANÁLISIS DE RESULTADOS

### 5.1 Interpretación de Modos
- **Modo 1**: Forma de vibración asociada a la frecuencia más baja (generalmente flexión o torsión).
- **Modos Superiores**: Patrones complejos con nodos vibratorios.

### 5.2 Separación Modal
Para evitar acoplamiento dinámico, se recomienda:

$$
\frac{f_j}{f_i} > 1.2 \quad \forall i,j \ (i \neq j)
$$

### 5.3 Factores de Participación
Miden la contribución de cada modo a la respuesta global:

$$
\gamma_i = \frac{\{\phi_i\}^T [M] \{1\}}{\sqrt{\{\phi_i\}^T [M] \{\phi_i\}}}
$$

---

**Nota**: Este documento es compatible con renderizadores de ecuaciones como **MathJax** o **KaTeX**.

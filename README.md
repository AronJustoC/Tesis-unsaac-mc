# ANÁLISIS VIBRACIONAL DE ESTRUCTURAS MEDIANTE MÉTODO MATRICIAL

## 1. FUNDAMENTOS TEÓRICOS

### 1.1 Introducción
El análisis vibracional de estructuras requiere un enfoque sistemático que combine la teoría de vibraciones con el método matricial de rigidez. Este método permite determinar las frecuencias naturales y modos de vibración de la estructura, elementos cruciales para evaluar su comportamiento dinámico.

### 1.2 Principios Fundamentales
- **Compatibilidad**: Las deformaciones son continuas y únicas en cada punto.
- **Equilibrio**: La estructura mantiene equilibrio estático bajo fuerzas externas e internas.
- **Linealidad**: Comportamiento lineal que permite aplicar superposición.

## 2. FORMULACIÓN MATRICIAL DEL PROBLEMA DINÁMICO

### 2.1 Ecuación General del Movimiento
La ecuación que gobierna el movimiento de la estructura es:

\[
[M]\{\ddot{u}\} + [C]\{\dot{u}\} + [K]\{u\} = \{F(t)\}
\]

Donde:
- \([M]\) = Matriz de masa
- \([C]\) = Matriz de amortiguamiento
- \([K]\) = Matriz de rigidez global
- \(\{u\}\) = Vector de desplazamientos
- \(\{F(t)\}\) = Vector de fuerzas externas

### 2.2 Desarrollo de la Matriz de Rigidez Global

#### 1. Matriz de Rigidez Local (Elemento Frame en 3D)
La matriz de rigidez de un elemento frame en 3D es de \(12 \times 12\):

\[
[k_{local}] = 
\begin{bmatrix}
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
\]

#### 2. Transformación al Sistema Global
\[
[K_{global}] = [T]^T[k_{local}][T]
\]

### 2.3 Matriz de Masa
Para un elemento frame en 3D, la matriz de masa consistente es:

\[
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
\]

## 3. ANÁLISIS MODAL

1. Ensamblar matriz de rigidez global \([K]\).
2. Ensamblar matriz de masa global \([M]\).
3. Resolver \(det([K] - \omega^2[M]) = 0\).
4. Calcular frecuencias naturales \(f_n = \frac{\omega_n}{2\pi}\).
5. Determinar modos de vibración.

## 4. IMPLEMENTACIÓN COMPUTACIONAL
- Definir la estructura.
- Calcular matrices locales y globales.
- Resolver ecuaciones modales.

## 5. ANÁLISIS DE RESULTADOS
- Interpretación de modos.
- Evaluación de separación modal.
- Validación con datos experimentales.

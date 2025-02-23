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

$$
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
$$

#### Matriz de Transformación de Coordenadas Locales a Globales

Para transformar la matriz de rigidez local a coordenadas globales se utiliza la matriz de transformación [T]:

$$
[K_{global}] = [T]^T [k_{local}] [T]
$$

Donde:
- [T]: Matriz que convierte las coordenadas locales del elemento a coordenadas globales.
- Los cosenos directores ($l_x, m_x, n_x, l_y, m_y, n_y, l_z, m_z, n_z$) definen la orientación del elemento:
   - $l_x, m_x, n_x$: Proyecciones del eje local x sobre los ejes globales X, Y, Z.
   - $l_y, m_y, n_y$: Proyecciones del eje local y sobre los ejes globales X, Y, Z.
   - $l_z, m_z, n_z$: Proyecciones del eje local z sobre los ejes globales X, Y, Z.

Ejemplo de matriz de transformación para un elemento frame 3D con 12 grados de libertad:

$$
[T] = \begin{bmatrix}
l_x & m_x & n_x & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0 \\
l_y & m_y & n_y & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0 \\
l_z & m_z & n_z & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0 \\
0   & 0   & 0   & l_x & m_x & n_x & 0   & 0   & 0   & 0   & 0   & 0 \\
0   & 0   & 0   & l_y & m_y & n_y & 0   & 0   & 0   & 0   & 0   & 0 \\
0   & 0   & 0   & l_z & m_z & n_z & 0   & 0   & 0   & 0   & 0   & 0 \\
0   & 0   & 0   & 0   & 0   & 0   & l_x & m_x & n_x & 0   & 0   & 0 \\
0   & 0   & 0   & 0   & 0   & 0   & l_y & m_y & n_y & 0   & 0   & 0 \\
0   & 0   & 0   & 0   & 0   & 0   & l_z & m_z & n_z & 0   & 0   & 0 \\
0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & l_x & m_x & n_x \\
0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & l_y & m_y & n_y \\
0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & 0   & l_z & m_z & n_z
\end{bmatrix}
$$

Esta matriz se emplea para transformar tanto las matrices de rigidez como las de masa de los elementos estructurales.

---

### 2.3 Matriz de Masa Consistente
Para elementos frame 3D:

$$
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
$$

---

## 3. ANÁLISIS MODAL AMPLIADO

### 3.1 Problema de Autovalores
Para el sistema homogéneo ($\{F(t)\} = 0$), la ecuación de movimiento se reduce a:

$$
[K]\{\phi\} = \omega^2 [M]\{\phi\}
$$

Donde:
- $\omega^2$ son los autovalores (cuadrado de las frecuencias angulares).
- $\{\phi\}$ son los autovectores (modos de vibración).

### 3.2 Solución del Determinante
Las frecuencias naturales se obtienen resolviendo el determinante:

$$
\det\left([K] - \omega^2 [M]\right) = 0
$$

### 3.3 Frecuencias Naturales
Cada autovalor $\omega_i^2$ corresponde a una frecuencia natural:

$$
f_i = \frac{\omega_i}{2\pi} \quad \text{(Hz)}
$$

### 3.4 Modos de Vibración
Los autovectores $\{\phi_i\}$ representan la forma modal asociada a $\omega_i$. Se normalizan de la siguiente manera:

$$
\{\phi_i\}^T [M] \{\phi_i\} = 1
$$

### 3.5 Propiedades de Ortogonalidad
- Ortogonalidad en masa: $\{\phi_i\}^T [M] \{\phi_j\} = 0 \quad (i \neq j)$
- Ortogonalidad en rigidez: $\{\phi_i\}^T [K] \{\phi_j\} = 0 \quad (i \neq j)$

### 3.6 Matriz Modal
Agrupando todos los modos de vibración en una matriz modal:

$$
[\Phi] = \begin{bmatrix} \{\phi_1\} & \{\phi_2\} & \cdots & \{\phi_n\} \end{bmatrix}
$$

Esta matriz diagonaliza $[K]$ y $[M]$:

$$
[\Phi]^T [K] [\Phi] = [\Omega^2], \quad [\Phi]^T [M] [\Phi] = [I]
$$

### 3.7 Solución Modal

El análisis modal es crucial en la dinámica estructural, permitiendo descomponer el comportamiento vibratorio en modos naturales. A continuación, se describen dos métodos comunes para la solución modal:

1. **Método de Lanczos**:
   - **Descripción**: Algoritmo iterativo para encontrar autovalores y autovectores de matrices grandes y dispersas.
   - **Proceso**:
     - Inicia con un vector de prueba $\{v\}$.
     - Genera una secuencia de Krylov: $\{v\}, [K]^{-1}[M]\{v\}, ([K]^{-1}[M])^2\{v\}, \ldots$.
     - Construye una base ortogonal que aproxima los autovectores.
     - Obtiene autovalores resolviendo un problema reducido en esta base.
   - **Ventajas**:
     - Eficiente para matrices dispersas grandes.
     - Convergencia rápida para los primeros modos de vibración.
     - Reduce el problema original a uno de menor dimensión.

2. **Normalización**:
   - **Descripción**: Asegura que los autovectores tengan una magnitud consistente.
   - **Proceso**:
     - **Normalización respecto a la masa**: Ajusta cada autovector $\{\phi\}$ para que $\{\phi\}^T[M]\{\phi\} = 1$.
     - **Factores de participación modal**: Miden la contribución de cada modo a la respuesta global:
       $$
       \gamma_i = \frac{\{\phi_i\}^T [M] \{1\}}{\sqrt{\{\phi_i\}^T [M] \{\phi_i\}}}
       $$
     - Facilita la comparación entre modos y la interpretación de su importancia relativa.

Estos métodos son esenciales para realizar un análisis modal preciso y eficiente, permitiendo a los ingenieros comprender mejor el comportamiento dinámico de las estructuras.


---
# Análisis Modal Estructural 3D

## Descripción
Software de análisis modal para estructuras tridimensionales basado en el método de elementos finitos (MEF). Permite realizar análisis dinámico de estructuras considerando elementos tipo viga en 3D con 6 grados de libertad por nodo.

## Características Principales
- Análisis modal completo en 3D
- Elementos tipo viga con 6 GDL por nodo
- Matrices dispersas para optimización de memoria
- Visualización 3D de modos de vibración
- Exportación de resultados en formato pickle
- Integración temporal mediante método Newmark-β

## Requisitos
```bash
Python >= 3.8
numpy >= 1.21.0
scipy >= 1.7.0
matplotlib >= 3.4.0
```

## Instalación
1. Clonar el repositorio:
```bash
git clone https://github.com/usuario/analisis-modal-3d.git
cd analisis-modal-3d
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto
```
analisis-modal-3d/
├── src/
│   ├── __init__.py
│   ├── structures/
│   │   ├── __init__.py
│   │   ├── node.py
│   │   ├── element.py
│   │   └── structure.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── assembler.py
│   │   ├── modal.py
│   │   └── dynamic.py
│   └── visualization/
│       ├── __init__.py
│       └── plotter.py
├── examples/
│   ├── simple_beam.py
│   └── space_frame.py
├── tests/
│   └── test_modal.py
├── docs/
│   └── theory.pdf
├── requirements.txt
└── README.md
```

## Uso Básico

```python
from src.structures import Structure, Node, Element
from src.analysis import modal_analysis, dynamic_response
from src.visualization import plot_mode_shape

# Crear estructura
structure = Structure()

# Añadir nodos
n1 = structure.add_node(0, 0, 0)
n2 = structure.add_node(0, 0, 3)

# Definir propiedades
section = {
    'area': 0.01,
    'Ix': 8.33e-6,
    'Iy': 8.33e-6,
    'Iz': 1.67e-5
}

material = {
    'E': 200e9,    # Módulo de Young
    'G': 76.9e9,   # Módulo de cortante
    'rho': 7850    # Densidad
}

# Añadir elemento
element = structure.add_element(n1, n2, section, material)

# Realizar análisis modal
frequencies, modes = modal_analysis(structure, num_modes=5)

# Visualizar primer modo
plot_mode_shape(structure, modes[:, 0])
```

## Ejemplos Incluidos
1. `simple_beam.py`: Análisis de una viga en voladizo
2. `space_frame.py`: Pórtico espacial con múltiples elementos

## Funcionalidades Detalladas

### Análisis Modal
- Solución del problema de autovalores generalizado
- Normalización de modos respecto a la masa
- Cálculo de frecuencias naturales y modos de vibración
- Método de Lanczos para sistemas grandes

### Análisis Dinámico
- Integración temporal mediante Newmark-β
- Superposición modal
- Respuesta a cargas armónicas
- Respuesta transitoria

### Visualización
- Gráficos 3D interactivos
- Animación de modos de vibración
- Deformadas modales
- Exportación de gráficos

## Documentación
La documentación completa se encuentra en `docs/theory.pdf`, incluyendo:
- Fundamento teórico
- Ejemplos detallados
- Referencia de API
- Guía de usuario

## Tests
Ejecutar suite de pruebas:
```bash
python -m pytest tests/
```

## Contribuciones
1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request


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
## Contacto
Nombre - email@ejemplo.com
Project Link: https://github.com/usuario/analisis-modal-3d

## Referencias
1. Bathe, K.J. (1996). Finite Element Procedures
2. Cook, R.D. (2001). Concepts and Applications of Finite Element Analysis
3. Zienkiewicz, O.C. (2000). The Finite Element Method


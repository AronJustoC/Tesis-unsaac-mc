import numpy as np

class Element:
    def __init__(self, node1, node2, section, material):
        self.nodes = (node1, node2)
        self.section = section
        self.material = material
        self._compute_length()
        self._compute_local_stiffness()
        self._compute_transformation_matrix()
        self._compute_global_stiffness()
        self._compute_local_mass()
        self._compute_global_mass()

    def _compute_length(self):
        p1 = np.array(self.nodes[0].coords)
        p2 = np.array(self.nodes[1].coords)
        self.L = np.linalg.norm(p2 - p1)

    def _compute_local_stiffness(self):
        E = self.material["E"]
        G = self.material["G"]
        A = self.section["area"]
        Iy = self.section["Iy"]
        Iz = self.section["Iz"]
        J = self.section["Ix"]
        L = self.L

        self.k_local = np.zeros((12, 12))

        # Parametros para la escritura dela matriz
        axial = E * A / L
        flex_y_1 = 12 * E * Iz / L**3
        flex_y_2 = 12 * E * Iy / L**3
        torsion = G * J / L

        # Terminos de flexion
        rot_y_1 = 6 * E * Iz / L**2
        rot_z_1 = 6 * E * Iy / L**2

        # Rotaciones
        flex_y_3 = 4 * E * Iy / L
        flex_y_4 = 2 * E * Iy / L
        flex_z_1 = 4 * E * Iz / L
        flex_z_2 = 2 * E * Iz / L

        # Llenando la matriz de rigidez local
        # Asignación de valores según la simetría
        self.k_local[0, 0] = axial
        self.k_local[0, 6] = -axial
        self.k_local[6, 0] = -axial
        self.k_local[6, 6] = axial

        self.k_local[1, 1] = flex_y_1
        self.k_local[1, 5] = rot_y_1
        self.k_local[1, 7] = -flex_y_1
        self.k_local[1, 11] = rot_y_1

        self.k_local[2, 2] = flex_y_2
        self.k_local[2, 4] = rot_z_1
        self.k_local[2, 8] = -flex_y_2
        self.k_local[2, 10] = rot_z_1

        self.k_local[3, 3] = torsion
        self.k_local[3, 9] = -torsion
        self.k_local[9, 3] = -torsion
        self.k_local[9, 9] = torsion

        self.k_local[4, 2] = rot_z_1
        self.k_local[4, 4] = flex_z_1
        self.k_local[4, 8] = -rot_z_1
        self.k_local[4, 10] = flex_z_2

        self.k_local[5, 1] = rot_y_1
        self.k_local[5, 5] = flex_y_3
        self.k_local[5, 7] = -rot_y_1
        self.k_local[5, 11] = flex_y_4

        self.k_local[7, 1] = -flex_y_1
        self.k_local[7, 5] = -rot_y_1
        self.k_local[7, 7] = flex_y_1
        self.k_local[7, 11] = -rot_y_1

        self.k_local[8, 2] = -flex_y_2
        self.k_local[8, 4] = -rot_z_1
        self.k_local[8, 8] = flex_y_2
        self.k_local[8, 10] = -rot_z_1

        self.k_local[10, 2] = rot_z_1
        self.k_local[10, 4] = flex_z_2
        self.k_local[10, 8] = -rot_z_1
        self.k_local[10, 10] = flex_z_1

        self.k_local[11, 1] = rot_y_1
        self.k_local[11, 5] = flex_y_4
        self.k_local[11, 7] = -rot_y_1
        self.k_local[11, 11] = flex_y_3

    def _compute_transformation_matrix(self):
        # Calculo de cosenos directores
        # Coordenadas de los nodos del elemento
        p1 = np.array(self.nodes[0].coords)
        p2 = np.array(self.nodes[1].coords)
        # Vector direccion
        dx = p2 - p1
        L = np.linalg.norm(dx)  # longitud del elemento

        if L < 1e-10:
            raise ValueError("Elemento tiene longitud cero.")

        # Vector unitario del eje local x (l)
        l = dx / L

        # Vector de referencia para calcular ejes locales y/z
        v_ref = np.array([1.0, 0.0, 0.0])  # Eje global X

        # Si el elemento es vertical (paralelo al eje Z)
        if np.abs(l[2]) > 0.999:
            v_ref = np.array([0.0, 1.0, 0.0])  # Usar eje global Y como referencia

        # Calcular vector temporal para eje local y
        m_temp = np.cross(v_ref, l)
        if (
            np.linalg.norm(m_temp) < 1e-10
        ):  # Caso especial para elementos alinieados
            v_ref = np.array([0.0, 0.0, 1.0])  # Usar eje global Z como referencia
            m_temp = np.cross(v_ref, l)

        # Normalizar vectores locales
        m = m_temp / np.linalg.norm(m_temp)
        n = np.cross(l, m)

        # Matriz de rotacion 3x3
        R = np.column_stack((l, m, n))

        # Inicializa T como una matriz de ceros 12x12
        self.T = np.zeros((12, 12))

        # Llenar bloques diagolanes
        for i in range(0, 12, 3):
            self.T[i : i + 3, i : i + 3] = R

    def _compute_global_stiffness(self):
        self.k_global = self.T.T @ self.k_local @ self.T

    def _compute_local_mass(self):
        rho = self.material["rho"]
        A = self.section["area"]
        L = self.L
        Ix = self.section["Ix"]

        factor = rho * A * L / 420
        rx2 = Ix / A

        self.m_local = np.zeros((12, 12))

        # Términos diagonales principales
        self.m_local[0, 0] = 140
        self.m_local[1, 1] = 156
        self.m_local[2, 2] = 156
        self.m_local[3, 3] = 140 * rx2
        self.m_local[4, 4] = 4 * L**2
        self.m_local[5, 5] = 4 * L**2

        # Términos acoplados
        self.m_local[0, 6] = self.m_local[6, 0] = 70
        self.m_local[1, 5] = self.m_local[5, 1] = 22 * L
        self.m_local[1, 7] = self.m_local[7, 1] = 54
        self.m_local[1, 11] = self.m_local[11, 1] = -13 * L
        self.m_local[2, 4] = self.m_local[4, 2] = -22 * L
        self.m_local[2, 8] = self.m_local[8, 2] = 54
        self.m_local[2, 10] = self.m_local[10, 2] = 13 * L
        self.m_local[3, 9] = self.m_local[9, 3] = 70 * rx2
        self.m_local[4, 8] = self.m_local[8, 4] = 13 * L
        self.m_local[4, 10] = self.m_local[10, 4] = -3 * L**2
        self.m_local[5, 7] = self.m_local[7, 5] = -13 * L
        self.m_local[5, 11] = self.m_local[11, 5] = -3 * L**2

        # Bloque inferior derecho
        self.m_local[6, 6] = 140
        self.m_local[7, 7] = 156
        self.m_local[8, 8] = 156
        self.m_local[9, 9] = 140 * rx2
        self.m_local[10, 10] = 4 * L**2
        self.m_local[11, 11] = 4 * L**2

        # Multiplicar por factor escalar
        self.m_local *= factor

        # Asegurarse de que la matriz de masa sea definida positiva
        self.m_local += np.eye(12) * 1e-6

    def _compute_global_mass(self):
        """Transforma la matriz de masa a coordenadas globales"""
        self.m_global = self.T.T @ self.m_local @ self.T

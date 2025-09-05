import numpy as np


class Element:
    """Representa un elemento estructural en 3D (viga).

    Calcula las matrices de rigidez y masa locales y globales para el elemento.
    """
    def __init__(self, node1, node2, section, material):
        """Inicializa un nuevo elemento.

        Args:
            node1 (Node): El primer nodo del elemento.
            node2 (Node): El segundo nodo del elemento.
            section (dict): Un diccionario con las propiedades de la sección transversal
                            (e.g., 'area', 'Iy', 'Iz', 'Ix').
            material (dict): Un diccionario con las propiedades del material
                             (e.g., 'E', 'G', 'rho').
        """
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
        """Calcula la longitud del elemento y la almacena en self.L."""
        p1 = np.array(self.nodes[0].coords)
        p2 = np.array(self.nodes[1].coords)
        self.L = np.linalg.norm(p2 - p1)

    def _compute_local_stiffness(self):
        """Calcula la matriz de rigidez local del elemento y la almacena en self.k_local."""
        E = self.material["E"]
        G = self.material["G"]
        A = self.section["area"]
        Iy = self.section["Iy"]
        Iz = self.section["Iz"]
        J = self.section["Ix"]
        L = self.L

        # Parametros para la escritura dela matriz
        axial = E * A / L
        torsion = G * J / L
        
        # Terminos de flexion en el plano XY (flexion alrededor de Z)
        flex_xy_1 = 12 * E * Iz / L**3
        flex_xy_2 = 6 * E * Iz / L**2
        flex_xy_3 = 4 * E * Iz / L
        flex_xy_4 = 2 * E * Iz / L

        # Terminos de flexion en el plano XZ (flexion alrededor de Y)
        flex_xz_1 = 12 * E * Iy / L**3
        flex_xz_2 = 6 * E * Iy / L**2
        flex_xz_3 = 4 * E * Iy / L
        flex_xz_4 = 2 * E * Iy / L

        # Llenando la matriz de rigidez local
        # Matriz de rigidez para una viga 3D, segun manual de SAP2000
        self.k_local = np.array([
            [axial, 0, 0, 0, 0, 0, -axial, 0, 0, 0, 0, 0],
            [0, flex_xy_1, 0, 0, 0, flex_xy_2, 0, -flex_xy_1, 0, 0, 0, flex_xy_2],
            [0, 0, flex_xz_1, 0, -flex_xz_2, 0, 0, 0, -flex_xz_1, 0, -flex_xz_2, 0],
            [0, 0, 0, torsion, 0, 0, 0, 0, 0, -torsion, 0, 0],
            [0, 0, -flex_xz_2, 0, flex_xz_3, 0, 0, 0, flex_xz_2, 0, flex_xz_4, 0],
            [0, flex_xy_2, 0, 0, 0, flex_xy_3, 0, -flex_xy_2, 0, 0, 0, flex_xy_4],
            [-axial, 0, 0, 0, 0, 0, axial, 0, 0, 0, 0, 0],
            [0, -flex_xy_1, 0, 0, 0, -flex_xy_2, 0, flex_xy_1, 0, 0, 0, -flex_xy_2],
            [0, 0, -flex_xz_1, 0, flex_xz_2, 0, 0, 0, flex_xz_1, 0, flex_xz_2, 0],
            [0, 0, 0, -torsion, 0, 0, 0, 0, 0, torsion, 0, 0],
            [0, 0, -flex_xz_2, 0, flex_xz_4, 0, 0, 0, flex_xz_2, 0, flex_xz_3, 0],
            [0, flex_xy_2, 0, 0, 0, flex_xy_4, 0, -flex_xy_2, 0, 0, 0, flex_xy_3]
        ])

    def _compute_transformation_matrix(self):
        """Calcula la matriz de transformación del elemento y la almacena en self.T."""
        p1 = np.array(self.nodes[0].coords)
        p2 = np.array(self.nodes[1].coords)
        dx = p2 - p1
        L = np.linalg.norm(dx)

        if L < 1e-9:
            raise ValueError("La longitud del elemento no puede ser cero.")

        l, m, n = dx / L

        if np.isclose(l, 0) and np.isclose(m, 0):
            R_row1 = np.array([0, 0, 1 if n > 0 else -1])
            R_row2 = np.array([0, 1, 0])
            R_row3 = np.array([-1 if n > 0 else 1, 0, 0])
        else:
            R_row1 = np.array([l, m, n])
            D = np.sqrt(l**2 + m**2)
            R_row2 = np.array([-m/D, l/D, 0])
            R_row3 = np.cross(R_row1, R_row2)

        R = np.vstack([R_row1, R_row2, R_row3])
        
        self.T = np.zeros((12, 12))
        for i in range(4):
            self.T[i*3:(i+1)*3, i*3:(i+1)*3] = R

    def _compute_global_stiffness(self):
        """Calcula la matriz de rigidez global del elemento y la almacena en self.k_global."""
        self.k_global = self.T.T @ self.k_local @ self.T

    def _compute_local_mass(self):
        """Calcula la matriz de masa local 'lumped' (diagonal).

        Este método es numéricamente muy estable.
        """
        rho = self.material["rho"]
        A = self.section["area"]
        L = self.L
        total_mass = rho * A * L
        node_mass = total_mass / 2.0

        self.m_local = np.zeros((12, 12))

        # Asignar la mitad de la masa a las traslaciones de cada nodo
        np.fill_diagonal(self.m_local, [node_mass] * 3 + [0] * 3 + [node_mass] * 3 + [0] * 3)

        # Añadir una pequeña inercia rotacional para estabilidad numérica
        # Esto evita que las rotaciones tengan masa cero, lo que causa problemas.
        placeholder_inertia = 1e-5 * total_mass
        self.m_local[3, 3] = self.m_local[4, 4] = self.m_local[5, 5] = placeholder_inertia
        self.m_local[9, 9] = self.m_local[10, 10] = self.m_local[11, 11] = placeholder_inertia

    def _compute_global_mass(self):
        """Transforma la matriz de masa local a coordenadas globales."""
        self.m_global = self.T.T @ self.m_local @ self.T
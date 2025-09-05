from analisis_modal_3d.structures.element import Element
from analisis_modal_3d.structures.node import Node


class Structure:
    """Representa una estructura compuesta por nodos y elementos.

    Permite añadir nodos, elementos y definir restricciones de grados de libertad.
    """
    def __init__(self):
        """Inicializa una nueva estructura vacía."""
        self.nodes = []
        self.elements = []
        self.num_dofs = 0
        self.constraints = {}  # Dictionary to store node constraints

    def add_node(self, x, y, z):
        """Añade un nuevo nodo a la estructura.

        Args:
            x (float): Coordenada X del nodo.
            y (float): Coordenada Y del nodo.
            z (float): Coordenada Z del nodo.

        Returns:
            Node: El objeto Node recién creado.
        """
        node = Node(x, y, z)
        node.id = len(self.nodes)  # Asignar ID de nodo
        node.dofs = [node.id * 6 + i for i in range(6)]  # Asignar DOFs
        self.nodes.append(node)
        self.num_dofs += 6  # 3 traslaciones + 3 rotaciones
        return node

    def add_element(self, node1, node2, section, material):
        """Añade un nuevo elemento a la estructura.

        Args:
            node1 (Node): El primer nodo del elemento.
            node2 (Node): El segundo nodo del elemento.
            section (dict): Un diccionario con las propiedades de la sección transversal.
            material (dict): Un diccionario con las propiedades del material.

        Returns:
            Element: El objeto Element recién creado.
        """
        element = Element(node1, node2, section, material)
        self.elements.append(element)
        return element

    def add_constraint(self, node: Node, constrained_dofs: list[str]):
        """Añade restricciones a un nodo específico de la estructura.

        Args:
            node (Node): El objeto Node al que se le aplicarán las restricciones.
            constrained_dofs (list[str]): Una lista de cadenas que representan
                                         los grados de libertad a restringir.
                                         Valores posibles: 'ux', 'uy', 'uz'
                                         (traslaciones) y 'rx', 'ry', 'rz'
                                         (rotaciones).
        Raises:
            ValueError: Si el nodo no forma parte de la estructura o si se
                        proporciona un nombre de DOF inválido.
        """
        if node not in self.nodes:
            raise ValueError("Node is not part of the structure")

        # Map DOF names to indices
        dof_map = {
            "ux": 0,
            "uy": 1,
            "uz": 2,  # translations
            "rx": 3,
            "ry": 4,
            "rz": 5,  # rotations
        }

        # Validate DOF names
        for dof in constrained_dofs:
            if dof not in dof_map:
                raise ValueError(f"Invalid DOF name: {dof}")

        # Store constraint indices for this node
        node_index = self.nodes.index(node)
        constrained_indices = [dof_map[dof] for dof in constrained_dofs]
        self.constraints[node_index] = constrained_indices

    def get_global_dof_index(self, node_index: int, local_dof: int) -> int:
        """Convierte un índice de nodo y un índice de DOF local a un índice de DOF global.

        Args:
            node_index (int): El índice del nodo.
            local_dof (int): El índice del grado de libertad local (0-5).

        Returns:
            int: El índice del grado de libertad global.
        """
        return node_index * 6 + local_dof

    def get_constrained_dofs(self) -> list[int]:
        """Obtiene una lista de todos los índices de grados de libertad globales restringidos.

        Returns:
            list[int]: Una lista ordenada de los índices de grados de libertad restringidos.
        """
        constrained_dofs = []
        for node_index, local_dofs in self.constraints.items():
            for local_dof in local_dofs:
                global_dof = self.get_global_dof_index(node_index, local_dof)
                constrained_dofs.append(global_dof)
        return sorted(list(set(constrained_dofs)))

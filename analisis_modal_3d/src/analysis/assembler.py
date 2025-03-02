import numpy as np

class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.num_dofs = 0
        self.constraints = {}
        
    def add_node(self, x, y, z):
        """
        Añade un nodo a la estructura y asigna sus DOFs.
        """
        node = Node(x, y, z)
        self.nodes.append(node)
        
        # Asignar DOFs al nuevo nodo
        next_dof = node.assign_dofs(self.num_dofs)
        self.num_dofs = next_dof
        
        return node
        
    def add_element(self, node1, node2, section, material):
        """
        Añade un elemento entre dos nodos.
        Verifica que los nodos tengan DOFs asignados.
        """
        if not node1.dofs or not node2.dofs:
            raise ValueError("Los nodos deben tener DOFs asignados antes de crear elementos")
            
        element = Element(node1, node2, section, material)
        self.elements.append(element)
        return element
    
    def add_constraint(self, node, constrained_dofs):
        """
        Añade restricciones a un nodo.
        """
        if node not in self.nodes:
            raise ValueError("El nodo no es parte de la estructura")
        
        # Mapeo de nombres de DOF a índices locales
        dof_map = {
            'ux': 0, 'uy': 1, 'uz': 2,  # traslaciones
            'rx': 3, 'ry': 4, 'rz': 5   # rotaciones
        }
        
        # Validar nombres de DOF
        for dof in constrained_dofs:
            if dof not in dof_map:
                raise ValueError(f"Nombre de DOF inválido: {dof}")
        
        # Almacenar índices de DOFs restringidos para este nodo
        node_index = self.nodes.index(node)
        start_dof = node.dofs[0]  # primer DOF del nodo
        constrained_indices = [start_dof + dof_map[dof] for dof in constrained_dofs]
        self.constraints[node_index] = constrained_indices
    
    def get_constrained_dofs(self):
        """
        Obtiene lista de todos los DOFs restringidos.
        """
        all_constrained = []
        for constrained_dofs in self.constraints.values():
            all_constrained.extend(constrained_dofs)
        return sorted(all_constrained)

def assemble_global_matrices(structure):
    """
    Ensambla matrices globales completas (incluyendo DOFs restringidos).
    """
    num_dofs = structure.num_dofs
    K = np.zeros((num_dofs, num_dofs))
    M = np.zeros((num_dofs, num_dofs))
    
    for element in structure.elements:
        k_global = element.k_global
        m_global = element.m_global
        
        # Obtener índices de DOFs del elemento
        dof_indices = []
        for node in element.nodes:
            dof_indices.extend(node.dofs)
        
        # Ensamblar en matrices globales
        for i, dof_i in enumerate(dof_indices):
            for j, dof_j in enumerate(dof_indices):
                K[dof_i, dof_j] += k_global[i, j]
                M[dof_i, dof_j] += m_global[i, j]
    
    return K, M  # Matrices completas (sin eliminar restricciones)
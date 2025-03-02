from .node import Node
from .element import Element

class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.num_dofs = 0
        self.constraints = {}  # Dictionary to store node constraints
        
    def add_node(self, x, y, z):
        node = Node(x, y, z)
        node.id = len(self.nodes)  # Assign node ID
        self.nodes.append(node)
        self.num_dofs += 6  # 3 translations + 3 rotations
        return node
        
    def add_element(self, node1, node2, section, material):
        element = Element(node1, node2, section, material)
        self.elements.append(element)
        return element
    
    def add_constraint(self, node, constrained_dofs):
        """
        Add constraints to a node.
        
        Args:
            node: Node object to constrain
            constrained_dofs: List of DOFs to constrain ('ux','uy','uz','rx','ry','rz')
        """
        if node not in self.nodes:
            raise ValueError("Node is not part of the structure")
        
        # Map DOF names to indices
        dof_map = {
            'ux': 0, 'uy': 1, 'uz': 2,  # translations
            'rx': 3, 'ry': 4, 'rz': 5   # rotations
        }
        
        # Validate DOF names
        for dof in constrained_dofs:
            if dof not in dof_map:
                raise ValueError(f"Invalid DOF name: {dof}")
        
        # Store constraint indices for this node
        node_index = self.nodes.index(node)
        constrained_indices = [dof_map[dof] for dof in constrained_dofs]
        self.constraints[node_index] = constrained_indices
        
    def get_global_dof_index(self, node_index, local_dof):
        """
        Convert node and local DOF index to global DOF index.
        
        Args:
            node_index: Index of the node
            local_dof: Local DOF index (0-5)
            
        Returns:
            Global DOF index
        """
        return node_index * 6 + local_dof
    
    def get_constrained_dofs(self):
        """
        Get list of all constrained global DOF indices.
        
        Returns:
            List of constrained DOF indices
        """
        constrained_dofs = []
        for node_index, local_dofs in self.constraints.items():
            for local_dof in local_dofs:
                global_dof = self.get_global_dof_index(node_index, local_dof)
                constrained_dofs.append(global_dof)
        return sorted(constrained_dofs)
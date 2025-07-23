class Node:
    """Representa un nodo en una estructura 3D.

    Cada nodo tiene un ID único, coordenadas (x, y, z) y grados de libertad (DOFs).
    """
    _id_counter = 0

    def __init__(self, x, y, z):
        """Inicializa un nuevo nodo.

        Args:
            x (float): Coordenada X del nodo.
            y (float): Coordenada Y del nodo.
            z (float): Coordenada Z del nodo.
        """
        self.id = Node._id_counter
        Node._id_counter += 1
        self.coords = (x, y, z)
        self.dofs = [self.id * 6 + i for i in range(6)]  # 6 GDL por nodo

    def __repr__(self):
        return f"Node {self.id} ({self.coords})"

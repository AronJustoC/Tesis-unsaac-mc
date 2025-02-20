class Node:
    _id_counter = 0

    def __init__(self, x, y, z):
        self.id = Node._id_counter
        Node._id_counter += 1
        self.coords = (x, y, z)
        self.dofs = [self.id * 6 + i for i in range(6)]  # 6 GDL por nodo

    def __repr__(self):
        return f"Node {self.id} ({self.coords})"

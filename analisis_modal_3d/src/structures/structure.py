from .node import Node
from .element import Element


class Structure:
    def __init__(self):
        self.nodes = []
        self.elements = []

    def add_node(self, x, y, z):
        new_node = Node(x, y, z)
        self.nodes.append(new_node)
        return new_node

    def add_element(self, node1, node2, section, material):
        new_element = Element(node1, node2, section, material)
        self.elements.append(new_element)
        return new_element

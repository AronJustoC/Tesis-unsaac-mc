from typing import ClassVar, override


class Node:
    _id_counter: ClassVar[int] = 1

    def __init__(self, x: float, y: float, z: float) -> None:
        self.id: int = Node._id_counter
        Node._id_counter += 1

        self.coords: tuple[float, float, float] = (x, y, z)
        self.dofs: list[int] = [self.id * 6 + i for i in range(6)]

    @override
    def __repr__(self) -> str:
        return f"Node(id={self.id}, coords={self.coords})"

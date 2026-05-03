from .Node import Node


class ColumnNode(Node):
    """Header node for a column in the exact cover matrix. Tracks column size."""

    def __init__(self, row: int, col: int):
        super().__init__(row, col)
        self.size = 1  # number of nodes currently in this column

    def add(self, node: Node) -> None:
        """Append a node to the bottom of this column."""
        node.parent = self
        node.up = self.up
        node.down = self
        self.up.down = node
        self.up = node
        self.size += 1

    def removeRL(self) -> None:
        """Unlink this column header from its horizontal neighbours."""
        self.right.left = self.left
        self.left.right = self.right

    def reinsertRL(self) -> None:
        """Relink this column header back into its horizontal neighbours."""
        self.right.left = self
        self.left.right = self

    def cover(self) -> None:
        """Remove this column and all rows that satisfy it from the matrix."""
        self.removeRL()
        current = self.down
        while current != self:
            row_node = current.right
            while row_node != current:
                row_node.removeUD()
                row_node.parent.size -= 1
                row_node = row_node.right
            current = current.down

    def uncover(self) -> None:
        """Restore this column and all rows removed during cover (runs in reverse)."""
        current = self.up
        while current != self:
            row_node = current.left
            while row_node != current:
                row_node.reinsertUD()
                row_node.parent.size += 1
                row_node = row_node.left
            current = current.up
        self.reinsertRL()

    def __repr__(self) -> str:
        string = ''
        current_node = self.down
        for _ in range(self.size - 1):
            string += str(current_node)
            current_node = current_node.down
        return f'[{self.row}, {self.col}]{string}'

class Node:
    """A single node in the dancing links matrix with four directional pointers."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        # each node starts pointing to itself in all directions
        self.up = self
        self.down = self
        self.right = self
        self.left = self

    def add_right(self, node: 'Node') -> None:
        """Insert a node immediately to the right of this one."""
        node.right = self.right
        node.left = self
        self.right.left = node
        self.right = node

    def removeUD(self) -> None:
        """Unlink this node from its vertical neighbours (cover operation)."""
        self.down.up = self.up
        self.up.down = self.down

    def reinsertUD(self) -> None:
        """Relink this node back into its vertical neighbours (uncover operation)."""
        self.down.up = self
        self.up.down = self

    def __repr__(self) -> str:
        return f'[{self.row}, {self.col}]'

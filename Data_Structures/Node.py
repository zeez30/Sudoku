class Node:
    def __init__(self, row, col):
        # Initialize the node with the given row and column
        self.row = row
        self.col = col
        # Set the node's up, down, right, and left pointers to itself initially
        self.up = self
        self.down = self
        self.right = self
        self.left = self

    def add_right(self, node):
        # Add a node to the right of the current node
        node.right = self.right
        node.left = self
        self.right.left = node
        self.right = node

    def removeUD(self):
        # Remove the current node from the up and down links
        self.down.up = self.up
        self.up.down = self.down

    def reinsertUD(self):
        # Reinsert the current node into the up and down links
        self.down.up = self
        self.up.down = self

    def __repr__(self) -> str:
        # Return a string representation of the node
        return f'[{self.row}, {self.col}]'

if __name__ == '__main__':
    # Create a test node with specific row and column values
    test_node = Node(1, 5)
    # Print the string representation of the test node
    print(f'Test Node: {test_node}')

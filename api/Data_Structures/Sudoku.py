class Sudoku:
    """Holds the Sudoku grid. Parses a flat 81-char string into a 9x9 grid."""

    def __init__(self, puzzle_string: str):
        self.size = int(len(puzzle_string) ** 0.5)
        self.grid = [[0] * self.size for _ in range(self.size)]
        for index, char in enumerate(puzzle_string):
            row = index // self.size
            col = index % self.size
            self.grid[row][col] = int(char) if char != '0' else 0

    def __repr__(self) -> str:
        return ''.join(
            '\n' + str(row) for row in self.grid
        )

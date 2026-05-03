class Sudoku:
    def __init__(self, puzzle_string):
        # Determine the size of the Sudoku grid based on the length of the input string
        self.size = int(len(puzzle_string) ** 0.5)
        # Initialize a 2D list to represent the Sudoku grid, filled with zeros
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # Populate the grid with the given numbers from the input string
        for index, char in enumerate(puzzle_string):
            row = index // self.size
            col = index % self.size
            self.grid[row][col] = int(char) if char != '0' else 0

    def __repr__(self) -> str:
        # Construct a string representation of the Sudoku grid
        grid_representation = ''
        for row in self.grid:
            grid_representation += f'\n{row}'
        return grid_representation


if __name__ == '__main__':
    # Create a Sudoku instance with a specific puzzle string
    puzzle_instance = Sudoku('530070000600195000098000060800060003400803001700020006060000280000419005000080079')
    # Print the string representation of the Sudoku puzzle
    print(f'Test Sudoku: {puzzle_instance}')

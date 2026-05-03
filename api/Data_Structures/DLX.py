from .Node import Node
from .Sudoku import Sudoku
from .Column import ColumnNode


class DLX:
    """
    Solves Sudoku as an exact cover problem using Knuth's Dancing Links algorithm.
    Builds a sparse binary matrix where rows = digit placements,
    columns = the four Sudoku constraints (cell, row, column, box).
    """

    def __init__(self, sudoku_string: str):
        self.solution: list = []
        self.multiple_solutions = None
        self.at_least_one_solution = False
        self.sudoku = Sudoku(sudoku_string)

        self.CELL_COUNT = self.sudoku.size ** 2
        self.CONSTRAINTS = 4
        self.DIGITS = self.ROW_SIZE = self.COL_SIZE = self.sudoku.size
        self.BOX_COL_SIZE = self.BOX_ROW_SIZE = int(self.sudoku.size ** .5)

        # sparse matrix: rows = digit placements, cols = constraints
        self.matrix = [
            [0] * (self.CELL_COUNT * self.CONSTRAINTS)
            for _ in range(self.CELL_COUNT * self.DIGITS)
        ]

        # column headers in a circular linked list; index 0 is the root header
        self.columns = [ColumnNode(-1, i) for i in range(-1, self.CELL_COUNT * self.CONSTRAINTS)]
        for i in range(len(self.columns) - 1):
            self.columns[i].add_right(self.columns[i + 1])
        self.header = self.columns[0]
        self._build_matrix()

    def _build_matrix(self) -> None:
        """Populate constraint columns for every valid digit placement."""
        for index, row in enumerate(self.matrix):
            i = index
            cell_number = int(i // self.DIGITS)
            row_number = int(i // (self.DIGITS * self.ROW_SIZE))
            col_number = cell_number % self.COL_SIZE
            box_number = int(
                row_number - (row_number % self.BOX_COL_SIZE)
                + col_number // self.BOX_ROW_SIZE
            )
            # skip placements that contradict pre-filled cells
            if self.sudoku.grid[row_number][col_number] != 0:
                i = (cell_number * self.DIGITS) + self.sudoku.grid[row_number][col_number] - 1
                if i != index:
                    continue
            self._add_constraints(index, cell_number, row_number, col_number, box_number, row)

    def _add_constraints(self, index, cell_number, row_number, col_number, box_number, row) -> None:
        """Add the four constraint nodes for a single digit placement."""
        OFFSET = 1  # col 0 is root header, real columns start at 1

        # constraint 1: each cell holds exactly one digit
        cell_i = cell_number
        cell_node = Node(index, cell_i)
        row[cell_i] = cell_node
        self.columns[cell_i + OFFSET].add(cell_node)

        # constraint 2: each digit appears once per row
        row_i = ((row_number * self.DIGITS) + (index % self.DIGITS)) + self.CELL_COUNT
        row_node = Node(index, row_i)
        row[row_i] = row_node
        self.columns[row_i + OFFSET].add(row_node)

        # constraint 3: each digit appears once per column
        col_i = (index % (self.ROW_SIZE * self.DIGITS)) + 2 * self.CELL_COUNT
        col_node = Node(index, col_i)
        row[col_i] = col_node
        self.columns[col_i + OFFSET].add(col_node)

        # constraint 4: each digit appears once per 3x3 box
        box_i = ((box_number * self.DIGITS) + (index % self.DIGITS)) + 3 * self.CELL_COUNT
        box_node = Node(index, box_i)
        row[box_i] = box_node
        self.columns[box_i + OFFSET].add(box_node)

        # link the four nodes horizontally within this row
        cell_node.add_right(row_node)
        row_node.add_right(col_node)
        col_node.add_right(box_node)

    def solve(self, depth: int = 0) -> None:
        """Recursively search for a solution using Algorithm X with backtracking."""
        if self.header.right == self.header or depth == self.sudoku.size ** 2:
            self.at_least_one_solution = True
            self.multiple_solutions = False if self.multiple_solutions is None else True
            if self.multiple_solutions:
                return
            self.solved = list(self.solution)
            return

        col = self._find_min_col()
        col.cover()

        current_sol = col.down
        while current_sol != col:
            self.solution.append(current_sol)
            sol_node = current_sol.right
            while sol_node != current_sol:
                sol_node.parent.cover()
                sol_node = sol_node.right

            self.solve(depth + 1)
            if self.multiple_solutions:
                return

            current_sol = self.solution.pop()
            col = current_sol.parent
            sol_node = current_sol.left
            while sol_node != current_sol:
                sol_node.parent.uncover()
                sol_node = sol_node.left
            current_sol = current_sol.down

        col.uncover()

    def _find_min_col(self) -> ColumnNode:
        """Pick the column with the fewest nodes (minimum remaining values heuristic)."""
        min_col = self.header.right
        current = self.header.right.right
        while current != self.header:
            if current.size < min_col.size:
                min_col = current
            current = current.right
        return min_col

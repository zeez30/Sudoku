import matplotlib.pyplot as plt

# Conditional imports to support both script execution and module import
try:
    from Node import Node
    from Sudoku import Sudoku
    from Column import ColumnNode
except ImportError:
    from .Node import Node
    from .Sudoku import Sudoku
    from .Column import ColumnNode

class DLX:
    def __init__(self, sudoku_string):
        self.solution = []
        self.multiple_solutions = None
        self.sudoku = Sudoku(sudoku_string)
        self.CELL_COUNT = self.sudoku.size ** 2
        self.CONSTRAINTS = 4
        self.DIGITS = self.ROW_SIZE = self.COL_SIZE = self.sudoku.size
        self.BOX_COL_SIZE = self.BOX_ROW_SIZE = int(self.sudoku.size ** .5)
        self.matrix = [[0 for _ in range(self.CELL_COUNT * self.CONSTRAINTS)] for _ in range(self.CELL_COUNT * self.DIGITS)]
        self.columns = [ColumnNode(-1, i) for i in range(-1, self.CELL_COUNT * self.CONSTRAINTS)]
        for i in range(len(self.columns) - 1):
            self.columns[i].add_right(self.columns[i + 1])
        self.header = self.columns[0]
        self.initialize_matrix()

    def initialize_matrix(self):
        #initialise the matrix with constraints for each cell, row, colum and box
        for index, row in enumerate(self.matrix):
            i = index
            cell_number = int(i // self.DIGITS)
            row_number = int(i // (self.DIGITS * self.ROW_SIZE))
            col_number = cell_number % self.COL_SIZE
            box_number = int(row_number - (row_number % self.BOX_COL_SIZE) + col_number // self.BOX_ROW_SIZE)

            if self.sudoku.grid[row_number][col_number] != 0:
                i = (cell_number * self.DIGITS) + self.sudoku.grid[row_number][col_number] - 1
                if i != index:
                    continue

            self.add_constraints(index, cell_number, row_number, col_number, box_number, row)

    def add_constraints(self, index, cell_number, row_number, col_number, box_number, row):
        #add constraints for cell,row,colum and box in the maitrix
        cell_i = cell_number
        cell_node = Node(index, cell_i)
        row[cell_i] = cell_node

        ROW_CONSTRAINT_OFFSET = 1 * self.CELL_COUNT
        row_i = ((row_number * self.DIGITS) + (index % self.DIGITS)) + ROW_CONSTRAINT_OFFSET
        row_node = Node(index, row_i)
        row[row_i] = row_node

        COL_CONSTRAINT_OFFSET = 2 * self.CELL_COUNT
        col_i = (index % (self.ROW_SIZE * self.DIGITS)) + COL_CONSTRAINT_OFFSET
        col_node = Node(index, col_i)
        row[col_i] = col_node

        BOX_CONSTRAINT_OFFSET = 3 * self.CELL_COUNT
        box_i = ((box_number * self.DIGITS) + (index % self.DIGITS)) + BOX_CONSTRAINT_OFFSET
        box_node = Node(index, box_i)
        row[box_i] = box_node

        cell_node.add_right(row_node)
        row_node.add_right(col_node)
        col_node.add_right(box_node)

        COLS_INDEX_OFFSET = 1
        self.columns[cell_i + COLS_INDEX_OFFSET].add(cell_node)
        self.columns[row_i + COLS_INDEX_OFFSET].add(row_node)
        self.columns[col_i + COLS_INDEX_OFFSET].add(col_node)
        self.columns[box_i + COLS_INDEX_OFFSET].add(box_node)

    def solve(self, depth=0):
        #solve the sudoku puzzle using the DXL algorithm
        if self.header.right == self.header or depth == self.sudoku.size ** 2:
            self.at_least_one_solution = True
            self.multiple_solutions = False if self.multiple_solutions is None else True
            if self.multiple_solutions:
                return
            self.solved = [n for n in self.solution]
        col = self.find_col()
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

    def find_col(self):
        #Find the colum with the smallest size
        min_col = self.header.right
        current = self.header.right.right
        while current != self.header:
            if current.size < min_col.size:
                min_col = current
            current = current.right
        return min_col

    def __repr__(self) -> str:
        #represents the matrix as a string
        r = ''
        for i in range(len(self.matrix)):
            row = ''
            for j in range(len(self.matrix[0])):
                current = self.matrix[i][j]
                if current != 0:
                    row += str(current)
            r += f'\n{row if row != "" else "empty"}'
        return r

    def print_cols(self):
        #print the columns of the matrix
        start = self.header
        print(start)
        current = start.right
        while current != start:
            print(current)
            current = current.right

if __name__ == '__main__':
    sudoku_string = '530070000600195000098000060800060003400803001700020006060000280000419005000080079'
    test_cover = DLX(sudoku_string)
    print(f'\nTest Sudoku: {test_cover.sudoku}')
    print(f'\nTest Cover Head: {test_cover.header}')
    print(f'\nTest Traversal (right): {test_cover.header.right}')
    print(f'\nTest Traversal (left): {test_cover.header.left}')
    print(f'\nTest Traversal (up): {test_cover.header.up}')
    print(f'\nTest Traversal (down): {test_cover.header.down}')

    test_cover.solve()
    solution = test_cover.solved
    if not test_cover.multiple_solutions:
        for i, node in enumerate(solution):
            matrix_row = node.row
            cell = matrix_row // 9
            sudoku_string = sudoku_string[:cell] + str((matrix_row % 9) + 1) + sudoku_string[cell + 1:]
        print(f'\nTest Solution: {Sudoku(sudoku_string)}')
    else:
        print('\nSudoku is unsolvable due to multiple solutions.')

    x1, y1, x2, y2, x3, y3, x4, y4 = [], [], [], [], [], [], [], []
    for i, _ in enumerate(test_cover.matrix):
        for j, _ in enumerate(test_cover.matrix[0]):
            if test_cover.matrix[i][j] != 0:
                current = test_cover.matrix[i][j]
                if current.col < 81:
                    y1.append(729 - i)
                    x1.append(j)
                elif current.col < 162:
                    y2.append(729 - i)
                    x2.append(j)
                elif current.col < 243:
                    y3.append(729 - i)
                    x3.append(j)
                else:
                    y4.append(729 - i)
                    x4.append(j)
    plt.scatter(x1, y1, marker='.', c='black')
    plt.scatter(x2, y2, marker='.', c='blue')
    plt.scatter(x3, y3, marker='.', c='green')
    plt.scatter(x4, y4, marker='.', c='red')
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('Cover Matrix')
    plt.show()

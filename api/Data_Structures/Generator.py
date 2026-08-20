import random

# cells removed per difficulty — higher = harder. Shared by the web API
# (api/generate.py) and the terminal CLI (main.py) so both agree on what
# "easy"/"intermediate"/"hard" mean.
DIFFICULTY_CELLS = {
    'easy':         30,
    'intermediate': 45,
    'hard':         55,
}


def _is_valid(grid: list[list[int]], num: int, coord: tuple[int, int]) -> bool:
    """Return True if placing num at coord doesn't break any Sudoku rule."""
    r, c = coord
    sq_r, sq_c = r - r % 3, c - c % 3

    if num in grid[r]:
        return False
    if num in [grid[row][c] for row in range(9)]:
        return False
    for i in range(3):
        for j in range(3):
            if grid[sq_r + i][sq_c + j] == num:
                return False
    return True


def build_solved_grid() -> str:
    """Fill an empty 9x9 grid using backtracking with shuffled digit order."""
    state = {'grid': [[0] * 9 for _ in range(9)], 'pos': 0}

    def fill():
        if state['pos'] == 81:
            return True
        r, c = divmod(state['pos'], 9)
        digits = list(range(1, 10))
        random.shuffle(digits)
        for d in digits:
            if _is_valid(state['grid'], d, (r, c)):
                state['grid'][r][c] = d
                state['pos'] += 1
                if fill():
                    return True
                state['grid'][r][c] = 0
                state['pos'] -= 1
        return False

    fill()
    return ''.join(str(n) for row in state['grid'] for n in row)


def remove_cells(solved: str, count: int) -> str:
    """Randomly remove `count` cells from a solved puzzle string."""
    cells = list(range(81))
    random.shuffle(cells)
    puzzle = list(solved)
    for cell in cells[:count]:
        puzzle[cell] = '0'
    return ''.join(puzzle)


def generate_puzzle(difficulty: str = 'easy') -> tuple[str, str]:
    """Generate a (puzzle, solution) pair of 81-char strings for a difficulty."""
    solved = build_solved_grid()
    cells_to_remove = DIFFICULTY_CELLS.get(difficulty, DIFFICULTY_CELLS['easy'])
    puzzle = remove_cells(solved, cells_to_remove)
    return puzzle, solved

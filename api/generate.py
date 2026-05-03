import json
import random
import sys
import os
from http.server import BaseHTTPRequestHandler

# make Data_Structures importable from this directory
sys.path.insert(0, os.path.dirname(__file__))
from Data_Structures.DLX import DLX

# cells removed per difficulty — higher = harder
DIFFICULTY_CELLS = {
    'easy':         30,
    'intermediate': 45,
    'hard':         55,
}


def _is_valid(puzzle: list[list[int]], num: int, coord: tuple[int, int]) -> bool:
    """Return True if placing num at coord doesn't break any Sudoku rule."""
    r, c = coord
    sq_r, sq_c = r - r % 3, c - c % 3

    if num in puzzle[r]:
        return False
    if num in [puzzle[row][c] for row in range(9)]:
        return False
    for i in range(3):
        for j in range(3):
            if puzzle[sq_r + i][sq_c + j] == num:
                return False
    return True


def _build_solved_puzzle() -> str:
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


def _remove_cells(solved: str, count: int) -> str:
    """Randomly remove `count` cells from a solved puzzle string."""
    cells = list(range(81))
    random.shuffle(cells)
    puzzle = list(solved)
    removed = 0
    for cell in cells:
        if removed >= count:
            break
        puzzle[cell] = '0'
        removed += 1
    return ''.join(puzzle)


class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler — generates a puzzle and returns puzzle + solution."""

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        difficulty = body.get('difficulty', 'easy')
        cells_to_remove = DIFFICULTY_CELLS.get(difficulty, DIFFICULTY_CELLS['easy'])

        solved = _build_solved_puzzle()
        puzzle = _remove_cells(solved, cells_to_remove)

        self._respond(200, {'puzzle': puzzle, 'solution': solved})

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self._cors()
        self.end_headers()

    def _respond(self, status: int, data: dict) -> None:
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors(self) -> None:
        """Attach CORS headers so the frontend can call this from any origin."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, *args):
        pass  # suppress default request logging

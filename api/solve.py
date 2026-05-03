import json
import sys
import os
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(__file__))
from Data_Structures.DLX import DLX
from Data_Structures.Sudoku import Sudoku


def _solve(puzzle_string: str) -> str | None:
    """Run DLX on the puzzle. Returns solution string or None if unsolvable."""
    dlx = DLX(puzzle_string)
    dlx.solve()

    if not dlx.at_least_one_solution or dlx.multiple_solutions:
        return None

    result = list(puzzle_string)
    for node in dlx.solved:
        cell = node.row // 9
        digit = (node.row % 9) + 1
        result[cell] = str(digit)
    return ''.join(result)


class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler — solves a given puzzle string."""

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        puzzle = body.get('puzzle', '')

        if len(puzzle) != 81:
            self._respond(400, {'error': 'Invalid puzzle string'})
            return

        solution = _solve(puzzle)
        if solution:
            self._respond(200, {'solution': solution})
        else:
            self._respond(422, {'error': 'No unique solution found'})

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self._cors()
        self.end_headers()

    def _respond(self, status: int, data: dict) -> None:
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors(self) -> None:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, *args):
        pass

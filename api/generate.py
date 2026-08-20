import json
import sys
import os
from http.server import BaseHTTPRequestHandler

# make Data_Structures importable from this directory
sys.path.insert(0, os.path.dirname(__file__))
from Data_Structures.Generator import generate_puzzle


class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler — generates a puzzle and returns puzzle + solution."""

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        difficulty = body.get('difficulty', 'easy')

        puzzle, solved = generate_puzzle(difficulty)

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

# Sudoku

A Sudoku web app built with React/TypeScript and a Python backend that generates and solves
puzzles using [Dancing Links / Algorithm X](https://en.wikipedia.org/wiki/Dancing_Links)
(Knuth's exact-cover algorithm). A terminal CLI version is also included.

## Project structure

```
src/                  React + TypeScript frontend (Vite, Tailwind)
  hooks/useGame.ts      game state, timer, mistakes, fetches puzzles from the API
  components/           Board, NumPad, Controls, GameOver, HowToPlay
api/                  Vercel serverless functions (Python)
  generate.py            POST /api/generate — generates a new puzzle for a difficulty
  solve.py               POST /api/solve — solves a given 81-char puzzle string
  Data_Structures/       DLX/Algorithm X implementation shared by generate.py, solve.py,
                          and the root-level main.py CLI
main.py               Standalone terminal CLI version of the game
```

## Running the web app

```bash
npm install
npm run dev
```

The `/api/*` routes are Vercel Python functions, which plain `vite dev` doesn't execute.
To run them locally, use the [Vercel CLI](https://vercel.com/docs/cli) instead:

```bash
vercel dev
```

## Running the CLI version

```bash
python main.py
```

Pick a difficulty, then enter moves as `r3c2 4` (row 3, column 2, place a 4).

## Deployment

Deployed on Vercel. `vercel.json` rewrites `/api/*` to the Python functions in `api/`.

## Tech stack

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS
- **Backend:** Python (Vercel serverless functions), Dancing Links / Algorithm X for
  puzzle generation and uniqueness-checked solving

import { useState, useCallback, useEffect, useRef } from 'react';
import type { Cell, GameStatus, Difficulty } from '../types';
import { MAX_MISTAKES } from '../types';

/** Convert a flat 81-char string into a 9x9 Cell grid */
function buildGrid(puzzle: string, _solution: string): Cell[][] {
  return Array.from({ length: 9 }, (_, r) =>
    Array.from({ length: 9 }, (_, c) => {
      const i = r * 9 + c;
      const val = parseInt(puzzle[i]);
      return {
        value: val,
        isGiven: val !== 0,
        isError: false,
        notes: [],
      };
    })
  );
}

export function useGame() {
  const [grid, setGrid]               = useState<Cell[][]>([]);
  const [solution, setSolution]       = useState<string>('');
  const [selected, setSelected]       = useState<[number, number] | null>(null);
  const [mistakes, setMistakes]       = useState(0);
  const [status, setStatus]           = useState<GameStatus>('idle');
  const [difficulty, setDifficulty]   = useState<Difficulty>('easy');
  const [loading, setLoading]         = useState(false);
  const [seconds, setSeconds]         = useState(0);
  const [noteMode, setNoteMode]       = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  /** Start/stop the timer based on game status */
  useEffect(() => {
    if (status === 'playing') {
      timerRef.current = setInterval(() => setSeconds(s => s + 1), 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [status]);

  /** Fetch a new puzzle from the generate API */
  const newGame = useCallback(async (diff?: Difficulty) => {
    const d = diff ?? difficulty;
    setLoading(true);
    setSelected(null);
    setMistakes(0);
    setSeconds(0);
    setStatus('idle');

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ difficulty: d }),
      });
      const data = await res.json();
      setGrid(buildGrid(data.puzzle, data.solution));
      setSolution(data.solution);
      setStatus('playing');
    } catch {
      console.error('Failed to fetch puzzle');
    } finally {
      setLoading(false);
    }
  }, [difficulty]);

  /** Place a digit in the selected cell and check for errors */
  const placeDigit = useCallback((digit: number) => {
    if (!selected || status !== 'playing') return;
    const [r, c] = selected;
    const cell = grid[r][c];
    if (cell.isGiven) return;

    if (noteMode && digit !== 0) {
      // toggle pencil mark
      setGrid(prev => {
        const next = prev.map(row => row.map(cell => ({ ...cell })));
        const notes = next[r][c].notes;
        next[r][c].notes = notes.includes(digit)
          ? notes.filter(n => n !== digit)
          : [...notes, digit].sort();
        next[r][c].value = 0;
        return next;
      });
      return;
    }

    const correct = parseInt(solution[r * 9 + c]);
    const isError = digit !== 0 && digit !== correct;

    setGrid(prev => {
      const next = prev.map(row => row.map(cell => ({ ...cell })));
      next[r][c].value = digit;
      next[r][c].isError = isError;
      next[r][c].notes = [];
      return next;
    });

    if (isError) {
      const newMistakes = mistakes + 1;
      setMistakes(newMistakes);
      if (newMistakes >= MAX_MISTAKES) setStatus('lost');
    } else if (digit !== 0) {
      // check if puzzle is complete
      const flat = grid.map((row, ri) =>
        row.map((cell, ci) => (ri === r && ci === c ? digit : cell.value))
      ).flat();
      if (flat.every((v, i) => v === parseInt(solution[i]))) {
        setStatus('won');
      }
    }
  }, [selected, grid, solution, mistakes, status, noteMode]);

  /** Reveal the correct value for the selected cell (hint) */
  const useHint = useCallback(() => {
    if (!selected || status !== 'playing') return;
    const [r, c] = selected;
    if (grid[r][c].isGiven) return;
    const correct = parseInt(solution[r * 9 + c]);
    setGrid(prev => {
      const next = prev.map(row => row.map(cell => ({ ...cell })));
      next[r][c].value = correct;
      next[r][c].isError = false;
      next[r][c].notes = [];
      next[r][c].isGiven = true; // treat hint cells as locked
      return next;
    });
  }, [selected, grid, solution, status]);

  return {
    grid, selected, setSelected,
    mistakes, status, difficulty, setDifficulty,
    loading, seconds, noteMode, setNoteMode,
    newGame, placeDigit, useHint,
  };
}

import { useEffect } from 'react';
import { useGame } from './hooks/useGame';
import Board from './components/Board';
import NumPad from './components/NumPad';
import Controls from './components/Controls';
import GameOver from './components/GameOver';

export default function App() {
  const {
    grid, selected, setSelected,
    mistakes, status, difficulty, setDifficulty,
    loading, seconds, noteMode, setNoteMode,
    newGame, placeDigit, useHint,
  } = useGame();

  // handle keyboard digit input
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const n = parseInt(e.key);
      if (n >= 1 && n <= 9) placeDigit(n);
      if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') placeDigit(0);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [placeDigit]);

  return (
    <div className="min-h-screen bg-bg flex flex-col items-center justify-center px-4 py-6 sm:py-8 gap-4 sm:gap-5">

      {/* title */}
      <h1 className="font-mono font-bold text-3xl text-primary">Sudoku</h1>

      {/* controls bar */}
      <Controls
        seconds={seconds}
        mistakes={mistakes}
        difficulty={difficulty}
        onDifficulty={d => { setDifficulty(d); newGame(d); }}
        onNewGame={() => newGame()}
        loading={loading}
      />

      {/* board + overlay wrapper */}
      <div className="relative">
        {loading ? (
          <div className="flex items-center justify-center rounded-lg bg-surface border border-line"
               style={{ width: 'min(94vw, 450px)', height: 'min(94vw, 450px)' }}>
            <span className="font-mono text-sm text-accent">Generating puzzle...</span>
          </div>
        ) : (
          <Board grid={grid} selected={selected} onSelect={(r, c) => setSelected([r, c])} />
        )}
        <GameOver status={status} seconds={seconds} difficulty={difficulty} onNewGame={() => newGame()} />
      </div>

      {/* number pad */}
      <NumPad
        onDigit={placeDigit}
        noteMode={noteMode}
        onToggleNotes={() => setNoteMode(n => !n)}
        onHint={useHint}
      />

      {/* start prompt if idle */}
      {status === 'idle' && !loading && (
        <button
          onClick={() => newGame()}
          className="font-mono text-sm px-6 py-3 rounded
            bg-line text-primary border border-line
            hover:bg-accent hover:border-accent
            active:scale-95 transition-all"
        >
          Start game
        </button>
      )}
    </div>
  );
}

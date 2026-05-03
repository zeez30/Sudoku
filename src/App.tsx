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
    <div className="min-h-screen bg-[#101913] flex flex-col items-center justify-center px-4 py-8 gap-5">

      {/* title */}
      <div className="text-center">
        <h1 className="font-display font-bold text-3xl text-gradient">Sudoku</h1>
        <p className="font-mono text-xs text-[#b2f5fa] mt-1">Dancing Links · Algorithm X</p>
      </div>

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
          <div className="flex items-center justify-center rounded-lg bg-[#140e1b] border border-[#344b07]"
               style={{ width: 'min(90vw, 450px)', height: 'min(90vw, 450px)' }}>
            <span className="font-mono text-sm text-[#b05f1c]">Generating puzzle...</span>
          </div>
        ) : (
          <Board grid={grid} selected={selected} onSelect={(r, c) => setSelected([r, c])} />
        )}
        <GameOver status={status} seconds={seconds} onNewGame={() => newGame()} />
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
            bg-[#344b07] text-[#edf7b5] border border-[#344b07]
            hover:bg-[#b05f1c] hover:border-[#b05f1c]
            active:scale-95 transition-all"
        >
          Start game
        </button>
      )}
    </div>
  );
}

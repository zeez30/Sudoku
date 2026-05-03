import type { GameStatus } from '../types';

interface Props {
  status: GameStatus;
  seconds: number;
  onNewGame: () => void;
}

function fmt(s: number): string {
  const m = Math.floor(s / 60).toString().padStart(2, '0');
  const sec = (s % 60).toString().padStart(2, '0');
  return `${m}:${sec}`;
}

export default function GameOver({ status, seconds, onNewGame }: Props) {
  if (status !== 'won' && status !== 'lost') return null;

  const won = status === 'won';

  return (
    /* full-screen overlay */
    <div className="absolute inset-0 flex items-center justify-center
      bg-[#101913]/90 backdrop-blur-sm z-10 rounded-lg">
      <div className="text-center flex flex-col items-center gap-4 p-8
        bg-[#140e1b] border border-[#344b07] rounded-xl">

        <h2 className="font-display font-bold text-2xl"
            style={{ color: won ? '#edf7b5' : '#aa2422' }}>
          {won ? 'Puzzle solved' : 'Game over'}
        </h2>

        {won && (
          <p className="font-mono text-sm text-[#b05f1c]">
            Completed in {fmt(seconds)}
          </p>
        )}

        {!won && (
          <p className="font-mono text-sm text-[#b2f5fa]">
            Too many mistakes
          </p>
        )}

        <button
          onClick={onNewGame}
          className="mt-2 px-6 py-2 rounded bg-[#344b07] text-[#edf7b5]
            font-mono text-sm border border-[#344b07]
            hover:bg-[#b05f1c] hover:border-[#b05f1c]
            active:scale-95 transition-all duration-100"
        >
          Play again
        </button>
      </div>
    </div>
  );
}

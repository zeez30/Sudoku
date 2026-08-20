import type { GameStatus, Difficulty } from '../types';

interface Props {
  status: GameStatus;
  seconds: number;
  difficulty: Difficulty;
  onNewGame: () => void;
}

function fmt(s: number): string {
  const m = Math.floor(s / 60).toString().padStart(2, '0');
  const sec = (s % 60).toString().padStart(2, '0');
  return `${m}:${sec}`;
}

export default function GameOver({ status, seconds, difficulty, onNewGame }: Props) {
  if (status !== 'won' && status !== 'lost') return null;

  const won = status === 'won';
  const showTime = difficulty !== 'easy';

  return (
    /* full-screen overlay */
    <div className="absolute inset-0 flex items-center justify-center
      bg-bg/90 backdrop-blur-sm z-10 rounded-lg p-4">
      <div className="text-center flex flex-col items-center gap-4 p-8
        bg-surface border border-line rounded-xl">

        <h2 className={`font-display font-bold text-2xl ${won ? 'text-primary' : 'text-danger'}`}>
          {won ? 'Puzzle solved' : 'Game over'}
        </h2>

        {won && (
          <p className="font-mono text-sm text-accent">
            {showTime ? `Completed in ${fmt(seconds)}` : 'Nice work!'}
          </p>
        )}

        {!won && (
          <p className="font-mono text-sm text-secondary">
            Too many mistakes
          </p>
        )}

        <button
          onClick={onNewGame}
          className="mt-2 px-6 py-3 rounded bg-line text-primary
            font-mono text-sm border border-line
            hover:bg-accent hover:border-accent
            active:scale-95 transition-all duration-100"
        >
          Play again
        </button>
      </div>
    </div>
  );
}

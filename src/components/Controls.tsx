import type { Difficulty } from '../types';
import { DIFFICULTIES, MAX_MISTAKES } from '../types';
import HowToPlay from './HowToPlay';

interface Props {
  seconds: number;
  mistakes: number;
  difficulty: Difficulty;
  onDifficulty: (d: Difficulty) => void;
  onNewGame: () => void;
  loading: boolean;
}

/** Format seconds as mm:ss */
function fmt(s: number): string {
  const m = Math.floor(s / 60).toString().padStart(2, '0');
  const sec = (s % 60).toString().padStart(2, '0');
  return `${m}:${sec}`;
}

export default function Controls({
  seconds, mistakes, difficulty, onDifficulty, onNewGame, loading,
}: Props) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-y-2 gap-x-3 w-full"
         style={{ maxWidth: 'min(94vw, 450px)' }}>

      <div className="flex items-center gap-3">
        {/* timer — easy mode is untimed by design */}
        {difficulty === 'easy' ? (
          <span className="font-mono text-sm text-secondary/60">No timer</span>
        ) : (
          <span className="font-mono text-sm text-primary">{fmt(seconds)}</span>
        )}

        {/* mistake pips */}
        <div className="flex items-center gap-1">
          {Array.from({ length: MAX_MISTAKES }).map((_, i) => (
            <div key={i} className={`w-2 h-2 rounded-full border border-danger
              ${i < mistakes ? 'bg-danger' : 'bg-transparent'}`}
            />
          ))}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <HowToPlay />

        {/* difficulty selector */}
        <select
          value={difficulty}
          onChange={e => onDifficulty(e.target.value as Difficulty)}
          className="bg-surface border border-line text-primary
            font-mono text-xs px-2 py-2 rounded outline-none cursor-pointer"
        >
          {DIFFICULTIES.map(d => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>

        {/* new game */}
        <button
          onClick={onNewGame}
          disabled={loading}
          className="font-mono text-xs px-3 py-2 rounded
            bg-line text-primary border border-line
            hover:bg-accent hover:border-accent
            disabled:opacity-50 active:scale-95 transition-all duration-100"
        >
          {loading ? '...' : 'New game'}
        </button>
      </div>
    </div>
  );
}

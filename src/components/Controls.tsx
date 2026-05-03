import type { Difficulty } from '../types';
import { DIFFICULTIES, MAX_MISTAKES } from '../types';

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
    <div className="flex items-center justify-between w-full"
         style={{ maxWidth: 'min(90vw, 450px)' }}>

      {/* timer */}
      <span className="font-mono text-sm text-[#edf7b5]">{fmt(seconds)}</span>

      {/* mistake pips */}
      <div className="flex items-center gap-1">
        {Array.from({ length: MAX_MISTAKES }).map((_, i) => (
          <div key={i} className={`w-2 h-2 rounded-full border border-[#aa2422]
            ${i < mistakes ? 'bg-[#aa2422]' : 'bg-transparent'}`}
          />
        ))}
      </div>

      {/* difficulty selector */}
      <select
        value={difficulty}
        onChange={e => onDifficulty(e.target.value as Difficulty)}
        className="bg-[#140e1b] border border-[#344b07] text-[#edf7b5]
          font-mono text-xs px-2 py-1 rounded outline-none cursor-pointer"
      >
        {DIFFICULTIES.map(d => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>

      {/* new game */}
      <button
        onClick={onNewGame}
        disabled={loading}
        className="font-mono text-xs px-3 py-1 rounded
          bg-[#344b07] text-[#edf7b5] border border-[#344b07]
          hover:bg-[#b05f1c] hover:border-[#b05f1c]
          disabled:opacity-50 active:scale-95 transition-all duration-100"
      >
        {loading ? '...' : 'New game'}
      </button>
    </div>
  );
}

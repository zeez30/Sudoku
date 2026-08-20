interface Props {
  onDigit: (n: number) => void;
  noteMode: boolean;
  onToggleNotes: () => void;
  onHint: () => void;
}

export default function NumPad({ onDigit, noteMode, onToggleNotes, onHint }: Props) {
  return (
    <div className="flex flex-col gap-3 w-full" style={{ maxWidth: 'min(94vw, 450px)' }}>
      {/* digit buttons 1–9 — 5 columns on narrow phones so buttons stay tap-sized, single row once there's room */}
      <div className="grid grid-cols-5 sm:grid-cols-9 gap-1.5">
        {[1,2,3,4,5,6,7,8,9].map(n => (
          <button
            key={n}
            onClick={() => onDigit(n)}
            className="aspect-square flex items-center justify-center rounded
              bg-surface border border-line text-primary
              font-mono font-bold text-base touch-manipulation
              hover:bg-line
              active:scale-95 transition-all duration-100"
          >
            {n}
          </button>
        ))}
      </div>

      {/* action buttons */}
      <div className="grid grid-cols-3 gap-2">
        <button
          onClick={() => onDigit(0)}
          className="py-3 rounded bg-surface border border-hairline
            text-secondary font-mono text-xs touch-manipulation
            hover:border-danger hover:text-danger
            active:scale-95 transition-all duration-100"
        >
          Erase
        </button>

        <button
          onClick={onToggleNotes}
          className={`py-3 rounded border font-mono text-xs touch-manipulation
            active:scale-95 transition-all duration-100
            ${noteMode
              ? 'bg-line border-line text-primary'
              : 'bg-surface border-hairline text-secondary hover:border-line'
            }`}
        >
          Notes
        </button>

        <button
          onClick={onHint}
          className="py-3 rounded bg-surface border border-hairline
            text-secondary font-mono text-xs touch-manipulation
            hover:border-accent hover:text-accent
            active:scale-95 transition-all duration-100"
        >
          Hint
        </button>
      </div>
    </div>
  );
}

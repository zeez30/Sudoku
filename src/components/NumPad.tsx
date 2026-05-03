interface Props {
  onDigit: (n: number) => void;
  noteMode: boolean;
  onToggleNotes: () => void;
  onHint: () => void;
}

export default function NumPad({ onDigit, noteMode, onToggleNotes, onHint }: Props) {
  return (
    <div className="flex flex-col gap-3 w-full" style={{ maxWidth: 'min(90vw, 450px)' }}>
      {/* digit buttons 1–9 */}
      <div className="grid grid-cols-9 gap-1">
        {[1,2,3,4,5,6,7,8,9].map(n => (
          <button
            key={n}
            onClick={() => onDigit(n)}
            className="aspect-square flex items-center justify-center rounded
              bg-[#140e1b] border border-[#344b07] text-[#edf7b5]
              font-mono font-bold text-sm
              hover:bg-[#344b07] hover:text-[#edf7b5]
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
          className="py-2 rounded bg-[#140e1b] border border-[#271b36]
            text-[#b2f5fa] font-mono text-xs
            hover:border-[#aa2422] hover:text-[#aa2422]
            active:scale-95 transition-all duration-100"
        >
          Erase
        </button>

        <button
          onClick={onToggleNotes}
          className={`py-2 rounded border font-mono text-xs
            active:scale-95 transition-all duration-100
            ${noteMode
              ? 'bg-[#344b07] border-[#344b07] text-[#edf7b5]'
              : 'bg-[#140e1b] border-[#271b36] text-[#b2f5fa] hover:border-[#344b07]'
            }`}
        >
          Notes
        </button>

        <button
          onClick={onHint}
          className="py-2 rounded bg-[#140e1b] border border-[#271b36]
            text-[#b2f5fa] font-mono text-xs
            hover:border-[#b05f1c] hover:text-[#b05f1c]
            active:scale-95 transition-all duration-100"
        >
          Hint
        </button>
      </div>
    </div>
  );
}

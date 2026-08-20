import { useState } from 'react';

export default function HowToPlay() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="How to play"
        className="w-8 h-8 flex items-center justify-center rounded-full shrink-0
          border border-hairline text-secondary font-mono text-sm
          hover:border-line hover:text-primary active:scale-95 transition-all"
      >
        ?
      </button>

      {open && (
        <div
          className="fixed inset-0 z-20 flex items-center justify-center
            bg-bg/90 backdrop-blur-sm p-4"
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-sm bg-surface border border-line rounded-xl p-6
              flex flex-col gap-4"
            onClick={e => e.stopPropagation()}
          >
            <h2 className="font-display font-bold text-xl text-primary">How to play</h2>

            <ul className="flex flex-col gap-2.5 font-mono text-sm text-secondary list-none">
              <li>Select a cell, then tap a number (or press 1–9 on a keyboard) to fill it in.</li>
              <li>Every row, column, and 3×3 box must contain the digits 1–9 exactly once.</li>
              <li><span className="text-primary">Notes</span> pencils in candidate numbers instead of filling the cell.</li>
              <li><span className="text-primary">Hint</span> reveals the correct number for the selected cell.</li>
              <li>3 mistakes ends the game. Easy mode has no timer.</li>
            </ul>

            <button
              onClick={() => setOpen(false)}
              className="mt-2 px-6 py-3 rounded bg-line text-primary font-mono text-sm
                border border-line hover:bg-accent hover:border-accent
                active:scale-95 transition-all"
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </>
  );
}

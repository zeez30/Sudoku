import type { Cell } from '../types';

interface Props {
  grid: Cell[][];
  selected: [number, number] | null;
  onSelect: (r: number, c: number) => void;
}

/** Returns true if cell [r,c] is in the same row, col, or 3x3 box as selected */
function isRelated(r: number, c: number, sel: [number, number]): boolean {
  const [sr, sc] = sel;
  return r === sr || c === sc ||
    (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3));
}

export default function Board({ grid, selected, onSelect }: Props) {
  if (!grid.length) return null;

  return (
    <div className="grid grid-cols-9 border-2 border-line rounded-lg overflow-hidden"
         style={{ width: 'min(94vw, 450px)', height: 'min(94vw, 450px)' }}>
      {grid.map((row, r) =>
        row.map((cell, c) => {
          const isSelected   = selected?.[0] === r && selected?.[1] === c;
          const isHighlighted = selected ? isRelated(r, c, selected) : false;
          const sameValue    = selected && cell.value !== 0 &&
                               cell.value === grid[selected[0]][selected[1]].value;

          // right/bottom borders for 3x3 box separation
          const boxRight  = (c + 1) % 3 === 0 && c !== 8;
          const boxBottom = (r + 1) % 3 === 0 && r !== 8;

          let bg = 'bg-bg';
          if (isSelected)         bg = 'bg-line';
          else if (sameValue)     bg = 'bg-line/40';
          else if (isHighlighted) bg = 'bg-surface';

          return (
            <div
              key={`${r}-${c}`}
              onClick={() => onSelect(r, c)}
              className={`
                ${bg} flex items-center justify-center cursor-pointer
                border-[0.5px] border-hairline relative select-none touch-manipulation
                transition-colors duration-100
                ${boxRight  ? 'border-r-2 border-r-line' : ''}
                ${boxBottom ? 'border-b-2 border-b-line' : ''}
              `}
            >
              {cell.value !== 0 ? (
                <span className={`
                  font-mono text-base font-bold leading-none
                  ${cell.isError   ? 'text-danger' :
                    cell.isGiven   ? 'text-primary' :
                                     'text-accent'}
                `}>
                  {cell.value}
                </span>
              ) : cell.notes.length > 0 ? (
                /* pencil marks — 3x3 mini grid */
                <div className="grid grid-cols-3 w-full h-full p-[1px]">
                  {[1,2,3,4,5,6,7,8,9].map(n => (
                    <span key={n} className="flex items-center justify-center
                      text-[6px] font-mono text-accent leading-none">
                      {cell.notes.includes(n) ? n : ''}
                    </span>
                  ))}
                </div>
              ) : null}
            </div>
          );
        })
      )}
    </div>
  );
}

/** Represents a single cell in the Sudoku grid */
export interface Cell {
  value: number;       // 0 = empty
  isGiven: boolean;    // true = part of the original puzzle, not editable
  isError: boolean;    // true = user input conflicts with solution
  notes: number[];     // pencil-mark candidates
}

/** Overall game status */
export type GameStatus = 'idle' | 'playing' | 'won' | 'lost';

export type Difficulty = 'easy' | 'intermediate' | 'hard';

export const MAX_MISTAKES = 3;

export const DIFFICULTIES: Difficulty[] = ['easy', 'intermediate', 'hard'];

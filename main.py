import re
import sys
import os

# the canonical DLX/Sudoku data structures live under api/, shared with the
# Vercel serverless functions rather than duplicated here
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api'))
from Data_Structures.Generator import generate_puzzle, DIFFICULTY_CELLS


# function to print a nice looking sudoku puzzle
def print_sudoku(sudoku_str):
    sudoku = [[s for s in sudoku_str[n:n + 9]] for n in range(0, 81, 9)]
    row_strings = []
    for row in sudoku:
        # each row will start with a pipe
        row_string = '|'

        for i, num in enumerate(row):
            # the pipe for col 9 comes later
            if i == 8:
                row_string += num
            # each col that isn't 3, 6, 9 will be followed by a space
            elif (i + 1) % 3 != 0:
                row_string += num + ' '
            # col 3 and 6 are followed by a pipe
            else:
                row_string += num + '|'

        row_strings.append(row_string.replace('0', ' '))

    divider = ' ' + '_' * len(row_strings[0])

    # top line
    print(divider)

    # rows are printed with a pipe on the end, divider line after every 3rd row
    for i, row_string in enumerate(row_strings):
        print(f'{row_string}|')
        if not (i + 1) % 3:
            print(divider)


# Function to start the application
def play():
    difficulty = input('Choose difficulty level (easy, intermediate, hard): ').lower()
    if difficulty not in DIFFICULTY_CELLS:
        print("Invalid difficulty level. Defaulting to 'easy'.")
        difficulty = 'easy'

    new_sudoku, new_sudoku_solved = generate_puzzle(difficulty)
    playing = True

    while playing:
        print_sudoku(new_sudoku)
        print("Can you solve this? Enter your answer in the format 'r3c2 4' or 'quit' to exit.")

        # Using sys.stdin.readline() for faster input
        arg = sys.stdin.readline().strip()

        # Check if the user wants to quit
        if arg.lower() == 'quit':
            playing = False
            continue

        # Parsing the input, e.g. 'r3c2 4' -> row 3, col 2, digit 4
        try:
            cell_ref, num = arg.split()
            match = re.fullmatch(r'r([1-9])c([1-9])', cell_ref)
            if not match:
                raise ValueError
            row, col = int(match.group(1)), int(match.group(2))
            num = int(num)
        except ValueError:
            print("Invalid input. Please try again.")
            continue

        cell = (row - 1) * 9 + col - 1
        cell_num = int(new_sudoku_solved[cell:cell + 1])

        if cell_num == num:
            new_sudoku = new_sudoku[0:cell] + str(cell_num) + new_sudoku[cell + 1:]

            if new_sudoku.find('0') == -1:
                print('Congrats, you finished the puzzle!')
                print_sudoku(new_sudoku)
                keep_playing = input('Keep playing? Y/N: ')

                if keep_playing.upper() == 'Y':
                    print('Generating puzzle...')
                    play()
                else:
                    playing = False
                    continue

            print('Yayy, keep going!')
        else:
            print('Oops, That wasn\'t right!')

    print('Thanks for playing!')
    sys.exit()


# start the sudoku game
if __name__ == '__main__':
    print('Generating puzzle...')
    play()
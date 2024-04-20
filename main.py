import random
import copy
import sys
from Data_Structures.DLX import DLX

#define difficulty levels for the sudoku game
DIFFICULTY_LEVELS = {
    'easy': 10,
    'intermediate': 20,
    'hard': 30,

}
# helper function to check if a string can be converted to integer
def valid_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# function to check if a number is valid in a sudoku puzzle based on the rules
def check_valid_num(puzzle, num, coord):
    #Calculate the starting points for the 3x3 square the number would belong to
    square_y = coord[0] - (coord[0] % 3)
    square_x = coord[1] - (coord[1] % 3)

    # check if number already exists in row
    if puzzle[coord[0]].count(num) != 0:
        return False
    # check if number already exits in column
    if [row[coord[1]] for row in puzzle].count(num) != 0:
        return False
    # check if number exits in the 3x3 square
    for i in range(3):
        for j in range(3):
            if puzzle[square_y + i][square_x + j] == num:
                return False

    return True


# Uses the DLX algorithm to check if a sudoku puzzle is solvable
def check_sudoku(puzzle_str):
    cover = DLX(puzzle_str)
    cover.solve()
    return cover.at_least_one_solution and not cover.multiple_solutions


# function to create a filled puzzle
def generate_puzzle():
    # initalizes empty puzzle with a tile counter set to 0
    new_puzzle = {
        'puzzle': [[0 for i in range(9)] for j in range(9)],
        'current_space': 0
    }

    # recursive function to build upon above puzzle
    def build_sudoku():
        space = new_puzzle['current_space']
        # the counter being at 81 indicates that the puzzle is full
        if space == 81:
            return
        # creates coordinates of current tile from counter
        coord = [int(space // 9), space % 9]

        # shuffled list of nums 1-9
        num_list = list(range(1, 10))
        random.shuffle(num_list)

        # tries nums 1-9 in random order at current tile
        for num in num_list:
            if new_puzzle['current_space'] == 81:
                return
            if check_valid_num(new_puzzle['puzzle'], num, coord):
                new_puzzle['puzzle'][coord[0]][coord[1]] = num
                new_puzzle['current_space'] += 1
                build_sudoku()

        # when the puzzle is full there is no need for resets as the function unwinds
        if new_puzzle['current_space'] == 81:
            return

        # sets current tile back to 0 and rewinds counter before backtracking
        new_puzzle['puzzle'][coord[0]][coord[1]] = 0
        new_puzzle['current_space'] -= 1
        return

    build_sudoku()
    return ''.join([''.join([str(n) for n in m]) for m in new_puzzle['puzzle']])

#Function to generate a sudoku puzzle with a specified difficulty level
def generate_sudoku(difficulty='easy'):
    # Generate a fully solved puzzle
    solved_puzzle = generate_puzzle()
    puzzle = list(solved_puzzle)

    # Determine the number of tiles to remove based on the difficulty level
    tiles_to_remove = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS['easy'])

    # Create a list to keep track of removed tiles
    removed_tiles = []

    # Remove tiles until the desired number is reached
    while len(removed_tiles) < tiles_to_remove:
        cell = random.randint(0, 80)
        if puzzle[cell] == '0': # Ensure we're not removing a tile that's already removed
            continue
        removed_tiles.append(cell)
        puzzle[cell] = '0'

    # Convert the list back to a string for consistency with the rest of your code
    puzzle = ''.join(puzzle)

    return puzzle, solved_puzzle



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

    # top line
    print(' _________________')

    # rows are printed with a pipe on the end
    for i, row_string in enumerate(row_strings):
        # rows 3, 6 and 9 are underlined
        if not (i + 1) % 3:
            print("\u0332".join(row_string) + '|')
        else:
            print(f'{row_string}|')


# Function to start the application
def play():
    difficulty = input('Choose difficulty level (easy, intermediate, hard): ').lower()
    if difficulty not in DIFFICULTY_LEVELS:
        print("Invalid difficulty level. Defaulting to 'easy'.")
        difficulty = 'easy'

    new_sudoku, new_sudoku_solved = generate_sudoku(difficulty)
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

        # Parsing the input
        try:
            row, col, num = arg.split()
            row = int(row[1:])
            col = int(col[1:])
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
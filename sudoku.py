import pprint
import collections

columns = collections.defaultdict(set)
rows = collections.defaultdict(set)
boxes = collections.defaultdict(set)
empty = collections.deque()

board = [
        [8, 7, 3, 4, 1, 0, 9, 0, 0],
        [0, 6, 5, 0, 2, 8, 0, 7, 0],
        [0, 2, 0, 7, 0, 3, 0, 0, 0],
        [5, 4, 0, 0, 0, 0, 2, 1, 0],
        [2, 0, 8, 0, 0, 7, 4, 9, 0],
        [6, 9, 0, 0, 8, 0, 0, 0, 0],
        [4, 8, 0, 0, 0, 0, 5, 0, 0],
        [7, 0, 0, 0, 3, 1, 6, 0, 9],
        [0, 1, 0, 0, 0, 9, 8, 0, 7]
]


def prepBoard(board):
    """
    adds each position to corresponding dictionary set
    Inputs:
    in: board: 2d list
    return: None => adds values already in each box to corresponding dictionary sets
    """
    for i in range(0, 9):
        for k in range(0, 9):
            if board[i][k] == 0:
                empty.append([i, k])
            else:
                columns[k].add(board[i][k])
                rows[i].add(board[i][k])
                boxes[(i//3, k//3)].add(board[i][k])


def makeBoard():
    for i in range(len(board)):
        if i % 3 == 0:
            print("------------------------")
        for k in range(len(board[0])):
            if k % 3 == 0:
                print("| ", end="")
            print(str(board[i][k]) + " ", end="")
        print("|", end="\n")
    print("------------------------")


def solve(empty, index):
    """
    solves sudoku using backtracking
    in: empty => List[List[]] deque of all unfilled boxes where each item in list is a sublist of row and column of unfilled box
    return: boolean value
    """
    # base case
    if index >= len(empty):
        return True
    r, c = empty[index]

    # recursive case
    for i in range(1, 10):
        board[r][c] = i
        if isValid(r, c):
            columns[c].add(board[r][c])
            rows[r].add(board[r][c])
            boxes[(r//3, c//3)].add(board[r][c])
            if solve(empty, index + 1):
                return True
            columns[c].remove(board[r][c])
            rows[r].remove(board[r][c])
            boxes[(r//3, c//3)].remove(board[r][c])

    return False


def isValid(i, k):
    """
    checks to see if the value at a particular spot in the board violates the principles of sudoku
    in: i, k => integers that correspond to a row and column of the 2d board
    return: boolean value stating whether the value violates the sudoku principles or not
    """
    if (board[i][k] in rows[i] or
        board[i][k] in columns[k] or
            board[i][k] in boxes[(i//3, k//3)]):
        return False
    return True


makeBoard()
prepBoard(board)
solve(empty, 0)
makeBoard()

import collections


class Sudoku():

    def __init__(self):
        self.columns = collections.defaultdict(set)
        self.rows = collections.defaultdict(set)
        self.boxes = collections.defaultdict(set)
        self.empty = collections.deque()
        self.board = [
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

    def prepBoard(self):
        """
        adds each position to corresponding dictionary set
        in: self.board: 2d list
        return: None => adds values already in each box to corresponding dictionary sets
        """
        for i in range(0, 9):
            for k in range(0, 9):
                if self.board[i][k] == 0:
                    self.empty.append([i, k])
                else:
                    self.columns[k].add(self.board[i][k])
                    self.rows[i].add(self.board[i][k])
                    self.boxes[(i//3, k//3)].add(self.board[i][k])

    def makeBoard(self):
        """
        Creates the dispaly of the sudoku self.board
        return: None
        """
        for i in range(len(self.board)):
            if i % 3 == 0:
                print("------------------------")
            for k in range(len(self.board[0])):
                if k % 3 == 0:
                    print("| ", end="")
                print(str(self.board[i][k]) + " ", end="")
            print("|", end="\n")
        print("------------------------")

    def solve(self, index):
        """
        solves sudoku using backtracking
        in: empty => List[List[]] deque of all unfilled boxes where each item in list is a sublist of row and column of unfilled box
        return: boolean value
        """
        # base case
        if index >= len(self.empty):
            return True
        r, c = self.empty[index]

        # recursive case
        for i in range(1, 10):
            self.board[r][c] = i
            if self.isValid(r, c):
                self.columns[c].add(self.board[r][c])
                self.rows[r].add(self.board[r][c])
                self.boxes[(r//3, c//3)].add(self.board[r][c])
                if self.solve(index + 1):
                    return True
                self.columns[c].remove(self.board[r][c])
                self.rows[r].remove(self.board[r][c])
                self.boxes[(r//3, c//3)].remove(self.board[r][c])

        return False

    def isValid(self, i, k):
        """
        checks to see if the value at a particular spot in the self.board violates the principles of sudoku
        in: i, k => integers that correspond to a row and column of the 2d self.board
        return: boolean value stating whether the value violates the sudoku principles or not
        """
        if (self.board[i][k] in self.rows[i] or
            self.board[i][k] in self.columns[k] or
                self.board[i][k] in self.boxes[(i//3, k//3)]):
            return False
        return True


sud = Sudoku()
sud.makeBoard()
sud.prepBoard()
sud.solve(0)
sud.makeBoard()

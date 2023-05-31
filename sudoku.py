import collections
from turtle import update
import pygame
from sys import exit


class Sudoku:

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

    def __init__(self, screen):
        self.columns = collections.defaultdict(set)
        self.rows = collections.defaultdict(set)
        self.boxes = collections.defaultdict(set)
        self.empty = collections.deque()
        self.model = None
        self.width = 540
        self.height = 540
        self.squares = [[Square(self.board[i][j], i, j)
                         for j in range(9)] for i in range(9)]
        self.modelUpdate()
        self.screen = screen
        self.selectedSquare = None

    def modelUpdate(self):
        self.columns.clear()
        self.rows.clear()
        self.boxes.clear()
        self.empty.clear()
        self.model = [
            [self.squares[i][j].value for j in range(9)] for i in range(9)]
        for i in range(9):
            for k in range(9):
                if self.model[i][k] == 0:
                    self.empty.append([i, k])
                else:
                    self.columns[k].add(self.model[i][k])
                    self.rows[i].add(self.model[i][k])
                    self.boxes[(i//3, k//3)].add(self.model[i][k])

    def set(self, num):
        i, j = self.selectedSqare
        if self.squares[i][j].value == 0:
            self.squares[i][j].changeValue(num)
            self.modelUpdate()

            if self.isValid(i, j, self.model, self.modelRows, self.modelCols, self.modelBoxs) and self.testSolve():
                return True
            else:
                self.squares[i][j].changeValue(0)
                self.squares[i][j].tValue(0)
                self.modelUpdate()
                return False

    def selectedNumber(self, value):
        i, j = self.selectedSquare
        self.squares[i][j].tValue(value)

    def loseNumber(self):
        i, j = self.selectedSquare
        if self.squares[i][j].value == 0:
            self.squares[i][j].tValue(0)

    def selectSquare(self, r, c):
        for i in range(9):
            for j in range(9):
                self.squares[i][j].selectedSquare = False
        self.squares[r][c].selectedSquare = True
        self.selectedSquare = (r, c)

    def testSolve(self):
        """
        test solves

        """

        cols = self.columns.copy()
        rows = self.rows.copy()
        boxes = self.boxes.copy()
        emp = self.empty.copy()
        board = self.model.copy()

        for i in range(9):
            for k in range(9):
                if board[i][k] == 0:
                    emp.append([i, k])
                else:
                    cols[k].add(board[i][k])
                    rows[i].add(board[i][k])
                    boxes[(i//3, k//3)].add(board[i][k])

        def solve(self, index):
            """
            solves sudoku using backtracking
            in: empty => List[List[]] deque of all unfilled boxes where each item in list is a sublist of row and column of unfilled box
            return: boolean value
            """
            # base case
            if index >= len(emp):
                return True
            r, c = emp[index]

            # recursive case
            for i in range(1, 10):
                board[r][c] = i
                if self.isValid(r, c, board, rows, cols, boxes):
                    cols[c].add(board[r][c])
                    rows[r].add(board[r][c])
                    boxes[(r//3, c//3)].add(board[r][c])
                    if solve(index + 1):
                        return True
                    cols[c].remove(board[r][c])
                    rows[r].remove(board[r][c])
                    boxes[(r//3, c//3)].remove(board[r][c])

            return False

        return solve(0)

    def isValid(self, i, k, board, rows, cols, boxes):
        """
        checks to see if the value at a particular spot in the self.board violates the principles of sudoku
        in: i, k => integers that correspond to a row and column of the 2d self.board
        return: boolean value stating whether the value violates the sudoku principles or not
        """
        if (board[i][k] in rows[i] or
            board[i][k] in cols[k] or
                board[i][k] in boxes[(i//3, k//3)]):
            return False
        return True

    def drawSudoku(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (130, 130, 540, 540), 6)
        for i in range(9):
            for j in range(9):
                if i % 3 == 0 and j % 3 == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (130 + (180 * i/3), 130 + (180 * j/3), 180, 180), 3)
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (130 + (60 * i), 130 + (60 * j), 60, 60), 1)

        for i in range(9):
            for j in range(9):
                self.squares[i][j].drawSquare(self.screen)


class Square:

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.t = 0
        self.selectedSquare = False

    def changeValue(self, value):
        self.value = value

    def tValue(self, value):
        self.t = value

    def drawSquare(self, screen):
        font = pygame.font.SysFont("Arial", 40)

        if self.selectedSquare:
            pygame.draw.rect(screen, (160, 32, 240), (130 +
                             (60 * self.row), 130 + (60 * self.col), 60, 60), 1)

        if self.value != 0:
            num = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(num, (130 + (60 * self.row) +
                        20, 130 + (60 * self.col) + 10))
        elif self.t != 0 and self.value == 0:
            num = font.render(str(self.t), True, (160, 32, 240))
            screen.blit(num, (130 + (60 * self.row) +
                        20, 130 + (60 * self.col) + 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Sudoku')
    sudoku = Sudoku(screen)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    # text_surface = font.render()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # screen.blit(, (0, 0))

        sudoku.drawSudoku()
        pygame.display.update()
        clock.tick(60)


main()

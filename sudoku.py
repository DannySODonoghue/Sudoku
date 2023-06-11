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

    def setValue(self, num):
        i, j = self.selectedSquare
        if self.squares[i][j].value == 0:
            self.squares[i][j].changeValue(num)

            if self.isValid(i, j, num, self.rows, self.columns, self.boxes) and self.testSolve():
                self.modelUpdate()
                return True
            else:
                self.squares[i][j].changeValue(0)
                self.squares[i][j].changeTest(None)
                self.modelUpdate()
                return False

    def testSelectedNumber(self, value):
        i, j = self.selectedSquare
        if self.squares[i][j].value == 0:
            self.squares[i][j].changeTest(value)

    def clearNumber(self):
        i, j = self.selectedSquare
        if self.squares[i][j].value == 0:
            self.squares[i][j].changeTest(None)
            self.modelUpdate()

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
        self.modelUpdate()
        cols = self.columns.copy()
        rows = self.rows.copy()
        boxes = self.boxes.copy()
        emp = self.empty.copy()
        board = self.model.copy()

        def solve(index):
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
                if self.isValid(r, c, i, rows, cols, boxes):
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

    def isValid(self, i, k, num, rows, cols, boxes):
        """
        checks to see if the value at a particular spot in the self.board violates the principles of sudoku
        in: i, k => integers that correspond to a row and column of the 2d self.board
        return: boolean value stating whether the value violates the sudoku principles or not
        """
        if (num in rows[i] or
            num in cols[k] or
                num in boxes[(i//3, k//3)]):
            return False
        return True

    def drawSudoku(self):
        if self.selectedSquare:
            i, j = self.selectedSquare
            row, col = self.squares[i][j].row, self.squares[i][j].col
            pygame.draw.rect(self.screen, (250, 164, 52), (130 +
                                                           (60 * col), 130 + (60 * row), 60, 60))
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

    def clickBox(self, position):
        if position[0] > 130 and position[0] < 670 and position[1] > 130 and position[1] < 670:
            return ((position[1] - 130) // 60, (position[0] - 130) // 60)
        else:
            return False

    def sudokuDone(self):
        for i in range(9):
            for j in range(9):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def completeModel(self):
        self.modelUpdate()

        def solveModel(index):

            if index >= len(self.empty):
                return True
            r, c = self.empty[index]

            # recursive case
            for i in range(1, 10):
                self.model[r][c] = i
                if self.isValid(r, c, i, self.rows, self.columns, self.boxes):
                    self.squares[r][c].changeValue(i)
                    self.squares[r][c].updateGUIChange(self.screen, True)
                    self.model = [
                        [self.squares[i][j].value for j in range(9)] for i in range(9)]
                    self.columns[c].add(self.model[r][c])
                    self.rows[r].add(self.model[r][c])
                    self.boxes[(r//3, c//3)].add(self.model[r][c])
                    pygame.display.update()
                    pygame.time.delay(100)

                    if solveModel(index + 1):
                        return True

                    self.columns[c].remove(self.model[r][c])
                    self.rows[r].remove(self.model[r][c])
                    self.boxes[(r//3, c//3)].remove(self.model[r][c])
                    self.model[r][c] = 0
                    self.squares[r][c].changeValue(0)
                    self.squares[r][c].updateGUIChange(self.screen, False)
                    self.model = [
                        [self.squares[i][j].value for j in range(9)] for i in range(9)]
                    pygame.display.update()
                    pygame.time.delay(100)

            return False

        solveModel(0)


class Square:

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.test = None
        self.selectedSquare = False
        self.guess = None

    def changeValue(self, value):
        self.value = value

    def changeTest(self, value):
        self.test = value

    def drawSquare(self, screen):
        font = pygame.font.SysFont("Arial", 40)

        if self.selectedSquare:
            if self.guess == True:
                self.guess == None
                pygame.draw.rect(screen, (0, 255, 0), (130 +
                                                       (60 * self.col), 130 + (60 * self.row), 60, 60), 1)
            elif self.guess == False:
                self.guess == None
                pygame.draw.rect(screen, (255, 0, 0), (130 +
                                                       (60 * self.col), 130 + (60 * self.row), 60, 60), 1)

        if self.guess == True:
            self.guess == None
            pygame.draw.rect(screen, (0, 255, 0), (130 +
                                                   (60 * self.col), 130 + (60 * self.row), 60, 60), 1)
        elif self.guess == False:
            self.guess == None
            pygame.draw.rect(screen, (255, 0, 0), (130 +
                                                   (60 * self.col), 130 + (60 * self.row), 60, 60), 1)

        if self.value != 0:
            num = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(num, (130 + (60 * self.col) +
                        20, 130 + (60 * self.row) + 10))
        elif self.test and self.value == 0:
            num = font.render(str(self.test), True, (0, 0, 0))
            screen.blit(num, (130 + (60 * self.col) +
                        20, 130 + (60 * self.row) + 10))

    def updateGUIChange(self, screen, val):
        pygame.draw.rect(screen, (255, 255, 255), ((130 +
                                                   (60 * self.col), 130 + (60 * self.row), 60, 60)), 0)
        font = pygame.font.SysFont("Arial", 40)
        if self.value != 0:
            num = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(num, (130 + (60 * self.col) +
                        20, 130 + (60 * self.row) + 10))

        if val:
            pygame.draw.rect(screen, (0, 255, 0), (130 +
                                                   (60 * self.col), 130 + (60 * self.row), 60, 60), 1)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (130 +
                                                   (60 * self.col), 130 + (60 * self.row), 60, 60), 1)


def drawLegend(screen):
    font = pygame.font.SysFont("Comicsans", 60)
    legFont = pygame.font.SysFont("Comicsans", 25)
    keyFont = pygame.font.SysFont("Comicsans", 15)

    titleSurface = font.render("Sudoku", True, 'Black')
    legendSurface = legFont.render("Legend:", True, 'Black')
    key1Surface = keyFont.render("- c: Auto complete sudoku", True, 'Black')
    key2Surface = keyFont.render("- d: Delete selected value", True, 'Black')
    key3Surface = keyFont.render(
        "- Return: Enter selected value", True, 'Black')

    screen.blit(titleSurface, (300, 30))
    screen.blit(legendSurface, (50, 10))
    screen.blit(key1Surface, (50, 50))
    screen.blit(key2Surface, (50, 70))
    screen.blit(key3Surface, (50, 90))


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Sudoku')
    sudoku = Sudoku(screen)
    font = pygame.font.SysFont("Times New Roman", 60)
    completeSurface = font.render("Complete!", True, 'Black')
    complete = False

    while True:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                i, j = pygame.mouse.get_pos()
                if sudoku.clickBox((i, j)):
                    clickedBox = sudoku.clickBox((i, j))
                    sudoku.selectSquare(clickedBox[0], clickedBox[1])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if sudoku.selectedSquare:
                    i, j = sudoku.selectedSquare
                    if event.key == pygame.K_DOWN:
                        if i + 1 < 9:
                            sudoku.selectSquare(i + 1, j)
                    if event.key == pygame.K_UP:
                        if i - 1 >= 0:
                            sudoku.selectSquare(i - 1, j)
                    if event.key == pygame.K_LEFT:
                        if j - 1 >= 0:
                            sudoku.selectSquare(i, j - 1)
                    if event.key == pygame.K_RIGHT:
                        if j + 1 < 9:
                            sudoku.selectSquare(i, j + 1)

                    if event.key == pygame.K_d:
                        sudoku.clearNumber()
                    if event.key == pygame.K_RETURN:
                        i, j = sudoku.selectedSquare
                        if sudoku.squares[i][j].test:
                            key = None
                            if sudoku.setValue(sudoku.squares[i][j].test):
                                sudoku.squares[i][j].guess = True
                            else:
                                sudoku.squares[i][j].guess = False
                        if sudoku.sudokuDone():
                            print("Complete!")
                            complete = True

                if event.key == pygame.K_c:
                    sudoku.completeModel()

        if key and sudoku.selectedSquare:
            sudoku.testSelectedNumber(key)

        screen.fill((255, 255, 255))
        sudoku.drawSudoku()
        drawLegend(screen)
        if complete:
            screen.fill((255, 255, 255))
            screen.blit(completeSurface, (300, 300))
        pygame.display.update()


main()

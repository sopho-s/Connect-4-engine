import pygame


class board:
    def __init__(self):
        self.board = [[0 for _ in range(6)] for _ in range(7)]
        self.moves = []

    def addcounter(self, column, colour):
        """
        It checks if the column is full, if it isn't, it adds a counter to the top of the column and then checks if any
        counters need to be moved down

        :param column: the column you want to add a counter to
        :param colour: 1 for red, 2 for yellow
        :return: a boolean value.
        """
        if self.board[column][5] == 0:
            self.board[column][5] = colour
            self.moves.append(column)
            for i in range(5):
                if self.board[column][5 - i] > 0 and self.board[column][4 - i] == 0:
                    self.board[column][4 - i] = self.board[column][5 - i]
                    self.board[column][5 - i] = 0
            return True
        else:
            return False

    def getboard(self):
        return self.board

    def getmoves(self):
        return self.moves

    def reset(self):
        self.board = [[0 for _ in range(6)] for _ in range(7)]
        self.moves = []

    def getrects(self):
        """
        It takes the board, and returns a list of tuples, each tuple containing a color and a rectangle
        :return: A list of lists. Each list contains a tuple of RGB values and a pygame.Rect object.
        """
        rectboard = []
        for i in range(7):
            for t in range(6):
                if self.board[i][5 - t] != 0:
                    rectboard.append([(((self.board[i][5 - t] + 1) % 2) * 255, 0, (self.board[i][5 - t] % 2) * 255),
                                      pygame.Rect(i * 100, t * 100, 100, 100)])
        return rectboard

    def check_horizontal(self, board):
        """
        For each row in the board, check if the first four elements are the same and not equal to zero

        :param board: The current board state
        :return: a boolean value.
        """
        for row in board:
            for i in range(len(row) - 3):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != 0:
                    return True
        return False

    def check_vertical(self, board):
        """
        We iterate through the columns of the board and check if the four consecutive values in the column are equal and not
        zero

        :param board: the current board
        :return: a boolean value.
        """
        for i in range(len(board[0])):
            for j in range(len(board) - 3):
                if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] and board[j][i] != 0:
                    return True
        return False

    def check_diagonal_top_left_to_bottom_right(self, board):
        """
        We iterate through the board, checking if the current position is equal to the next 3 positions in the diagonal

        :param board: The current state of the board
        :return: a boolean value.
        """
        # Check for diagonal 4 in a row (top-left to bottom-right)
        for i in range(len(board[0]) - 3):
            for j in range(len(board) - 3):
                if board[j][i] == board[j + 1][i + 1] == board[j + 2][i + 2] == board[j + 3][i + 3] and board[j][
                    i] != 0:
                    return True
        return False

    def check_diagonal_bottom_left_to_top_right(self, board):
        """
        We iterate through the board, starting at the bottom left corner, and check if the current position, the position
        above and to the right, the position above and two to the right, and the position above and three to the right are
        all the same and not 0

        :param board: The game board
        :return: a boolean value.
        """
        # Check for diagonal 4 in a row (bottom-left to top-right)
        for i in range(len(board[0]) - 3):
            for j in range(3, len(board)):
                if board[j][i] == board[j - 1][i + 1] == board[j - 2][i + 2] == board[j - 3][i + 3] and board[j][
                    i] != 0:
                    return True
        return False

    def check_four_in_a_row(self):
        """
        If there is a horizontal, vertical, or diagonal 4 in a row, return True. Otherwise, return False
        :return: a boolean value.
        """
        if self.check_horizontal(self.board) or self.check_vertical(
                self.board) or self.check_diagonal_top_left_to_bottom_right(
            self.board) or self.check_diagonal_bottom_left_to_top_right(self.board):
            return True

        # No 4 in a row found
        return False


def user_click():
    x, _ = pygame.mouse.get_pos()
    return x // 100


def main():
    """
    It creates a gameboard object, initialises pygame, and then runs a loop that checks for a mouse click, adds a counter to
    the gameboard, and then checks if the game is over.
    """
    player = 1
    gameboard = board()
    pygame.init()
    pygame.display.set_caption("connect 4")

    screen = pygame.display.set_mode((700, 600))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = user_click()
                if gameboard.addcounter(pos, player):
                    for rectangle in gameboard.getrects():
                        pygame.draw.rect(screen, rectangle[0], rectangle[1])
                    pygame.display.flip()
                    pygame.display.update()
                    if player == 1:
                        player = 2
                    else:
                        player = 1
                    running = not gameboard.check_four_in_a_row()

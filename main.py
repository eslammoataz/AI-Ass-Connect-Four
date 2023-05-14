import random

import numpy as np
import pygame
import sys
import math

# Global variable for the rows and cols of the board
rowCount = 6
colCount = 7
squareSize = 100
player = 0
playerPiece = 1
AI = 1
AiPiece = 2
turn = random.randint(player, AI)

windowLength = 4
empty = 0

# color of the board
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# info about the board
radius = int(squareSize / 2 - 5)
width = colCount * squareSize
height = (rowCount + 1) * squareSize


def create_board():
    board = np.zeros((rowCount, colCount))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


# checks if the last row in empty or not
def isValid_Location(board, col):
    return board[5][col] == 0


def get_next_open_rows(board, col):
    for r in range(rowCount):
        if board[r][col] == 0:
            return r


def printBoard(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizontally
    for c in range(colCount - 3):
        for r in range(rowCount):
            win = 1
            for nc in range(4):
                if (board[r][c + nc] != piece):
                    win = 0
            if win == 1:
                return True;

    # check horizontally
    for c in range(colCount):
        for r in range(rowCount - 3):
            win = 1
            for nr in range(4):
                if (board[r + nr][c] != piece):
                    win = 0
            if win == 1:
                return True;

    # check for pos dag
    for c in range(colCount - 3):
        for r in range(rowCount - 3):
            win = 1
            for add in range(4):
                if (board[r + add][c + add] != piece):
                    win = 0
            if win == 1:
                return True;

    # check for neg dag
    for c in range(colCount - 3):
        for r in range(3, rowCount):
            win = 1
            for add in range(4):
                if (board[r - add][c + add] != piece):
                    win = 0
            if win == 1:
                return True


def evaluate_window(window, piece):
    score = 0
    opponent_piece = playerPiece
    if piece == playerPiece:
        opponent_piece = AiPiece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 5
    if window.count(piece) == 2 and window.count(empty) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(empty) == 1:
        score -= 4
    return score


def score_position(board, piece):
    score = 0
    # score center col
    center_array = [int(i) for i in list(board[:, colCount // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # score horizontal
    for r in range(rowCount):
        row_array = [int(i) for i in list(board[r, :])]  # takes specific row with all the cols
        for c in range(colCount - 3):
            window = row_array[c:c + windowLength]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(colCount):
        col_array = [int(i) for i in list(board[:, c])]  # takes specific col with all the row
        for r in range(rowCount - 3):
            window = col_array[r:r + windowLength]
            score += evaluate_window(window, piece)

    # score pos diag
    for r in range(rowCount - 3):
        for c in range(colCount - 3):
            window = [board[r + i][c + i] for i in range(windowLength)]
            score += evaluate_window(window, piece)

    # score for neg diag
    for r in range(rowCount - 3):
        for c in range(colCount - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowLength)]
            score += evaluate_window(window, piece)

    return score


def is_tereminalNode(board):
    return winning_move(board, playerPiece) or winning_move(board, AiPiece) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_tereminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AiPiece):
                return (None, 100000000000000)
            elif winning_move(board, playerPiece):
                return (None, -10000000000000)
            else:  # more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AiPiece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_rows(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, AiPiece)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_rows(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, playerPiece)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(colCount):
        if isValid_Location(board, col):
            valid_locations.append(col)

    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_rows(board, col)
        temp_board = board.copy()
        dropPiece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def drawBoard(board):
    for c in range(colCount):
        for r in range(rowCount):
            pygame.draw.rect(screen, blue, (c * squareSize, r * squareSize + squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, black, (
                int(c * squareSize + squareSize / 2), int(r * squareSize + squareSize + squareSize / 2)), radius)

    for c in range(colCount):
        for r in range(rowCount):
            if board[r][c] == playerPiece:
                pygame.draw.circle(screen, red, (
                    int(c * squareSize + squareSize / 2), height - int(r * squareSize + squareSize / 2)), radius)
            elif (board[r][c] == AiPiece):
                pygame.draw.circle(screen, yellow, (
                    int(c * squareSize + squareSize / 2), height - int(r * squareSize + squareSize / 2)), radius)

    pygame.display.update()


board = create_board()
printBoard(board)

gameOver = False

pygame.init()

size = (width, height)

screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            posx = event.pos[0]
            if turn == player:
                pygame.draw.circle(screen, red, (posx, int(squareSize / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))

            # Ask for player 1 Input
            if turn == player:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))
                if (isValid_Location(board, col)):
                    dropPiece(board, get_next_open_rows(board, col), col, playerPiece)
                    if winning_move(board, playerPiece):
                        label = myfont.render("Player 1 Wins!!", 1, red)
                        screen.blit(label, (15, 10))
                        gameOver = True
                    turn += 1
                    turn = turn % 2
                    printBoard(board)
                    drawBoard(board)
                else:
                    print("Not Valid input")

    if (turn == AI and not gameOver):
        col, minimaxScore = minimax(board, 5, -math.inf, math.inf, True)
        if (isValid_Location(board, col)):
            dropPiece(board, get_next_open_rows(board, col), col, AiPiece)
            if winning_move(board, AiPiece):
                label = myfont.render("Player 2 Wins!!", 1, yellow)
                screen.blit(label, (15, 10))
                gameOver = True
            else:
                print("Not Valid input")
            turn += 1
            turn = turn % 2
            printBoard(board)
            drawBoard(board)

    if gameOver:
        pygame.time.wait(3000)

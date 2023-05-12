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
                return True;


def score_position(board, piece):
    # score horizontal
    score = 0
    for r in range(rowCount):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(colCount - 3):
            window = row_array[c:c + windowLength]
            if window.count(piece) == 4:
                score += 100
            if window.count(piece) == 3 and window.count(empty) == 1:
                score += 10

    return score

def get_valid_locations(board):
    valid_location = []
    for col in range(colCount):
        if isValid_Location(board,col):
            valid_location.append(col)

    return valid_location

def pick_best_move(board,piece):
    valid_locations=get_valid_locations(board)
    best_score =0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_rows(board,col)
        temp_board = board.copy()
        dropPiece(temp_board,row,col,piece)
        score = score_position(temp_board,piece)
        if score > best_score:
            best_score = score
            best_col = col

    return  best_col

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
        col = random.randint(0, colCount - 1)
        if (isValid_Location(board, col)):
            pygame.time.wait(500)
            dropPiece(board, get_next_open_rows(board, col), col, AiPiece)
            if winning_move(board, playerPiece):
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
        pygame.time.wait(2000)

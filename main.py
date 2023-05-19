import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np
import pygame
import sys
import math
from PIL import ImageTk, Image

# ---------------------------------------------------------#
# GUI PART
import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk

gameDifficulty = 1
selected_option = ""


def submit():
    global gameDifficulty, selected_option
    input_value = entry.get()
    gameDifficulty = input_value

    # Check if the input is within the range of 1 to 5
    if input_value.isdigit() and 1 <= int(input_value) <= 5:
        input_text = input_value
        output_label.config(text="You entered: " + input_text)
        selected_option = checkbox_var.get()  # Get the selected checkbox value
        window.destroy()  # Close the window
    else:
        output_label.config(text="Invalid input. Please enter a value from 1 to 5.", bg="#80c1ff")


# Create the main window
window = tk.Tk()
window.title("Connect Four Game")

# Load the background image
image_path = "./bck.png"
background_image = Image.open(image_path)
background_image = background_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Calculate the screen dimensions and center the window
window_width = 600
window_height = 500
x_position = int((window.winfo_screenwidth() / 2) - (window_width / 2))
y_position = int((window.winfo_screenheight() / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set the font size for the window
font_style = tkfont.Font(size=14)
window.option_add("*Font", font_style)

# Create a label to display the welcome message
welcome_label = tk.Label(window, text="Welcome to Connect Four Game", font=("Arial", 16, "bold"), bg="#80c1ff",
                         fg="white", highlightthickness=2, highlightcolor="black")
welcome_label.pack(pady=10)

# Create a frame to hold the label, entry, and checkboxes
frame = tk.Frame(window, bg="#80c1ff")
frame.pack(expand=True)

# Create a label and an entry widget for input
label = tk.Label(frame, text="Enter the game difficulty from 1 to 5:", font=("Arial", 16, "bold"), bg="#80c1ff",
                 fg="white", highlightthickness=0, highlightcolor="black")
label.pack(anchor="center")

entry = tk.Entry(frame)
entry.pack(anchor="center", pady=10)

# Create checkboxes
checkbox_var = tk.StringVar()
checkbox1 = tk.Checkbutton(frame, text="Minimax", variable=checkbox_var, bg="#80c1ff",onvalue="Minimax", offvalue="")
checkbox1.pack(anchor="center")
checkbox2 = tk.Checkbutton(frame, text="Minimax Alpha beta", variable=checkbox_var,bg="#80c1ff", onvalue="MinimaxAB", offvalue="")
checkbox2.pack(anchor="center")

# Create a styled button to submit the input
button_style = {"font": font_style, "background": "#80c1ff", "foreground": "white", "border": 0, "width": 20,
                "height": 2}
submit_button = tk.Button(window, text="Submit", command=submit, **button_style)
submit_button.pack(pady=10)

# Create a label to display the output
output_label = tk.Label(window, text="", highlightthickness=2, highlightcolor="black")
output_label.pack()


# Start the main event loop
window.mainloop()

# ---------------------------------------------------------------#


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

print(selected_option)
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

    # check vertically
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
        score += 10
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(empty) == 1:
        score -= 100
    elif window.count(opponent_piece) == 2 and window.count(empty) == 2:
        score -= 5
    if window.count(opponent_piece) == 4:
        score -= 100  # Add this

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


def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return -1, -1
    is_terminal = is_tereminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AiPiece):
                return None, 100000000000000
            elif winning_move(board, playerPiece):
                return None, -10000000000000
            else:  # more valid moves
                return None, 0
        else:  # Depth is zero
            return (pick_best_move(board, AiPiece), score_position(board, AiPiece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_rows(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, AiPiece)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_rows(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, playerPiece)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def minimax_alphaBeta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return -1, -1
    is_terminal = is_tereminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AiPiece):
                return None, 100000000000000
            elif winning_move(board, playerPiece):
                return None, -10000000000000
            else:  # more valid moves
                return None, 0
        else:  # Depth is zero
            return (pick_best_move(board, AiPiece), score_position(board, AiPiece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_rows(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, AiPiece)
            new_score = minimax_alphaBeta(b_copy, depth - 1, alpha, beta, False)[1]
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
            new_score = minimax_alphaBeta(b_copy, depth - 1, alpha, beta, True)[1]
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
    if len(valid_locations) == 0:
        return -1  # tie
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

myfont = pygame.font.SysFont("georgia", 75)
print(gameDifficulty)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()

    # Ask for player 1 Input
    if turn == player:

        col = pick_best_move(board, playerPiece)
        # tie
        if col == -1:
            label = myfont.render("Tie Game", 1, (0, 128, 0))
            screen.blit(label, (80, 10))
            gameOver = True

        elif isValid_Location(board, col) and not gameOver:
            pygame.time.wait(500)
            row = get_next_open_rows(board, col)
            dropPiece(board, row, col, playerPiece)
            if winning_move(board, playerPiece):
                label = myfont.render("Player 1 wins!!", 1, red)
                screen.blit(label, (80, 10))
                gameOver = True

            printBoard(board)
            drawBoard(board)

            turn += 1
            turn = turn % 2
        else:  # tie
            label = myfont.render("Tie Game", 1, (0, 128, 0))
            screen.blit(label, (80, 10))
            gameOver = True

    # # Ask for Player 2 Input
    if turn == AI and not gameOver:
        # col, minimax_score = minimax(board, int(gameDifficulty), True)
        col, minimax_score = minimax_alphaBeta(board, 5, -math.inf, math.inf, True)

        # tie
        if col == -1:
            label = myfont.render("Tie Game", 1, (0, 128, 0))
            screen.blit(label, (80, 10))
            gameOver = True

        elif isValid_Location(board, col):
            pygame.time.wait(500)
            row = get_next_open_rows(board, col)
            dropPiece(board, row, col, AiPiece)

            if winning_move(board, AiPiece):
                label = myfont.render("Player 2 wins!!", 1, yellow)
                screen.blit(label, (80, 10))
                gameOver = True

            printBoard(board)
            drawBoard(board)

            turn += 1
            turn = turn % 2
        else:
            label = myfont.render("Tie Game", 1, (0, 128, 0))
            screen.blit(label, (80, 10))
            gameOver = True

    if gameOver:
        pygame.time.wait(3000)

    pygame.time.wait(1000)

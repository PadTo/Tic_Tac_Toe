import sys
import pygame
import os
import numpy as np

pygame.init()


#####    Constants   #####

# Board Dimensions
WIDTH = 600
HEIGHT = 600
BOARD_ROWS = 3
BOARD_COLS = 3
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# RGB Colors
COLOR = (23, 145, 135)
BG_COLOR = (28, 170, 156)
BLACK = (0, 0, 0)

#####    Constants   #####


#####    Displaying Game Window   #####

# Displaying and Filing the Screen Color
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOR)

# Loading an Image and Fitting it on the the main screen
image = pygame.image.load('MRTN.jpg')
# Setting transparency
image.set_alpha(00)
image_rect = image.get_rect(center=(WIDTH//2, HEIGHT//2))

# Displaying the image and changing the caption
screen.blit(image, image_rect)
pygame.display.set_caption("Tic Tac Toe")

#####    Displaying Game Window   #####


##################### FUNCTIONS #####################

def draw_lines(color=(23, 145, 135), HEIGHT=0, WIDTH=0, EDGE_POS=50, THICK=5):
    # Color: a tuple with 3 variables that are equivalet to an RGB scale
    # Height: The entire height of the game window
    # Width: The entire width of the game window
    # Edge Position: the position of each line from the side surfaces
    # Thick: Thickness of the horizontal and vertical lines

    inc_horz_line_pos = np.floor(HEIGHT/3)
    inc_vert_line_pos = np.floor(WIDTH/3)

    horz_pos = inc_horz_line_pos.copy()
    vert_pos = inc_vert_line_pos.copy()

    for i in range(0, 3):
        pygame.draw.line(
            screen, color, (EDGE_POS, horz_pos), (WIDTH - EDGE_POS, (horz_pos)), THICK)
        pygame.draw.line(
            screen, color, (vert_pos, EDGE_POS), (vert_pos, HEIGHT - EDGE_POS), THICK)

        horz_pos += inc_horz_line_pos
        vert_pos += inc_vert_line_pos


# A function "do mark square"
def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0

    # Can also use:
    # if board[row][col] == 0:
    #     return True
    # else:
    #     return False


def is_bard_full():

    for row in board.shape[0]:
        for col in board.shape[1]:
            if board[row][col] == 0:
                return False

    return True


def draw_figures(COLOR_1=(255, 255, 255), COLOR_2=(0, 0, 0), SIDE_DIST=40):
    width = 14
    multiplier = 2
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen, COLOR_1, (int(col * WIDTH//3 + WIDTH//3 // 2), int(row * HEIGHT//3 + HEIGHT//3 // 2)), int(WIDTH//3 // 2 - SIDE_DIST), width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, COLOR_2, (col * WIDTH //
                                 3 + SIDE_DIST, row * HEIGHT//3 + SIDE_DIST),
                                 (col * WIDTH // 3 + WIDTH // 3 - SIDE_DIST,
                                  row * HEIGHT // 3 + HEIGHT // 3 - SIDE_DIST), width * multiplier)

                pygame.draw.line(screen, COLOR_2, (col * WIDTH //
                                 3 - SIDE_DIST + WIDTH//3, row * HEIGHT//3 + SIDE_DIST),
                                 (col * WIDTH // 3 + SIDE_DIST,
                                  row * HEIGHT // 3 + HEIGHT // 3 - SIDE_DIST), width * multiplier)


def check_win(player):

    player_1_win_sum = 3
    player_2_win_sum = 8
    sum = 0

    col_win = False
    row_win = False
    diag_win = False

    win_state = np.zeros(8)

    for col in range(BOARD_COLS):

        if board[:, col] == player_1_win_sum or board[:, col] == player_2_win_sum:
            draw_vertical_winning_line(col, player)
            return True

    for row in range(BOARD_ROWS):

        if board[row, :] == player_1_win_sum or board[row, :] == player_2_win_sum:
            draw_horizontal_winning_line(col, player)
            return True


def draw_asc_diag(player):
    pass


def draw_des_diag(player):
    pass


def draw_vertical_winning_line(col, player):
    pass


def draw_horizontal_winning_line(row, player):
    pass


def draw_diagonal_winning_line(row, player):
    pass


def restart():
    pass


##################### FUNCTIONS #####################
draw_lines(COLOR, HEIGHT, WIDTH, EDGE_POS=10)


player = 2


# mainloop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(np.floor(mouseY / (WIDTH//3)))
            clicked_col = int(np.floor(mouseX / (HEIGHT//3)))

            # print(clicked_row)
            # print(clicked_col)

            if available_square(clicked_row, clicked_col):
                if player == 2:
                    player = 1
                    mark_square(clicked_row, clicked_col, 2)

                    # print(player)

                elif player == 1:
                    player = 2
                    mark_square(clicked_row, clicked_col, 1)

                draw_figures()

                if check_win():
                    pass

    pygame.display.update()

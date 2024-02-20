import sys
import pygame
import os
import numpy as np


def init_game():

    global WIDTH, HEIGHT, THIRD_WIDTH, THIRD_HEIGHT, BOARD_ROWS, BOARD_COLS, board
    global COLOR, BG_COLOR, BLACK, screen

    pygame.init()  # Initialize the Pygame library

    #####    Constants   #####

    # Board Dimensions
    WIDTH = 600  # Width of the game window
    HEIGHT = 600  # Height of the game window
    # Width of one-third of the game window, used for board division
    THIRD_WIDTH = WIDTH // 3
    # Height of one-third of the game window, used for board division
    THIRD_HEIGHT = HEIGHT // 3

    BOARD_ROWS = 3  # Number of rows in the game board
    BOARD_COLS = 3  # Number of columns in the game board
    # Initialize the game board with zeros
    board = np.zeros((BOARD_ROWS, BOARD_COLS))

    # RGB Colors
    COLOR = (23, 145, 135)  # Color for the lines on the board
    BG_COLOR = (28, 170, 156)  # Background color of the game window
    BLACK = (0, 0, 0)  # Color for drawing X's or O's, if needed

    #####    Constants   #####

    #####    Displaying Game Window   #####

    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_COLOR)  # Fill the background with the specified color

    # Load and set an image for the background
    image = pygame.image.load('MRTN.jpg')
    image.set_alpha(00)  # Set the transparency of the image
    image_rect = image.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(image, image_rect)  # Draw the image on the screen
    pygame.display.set_caption("Tic Tac Toe")  # Set the window caption

    #####    Displaying Game Window   #####

    # Initial call to draw the grid lines
    draw_lines(COLOR, HEIGHT, WIDTH, EDGE_POS=10)


def draw_lines(color=(23, 145, 135), HEIGHT=0, WIDTH=0, EDGE_POS=50):
    # Function to draw the grid lines on the board
    THICK = HEIGHT//30  # Thickness of the lines based on the window height

    # Calculate the positions for the horizontal and vertical lines
    inc_horz_line_pos = np.floor(HEIGHT/3)
    inc_vert_line_pos = np.floor(WIDTH/3)

    # Initialize position variables for drawing lines
    horz_pos = inc_horz_line_pos.copy()
    vert_pos = inc_vert_line_pos.copy()

    # Draw two horizontal and two vertical lines to create the grid
    for i in range(0, 3):
        pygame.draw.line(screen, color, (EDGE_POS, horz_pos),
                         (WIDTH - EDGE_POS, horz_pos), THICK)
        pygame.draw.line(screen, color, (vert_pos, EDGE_POS),
                         (vert_pos, HEIGHT - EDGE_POS), THICK)
        horz_pos += inc_horz_line_pos
        vert_pos += inc_vert_line_pos


def mark_square(row, col, player):
    # Mark the specified square with the current player's number
    board[row][col] = player


def available_square(row, col):
    # Check if the specified square is available (not already marked)
    return board[row][col] == 0


def is_board_full():
    # Check if the board is full (no more available squares)
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == 0:
                return False
    return True


def draw_figures(COLOR_1=(255, 255, 255), COLOR_2=(0, 0, 0)):
    # Function to draw the players' marks (O for player 1, X for player 2)
    THICK = WIDTH//50  # Thickness of the marks
    # Distance from the edges of the squares to start drawing the marks
    SIDE_DIST = THIRD_WIDTH//5
    multiplier = 2

    # Loop through the board and draw the marks based on the player numbers
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw circle for player 1
                pygame.draw.circle(screen, COLOR_1, (int(col * THIRD_WIDTH + THIRD_WIDTH // 2), int(
                    row * THIRD_HEIGHT + THIRD_HEIGHT // 2)), int(WIDTH//3 // 2 - SIDE_DIST), THICK)
            elif board[row][col] == 2:
                # Draw lines to form an X for player 2
                pygame.draw.line(screen, COLOR_2, (col * THIRD_WIDTH + SIDE_DIST, row * THIRD_HEIGHT + SIDE_DIST), (col *
                                                                                                                    THIRD_WIDTH + THIRD_WIDTH - SIDE_DIST, row * THIRD_HEIGHT + THIRD_HEIGHT - SIDE_DIST), THICK * multiplier)
                pygame.draw.line(screen, COLOR_2, (col * THIRD_WIDTH - SIDE_DIST + THIRD_WIDTH, row * THIRD_HEIGHT + SIDE_DIST),
                                 (col * THIRD_WIDTH + SIDE_DIST, row * THIRD_HEIGHT + THIRD_HEIGHT - SIDE_DIST), THICK * multiplier)


def check_win(player):
    # Function to check if the current player has won
    player_1_win_sum = 3  # Sum value indicating player 1 has won
    player_2_win_sum = 6  # Sum value indicating player 2 has won

    # Check columns for win
    for col in range(BOARD_COLS):
        if np.min(board[:, col]) == 0:
            pass  # Skip if any square in the column is unmarked
        elif np.sum(board[:, col]) == player_1_win_sum or np.sum(board[:, col]) == player_2_win_sum:
            # Draw winning line if a win is detected
            draw_vertical_winning_line(col, player)
            return True

    # Check rows for win
    for row in range(BOARD_ROWS):
        if np.min(board[row, :]) == 0:
            pass  # Skip if any square in the row is unmarked
        elif np.sum(board[row, :]) == player_1_win_sum or np.sum(board[row, :]) == player_2_win_sum:
            # Draw winning line if a win is detected
            draw_horizontal_winning_line(row, player)
            return True

    # Check diagonals for win
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diag(player)  # Draw line for ascending diagonal win
        return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_des_diag(player)  # Draw line for descending diagonal win
        return True


def win_color(player):
    # Determine the color for the winning player
    if player == 2:
        color = (255, 255, 255)  # White for player 2
    else:
        color = (0, 0, 0)  # Black for player 1
    return color


def draw_asc_diag(player):
    # Draw ascending diagonal line
    SIDE_DIST = THIRD_WIDTH//8
    THICK = WIDTH//55
    pygame.draw.line(screen, win_color(player), (SIDE_DIST,
                                                 HEIGHT - SIDE_DIST), (WIDTH - SIDE_DIST, SIDE_DIST), THICK)


def draw_des_diag(player):
    # Draw descending diagonal line
    SIDE_DIST = THIRD_WIDTH//8
    THICK = WIDTH//55
    pygame.draw.line(screen, win_color(player), (SIDE_DIST, SIDE_DIST),
                     (WIDTH - SIDE_DIST, HEIGHT - SIDE_DIST), THICK)


def draw_vertical_winning_line(col, player):
    # Draw vertical line for column win
    SIDE_DIST = THIRD_WIDTH//8
    THICK = WIDTH//55
    pygame.draw.line(screen, win_color(player), (col * THIRD_WIDTH + THIRD_WIDTH // 2,
                                                 SIDE_DIST), (col * THIRD_WIDTH + THIRD_WIDTH // 2, HEIGHT - SIDE_DIST), THICK)


def draw_horizontal_winning_line(row, player):
    # Draw horizontal line for row win
    SIDE_DIST = THIRD_WIDTH//8
    THICK = WIDTH//55
    pygame.draw.line(screen, win_color(player), (SIDE_DIST, row * THIRD_HEIGHT + THIRD_HEIGHT //
                                                 2), (WIDTH - SIDE_DIST, row * THIRD_HEIGHT + THIRD_HEIGHT // 2), THICK)


def restart():
    # Reset the game to its initial state
    screen.fill(BG_COLOR)  # Clear the screen
    draw_lines(COLOR, HEIGHT, WIDTH, EDGE_POS=10)  # Redraw the grid lines
    player = 1  # Reset player to 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0  # Reset the board
    return player  # Return the starting player

    ##################### FUNCTIONS #####################


def main():
    player = 2  # Start with player 2
    GAME_OVER = False  # Flag to check if the game is over

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Quit the game if the close button is clicked

            if event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
                # Handle mouse clicks only if the game is not over
                # Get the X coordinate of the mouse click
                mouseX = event.pos[0]
                # Get the Y coordinate of the mouse click
                mouseY = event.pos[1]

                # Determine which square was clicked
                clicked_row = int(np.floor(mouseY / (WIDTH//3)))
                clicked_col = int(np.floor(mouseX / (HEIGHT//3)))

                if available_square(clicked_row, clicked_col):
                    # Mark the square for the current player if it's available
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()  # Draw the player's mark

                    if check_win(player):
                        GAME_OVER = True  # Set the game over flag if a win is detected

                    player = 1 if player == 2 else 2  # Switch to the other player

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game if the 'r' key is pressed
                    GAME_OVER = False
                    player = restart()  # Reset the game state

        pygame.display.update()  # Update the display with any changes

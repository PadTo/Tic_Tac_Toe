import sys
import pygame
import numpy as np
from constants import *


class TicTacToe:

    # Player 1: O
    # Player 2: X

    def __init__(self):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.THIRD_WIDTH = THIRD_WIDTH
        self.THIRD_HEIGHT = THIRD_HEIGHT

        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        self.board = board

        self.COLOR = COLOR
        self.BG_COLOR = BG_COLOR
        self.BLACK = BLACK

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(self.BG_COLOR)
        pygame.display.set_caption("Tic Tac Toe")

        self.player = 1
        self.GAME_OVER = False

        self.init_game()

    def init_game(self):
        try:
            image = pygame.image.load('MRTN.jpg')
            image.set_alpha(00)
            image_rect = image.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
            self.screen.blit(image, image_rect)
        except pygame.error:
            print(
                "Unable to load the image. Please ensure 'MRTN.jpg' is in the correct directory.")

        self.draw_lines(self.COLOR, self.HEIGHT, self.WIDTH, EDGE_POS=10)

    def draw_lines(self, color, HEIGHT, WIDTH, EDGE_POS=50):
        THICK = HEIGHT // 30
        inc_horz_line_pos = np.floor(HEIGHT / 3)
        inc_vert_line_pos = np.floor(WIDTH / 3)

        horz_pos = inc_horz_line_pos.copy()
        vert_pos = inc_vert_line_pos.copy()

        for i in range(0, 3):
            pygame.draw.line(self.screen, color, (EDGE_POS,
                             horz_pos), (WIDTH - EDGE_POS, horz_pos), THICK)
            pygame.draw.line(self.screen, color, (vert_pos, EDGE_POS),
                             (vert_pos, HEIGHT - EDGE_POS), THICK)
            horz_pos += inc_horz_line_pos
            vert_pos += inc_vert_line_pos

    def mark_square(self, row, col, player):
        self.board[row][col] = player

    def available_square(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row][col] == 0:
                    return False
        return True

    def draw_figures(self):
        THICK = WIDTH // 50
        SIDE_DIST = THIRD_WIDTH // 5
        multiplier = 2
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, (SAND), (int(col * self.THIRD_WIDTH + self.THIRD_WIDTH // 2), int(
                        row * self.THIRD_HEIGHT + self.THIRD_HEIGHT // 2)), int(self.WIDTH // 3 // 2 - SIDE_DIST), THICK)
                elif self.board[row][col] == 2:
                    pygame.draw.line(self.screen, (GRAY), (col * self.THIRD_WIDTH + SIDE_DIST, row * self.THIRD_HEIGHT + SIDE_DIST), (col *
                                     self.THIRD_WIDTH + self.THIRD_WIDTH - SIDE_DIST, row * self.THIRD_HEIGHT + self.THIRD_HEIGHT - SIDE_DIST), THICK * multiplier)
                    pygame.draw.line(self.screen, (GRAY), (col * self.THIRD_WIDTH - SIDE_DIST + self.THIRD_WIDTH, row * self.THIRD_HEIGHT + SIDE_DIST),
                                     (col * self.THIRD_WIDTH + SIDE_DIST, row * self.THIRD_HEIGHT + self.THIRD_HEIGHT - SIDE_DIST), THICK * multiplier)

    def check_win(self, player):
        player_1_win_sum = 3
        player_2_win_sum = 6
        for col in range(self.BOARD_COLS):
            if np.min(self.board[:, col]) == 0:
                continue
            if np.sum(self.board[:, col]) == player_1_win_sum or np.sum(self.board[:, col]) == player_2_win_sum:
                self.draw_vertical_winning_line(col, player)
                return True
        for row in range(self.BOARD_ROWS):
            if np.min(self.board[row, :]) == 0:
                continue
            if np.sum(self.board[row, :]) == player_1_win_sum or np.sum(self.board[row, :]) == player_2_win_sum:
                self.draw_horizontal_winning_line(row, player)
                return True
        if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player or self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.draw_diagonal_winning_line(player)
            return True
        return False

    def win_color(self, player):
        return (SAND) if player == 2 else (GRAY)

    def draw_vertical_winning_line(self, col, player):
        SIDE_DIST = self.THIRD_WIDTH // 8
        THICK = self.WIDTH // 55
        pygame.draw.line(self.screen, self.win_color(player), (col * self.THIRD_WIDTH + self.THIRD_WIDTH //
                         2, SIDE_DIST), (col * self.THIRD_WIDTH + self.THIRD_WIDTH // 2, self.HEIGHT - SIDE_DIST), THICK)

    def draw_horizontal_winning_line(self, row, player):
        SIDE_DIST = self.THIRD_WIDTH // 8
        THICK = self.WIDTH // 55
        pygame.draw.line(self.screen, self.win_color(player), (SIDE_DIST, row * self.THIRD_HEIGHT + self.THIRD_HEIGHT //
                         2), (self.WIDTH - SIDE_DIST, row * self.THIRD_HEIGHT + self.THIRD_HEIGHT // 2), THICK)

    def draw_diagonal_winning_line(self, player):
        SIDE_DIST = self.THIRD_WIDTH // 8
        THICK = self.WIDTH // 55
        if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            pygame.draw.line(self.screen, self.win_color(
                player), (SIDE_DIST, self.HEIGHT - SIDE_DIST), (self.WIDTH - SIDE_DIST, SIDE_DIST), THICK)
        elif self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            pygame.draw.line(self.screen, self.win_color(
                player), (SIDE_DIST, SIDE_DIST), (self.WIDTH - SIDE_DIST, self.HEIGHT - SIDE_DIST), THICK)

    def restart(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_lines(self.COLOR, self.HEIGHT, self.WIDTH, EDGE_POS=10)
        self.player = 1
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.GAME_OVER:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    clicked_row = int(mouseY // self.THIRD_HEIGHT)
                    clicked_col = int(mouseX // self.THIRD_WIDTH)
                    if self.available_square(clicked_row, clicked_col):
                        self.mark_square(clicked_row, clicked_col, self.player)
                        self.draw_figures()
                        if self.check_win(self.player):
                            self.GAME_OVER = True
                        self.player = 1 if self.player == 2 else 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.GAME_OVER = False
                        self.restart()

            pygame.display.update()


class AI:
    def __init__(self, level=0, player=2):
        self.level = level
        self.player = player

    def eval(self, main_board):
        pass

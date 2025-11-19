import pygame
import sys

# ----------------------
# Settings
# ----------------------
WIDTH, HEIGHT = 900, 900
CELL = WIDTH // 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 120, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic Tac Toe 3x3x3")
font = pygame.font.SysFont(None, 60)

# ----------------------
# Game data
# ----------------------
board_small = [[[ [None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
board_big = [[None for _ in range(3)] for _ in range(3)]
player = "X"
active_board = None
winner_big = None

# ----------------------
# Helpers
# ----------------------
def check_win_small(br, bc):
    b = board_small[br][bc]
    for r in range(3):
        if b[r][0] == b[r][1] == b[r][2] and b[r][0] is not None:
            return b[r][0]
    for c in range(3):
        if b[0][c] == b[1][c] == b[2][c] and b[0][c] is not None:
            return b[0][c]
    if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None:
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None:
        return b[0][2]
    return None


def check_big_win():
    B = board_big
    for r in range(3):
        if B[r][0] == B[r][1] == B[r][2] and B[r][0] is not None:
            return B[r][0]
    for c in range(3):
        if B[0][c] == B[1][c] == B[2][c] and B[0][c] is not None:
            return B[0][c]
    if B[0][0] == B[1][1] == B[2][2] and B[0][0] is not None:
        return B[0][0]
    if B[0][2] == B[1][1] == B[2][0] and B[0][2] is not None:
        return B[0][2]
    return None


def small_board_full(br, bc):
    return all(board_small[br][bc][r][c] is not None for r in range(3) for c in range(3))

# ----------------------
# Drawing
# ----------------------
def draw_board():
    screen.fill(WHITE)

    # highlight active board
    if active_board and not winner_big:
        ar, ac = active_board
        pygame.draw.rect(screen, (230, 240, 255), (ac * 3 * CELL, ar * 3 * CELL, 3 * CELL, 3 * CELL))

    # small grid lines
    for i in range(10):
        pygame.draw.line(screen, GRAY, (i * CELL, 0), (i * CELL, HEIGHT), 2)
        pygame.draw.line(screen, GRAY, (0, i * CELL), (WIDTH, i * CELL), 2)

    # big grid lines
    for i in range(4):
        pygame.draw.line(screen, BLACK, (i * 3 * CELL, 0), (i * 3 * CELL, HEIGHT), 7)
        pygame.draw.line(screen, BLACK, (0, i * 3 * CELL), (WIDTH, i * 3 * CELL), 7)

    # draw marks
    for br in range(3):
        for bc in range(3):
            for sr in range(3):
                for sc in range(3):
                    mark = board_small[br][bc][sr][sc]
                    if mark:
                        x = bc * 3 * CELL + sc * CELL + CELL // 2
                        y = br * 3 * CELL + sr * CELL + CELL // 2
                        color = BLUE if mark == "X" else RED
                        img = font.render(mark, True, color)
                        rect = img.get_rect(center=(x, y))
                        screen.blit(img, rect)

    # draw winners of big boards
    for br in range(3):
        for bc in range(3):
            w = board_big[br][bc]
            if w:
                x = bc * 3 * CELL + (3 * CELL) // 2
                y = br * 3 * CELL + (3 * CELL) // 2
                img = font.render(w, True, GREEN)
                rect = img.get_rect(center=(x, y))
                screen.blit(img, rect)

    # show winner
    if winner_big:
        text = font.render(f"Winner: {winner_big}!", True, BLACK)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

    pygame.display.flip()

# ----------------------
# Main loop
# ----------------------
running = True
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN and not winner_big:
            mx, my = event.pos
            big_c = mx // (3 * CELL)
            big_r = my // (3 * CELL)
            small_c = (mx % (3 * CELL)) // CELL
            small_r = (my % (3 * CELL)) // CELL

            if active_board and active_board != (big_r, big_c):
                break
            if board_small[big_r][big_c][small_r][small_c] is not None:
                break

            board_small[big_r][big_c][small_r][small_c] = player
            w = check_win_small(big_r, big_c)
            if w:
                board_big[big_r][big_c] = w

            nr, nc = small_r, small_c
            if small_board_full(nr, nc) or board_big[nr][nc] is not None:
                active_board = None
            else:
                active_board = (nr, nc)

            player = "O" if player == "X" else "X"

            winner_big = check_big_win()

pygame.quit()
sys.exit()
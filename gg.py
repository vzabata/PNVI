import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 640, 640
GRID_SIZE = 8
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32, bold=True)


# --- Load Images ---
def get_img(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))


# Replace these with your actual filenames
IMAGES = [get_img('circle.png'), get_img('triangle.png'), get_img('square.png'), get_img('stop.png')]


def create_board():
    board = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            while True:
                candy = random.randint(0, 3)
                if (c >= 2 and board[r][c - 1] == candy and board[r][c - 2] == candy) or \
                        (r >= 2 and board[r - 1][c] == candy and board[r - 2][c] == candy):
                    continue
                board[r][c] = candy
                break
    return board


def find_matches(board):
    to_rem = set()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if c < GRID_SIZE - 2 and board[r][c] == board[r][c + 1] == board[r][c + 2]:
                to_rem.update([(r, c), (r, c + 1), (r, c + 2)])
            if r < GRID_SIZE - 2 and board[r][c] == board[r + 1][c] == board[r + 2][c]:
                to_rem.update([(r, c), (r + 1, c), (r + 2, c)])
    return to_rem


def refill(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == -1:
                board[r][c] = random.randint(0, 3)


def draw(board, selected, score):
    screen.fill((255, 255, 255))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            screen.blit(IMAGES[board[r][c]], (c * TILE_SIZE, r * TILE_SIZE))

    if selected:  # Green border
        pygame.draw.rect(screen, (0, 255, 0), (selected[1] * TILE_SIZE, selected[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                         5)

    txt = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(txt, (15, 15))
    pygame.display.flip()


def main():
    board = create_board()
    score = 0
    selected = None

    # Draw immediately to prevent black screen
    draw(board, selected, score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                c, r = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE

                if not selected:
                    selected = (r, c)
                else:
                    r1, c1 = selected
                    # Check if adjacent
                    if abs(r1 - r) + abs(c1 - c) == 1:
                        board[r1][c1], board[r][c] = board[r][c], board[r1][c1]

                        matched = find_matches(board)
                        if matched:
                            score += 1  # Only +1 point for the successful move
                            while matched:
                                for mr, mc in matched: board[mr][mc] = -1
                                refill(board)
                                matched = find_matches(board)
                        else:
                            # Swap back if no match
                            board[r1][c1], board[r][c] = board[r][c], board[r1][c1]
                    selected = None

        draw(board, selected, score)
        clock.tick(FPS)


if __name__ == "__main__":
    main()

import pygame, sys

# --- CONFIG ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 60
GRID_COLS = 8
GRID_ROWS = 6
STATUS_BAR = 80
FPS = 30

# Colors
BLACK    = (0,    0,    0)
GRAY     = (150, 150, 150)
WHITE    = (255, 255, 255)
DARKGRAY = (50,  50,   50)
GREEN    = (0,   200,   0)
RED      = (200,   0,   0)
BLUE     = (0,   0,   200)

# --- LEVEL ---
LEVEL = [
    "........",
    ".T..T..E",
    "....T...",
    ".TT.....",
    ".S......",
    "........"
]

def parse_level():
    traps = set()
    start = exitp = None
    for r,row in enumerate(LEVEL):
        for c,ch in enumerate(row):
            if ch == "S": start = (c,r)
            if ch == "E": exitp = (c,r)
            if ch == "T": traps.add((c,r))
    return start, exitp, traps

def grid_origin():
    w = GRID_COLS * CELL_SIZE
    h = GRID_ROWS * CELL_SIZE
    return (WINDOW_WIDTH-w)//2, STATUS_BAR + (WINDOW_HEIGHT-STATUS_BAR-h)//2

def draw_board(screen, player):
    screen.fill(BLACK)
    pygame.draw.rect(screen, DARKGRAY, (0, 0, WINDOW_WIDTH, STATUS_BAR))

    gx, gy = grid_origin()

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(gx + c * CELL_SIZE, gy + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, DARKGRAY, rect, 1)

            if (c, r) == exitp:
                pygame.draw.rect(screen, BLUE, rect)

            if state == "REVEAL" and (c, r) in traps:
                pygame.draw.rect(screen, RED, rect)

            if (c, r) == tuple(player):
                player_rect = pygame.Rect(rect.x + 10, rect.y + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                pygame.draw.rect(screen, GREEN, player_rect)

    title_text = font.render("Trap Maze", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    moves_text = font.render(f"Moves: {moves}", True, WHITE)
    msg_text = font.render(message, True, WHITE)

    screen.blit(title_text, (20, 20))
    screen.blit(lives_text, (250, 20))
    screen.blit(moves_text, (450, 20))
    screen.blit(msg_text, (WINDOW_WIDTH//2 - msg_text.get_width() // 2, 100))


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
def main():
    global font, lives, moves, message, state, traps, exitp

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Trap Maze")
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 28)

    start, exitp, traps = parse_level()
    player = list(start)

    lives = 3
    moves = 0
    message = "Memorize traps!"
    reveal_start = pygame.time.get_ticks()
    REVEAL_MS = 2500
    hurt_time = 0
    state = "REVEAL"

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()

                if e.key == pygame.K_r:
                    return main()

                if state == "PLAY":
                    old = player.copy()

                    if e.key == pygame.K_UP:    player[1] -= 1
                    if e.key == pygame.K_DOWN:  player[1] += 1
                    if e.key == pygame.K_LEFT:  player[0] -= 1
                    if e.key == pygame.K_RIGHT: player[0] += 1

                    player[0] = max(0, min(GRID_COLS-1, player[0]))
                    player[1] = max(0, min(GRID_ROWS-1, player[1]))

                    if player != old:
                        moves += 1

                    if tuple(player) in traps:
                        lives -= 1
                        message = "You hit a trap!"
                        hurt_time = pygame.time.get_ticks()
                        state = "HURT"

                        if lives <= 0:
                            message = "GAME OVER"
                            state = "GAMEOVER"

                    if tuple(player) == exitp:
                        message = "YOU WIN!"
                        state = "WIN"

        if state == "REVEAL":
            if pygame.time.get_ticks() - reveal_start >= REVEAL_MS:
                state = "PLAY"
                message = "Go!"

        if state == "HURT":
            if pygame.time.get_ticks() - hurt_time >= 600:
                state = "PLAY"

        draw_board(screen, player)
        pygame.display.update()


if __name__ == "__main__":
    main()

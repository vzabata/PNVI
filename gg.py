import pygame
import random
import sys

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FPS = 60

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
BALL_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_SPEED = 10
BALL_SPEED_X = 6
BALL_SPEED_Y = 4
BALL_SPEED_INCREMENT = 0.6

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

def reset_ball():
    return WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, -BALL_SPEED_X, BALL_SPEED_Y


def draw_text(text, size, x, y):
    f = pygame.font.Font('freesansbold.ttf', size)
    surface = f.render(text, True, WHITE)
    rect = surface.get_rect(center=(x, y))
    window.blit(surface, rect)

def main():
    paddle_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2

    ball_x, ball_y, ball_dx, ball_dy = reset_ball()

    score = 0
    paused = False
    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_p and not game_over:
                    paused = not paused

                if event.key == pygame.K_r and game_over:
                    return main()

        keys = pygame.key.get_pressed()

        if not paused and not game_over:
            if keys[pygame.K_w] or keys[pygame.K_UP] and paddle_y > 0:
                paddle_y -= PADDLE_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN] and paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                paddle_y += PADDLE_SPEED

            ball_x += ball_dx
            ball_y += ball_dy

            if ball_y <= 0 or ball_y >= WINDOW_HEIGHT - BALL_SIZE:
                ball_dy = -ball_dy

            if ball_x >= WINDOW_WIDTH - BALL_SIZE:
                ball_dx = -ball_dx

            if (ball_x <= PADDLE_WIDTH and
                paddle_y < ball_y < paddle_y + PADDLE_HEIGHT):
                ball_dx = -ball_dx

                ball_dx *= 1.1
                ball_dy *= 1.1

                ball_dy += random.randint(-2, 2)

                score += 1

            if ball_x < -BALL_SIZE:
                game_over = True


        window.fill(BLACK)
        pygame.draw.rect(window, WHITE, (0, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(window, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
        draw_text(f"Score: {score}", 30, WINDOW_WIDTH - 100, 30)

        if paused:
            draw_text("PAUSED (Press P to Continue)", 40, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        if game_over:
            draw_text("GAME OVER", 60, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
            draw_text(f"Score: {score}", 40, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
            draw_text("Press R to Restart", 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70)

        pygame.display.update()


if __name__ == '__main__':
    main()

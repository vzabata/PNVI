import pygame
import random
import sys

WIDTH = 800
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()

spaceship_img = pygame.image.load("spaceship.png")
asteroid_img = pygame.image.load("asteroid.png")
crystal_img = pygame.image.load("energy_crystal.png")

background_music = "background_music.wav"
clash_sound = pygame.mixer.Sound("clash_sound.wav")

pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

spaceship_img = pygame.transform.scale(spaceship_img, (70, 70))
asteroid_img = pygame.transform.scale(asteroid_img, (80, 80))
crystal_img = pygame.transform.scale(crystal_img, (50, 50))

class Player:
    def __init__(self):
        self.image = spaceship_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        self.speed += 0.0008

    def draw(self):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, WHITE, self.rect, 1)


class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)   # small star pixels
        self.speed = 4

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))


class Asteroid:
    def __init__(self):
        self.image = asteroid_img
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH - 40), -100))
        self.hitbox = self.rect.inflate(-30, -30)

        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        self.hitbox.bottomleft = self.rect.bottomleft

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

class Crystal:
    def __init__(self):
        self.image = crystal_img
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), -40))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)
#        pygame.draw.rect(screen, WHITE, self.rect, 1)

def main():
    player = Player()
    asteroids = []
    crystals = []
    stars = [Star() for _ in range(260)]

    score = 0
    asteroid_timer = 0
    crystal_timer = 0

    running = True
    while running:
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        asteroid_timer += 1
        crystal_timer += 1

        if asteroid_timer > 50:
            asteroids.append(Asteroid())
            asteroid_timer = 0

        if crystal_timer > 90:
            crystals.append(Crystal())
            crystal_timer = 0

        player.update()

        for a in asteroids:
            a.update()
            if a.hitbox.colliderect(player.rect):
                clash_sound.play()
                return score

        for c in crystals:
            c.update()
            if c.rect.colliderect(player.rect):
                score += 1
                crystals.remove(c)



        asteroids = [a for a in asteroids if a.rect.y < HEIGHT + 100]
        crystals = [c for c in crystals if c.rect.y < HEIGHT + 100]

        # Draw
        screen.fill(BLACK)

        # Stars
        for s in stars:
            s.update()
            s.draw()

        player.draw()

        for a in asteroids:
            a.draw()
        for c in crystals:
            c.draw()

        font = pygame.font.SysFont("arial", 32)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

def game_over_screen(score):
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial", 32)

    while True:
        #screen.fill(BLACK)

        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 250))

        score_text = small_font.render(f"Your Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 350))

        restart_text = small_font.render("Press 'R' to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 430))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return


while True:
    score = main()
    game_over_screen(score)

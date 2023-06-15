import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 400, 600
SPEED = 5
GRAVITY = 1
FLAP_POWER = 15
BIRD_X = 50
PIPE_INTERVAL = 1600

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the pipe image
pipe_img = pygame.image.load('tree.png') # replace with your own image

class Bird:
    def __init__(self):
        self.y = HEIGHT / 2
        self.speed = 0

        # Load the bird images and set the bird's state to 0
        self.states = [pygame.image.load(f'bird{i}.png') for i in range(1, 4)]
        self.state = 0

    def flap(self):
        self.speed = -FLAP_POWER

    def move(self):
        self.speed += GRAVITY
        self.y += self.speed

        # Cycle through bird states
        self.state = (self.state + 1) % len(self.states)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - 100)

    def move(self):
        self.x -= SPEED

class Button:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, 200, 50)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        font = pygame.font.Font(None, 36)
        text_img = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_img, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

def run_game():
    bird = Bird()
    pipes = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.flap()

        if len(pipes) == 0 or pipes[-1].x < WIDTH - PIPE_INTERVAL:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.move()
            if pipe.x < -pipe_img.get_width():
                pipes.remove(pipe)

        bird.move()

        screen.fill((255, 255, 255))  # white background
        screen.blit(bird.states[bird.state], (BIRD_X, bird.y))
        for pipe in pipes:
            screen.blit(pipe_img, (pipe.x, pipe.height))

        pygame.display.flip()

        if bird.y < 0 or bird.y > HEIGHT:
            return
        for pipe in pipes:
            if pipe.x < BIRD_X + bird.states[bird.state].get_width() and pipe.x + pipe_img.get_width() > BIRD_X:
                if bird.y > pipe.height:
                    return

        pygame.time.wait(17)  # ~60 frames per second

def game_over_screen():
    restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 'Restart')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked():
                    return

        screen.fill((255, 255, 255))  # white background
        restart_button.draw(screen)

        pygame.display.flip()
        pygame.time.wait(17)  # ~60 frames per second

while True:
    run_game()
    game_over_screen()

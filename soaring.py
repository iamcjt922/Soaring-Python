# This small simple game was created as a method to show jr devs on my team how python can be utilized to create
# simple 2D games by utilizing pygame library. It is a simple clone of the very popular Flappy Bird game
# but with my own twist on the graphics and theme. This code is open source and you are free to use it how you like
# modify, copy, distribute or edit. While attribution is not required, it is greatly appreciated :). 
# Please ensure you have the proper installed libraries. If you don't then you can install them using the pip command.
# For example on mac in terminal you can type python3 -m pip install pygame

# I hope this helps some beginner game developers or just people in general curious about game creation using Python.
# Feel free to reach out to me at hello@iamcjt.com with any questions!

import pygame
import sys
import random

# Initializing Pygame library
pygame.init()

# Constants setup - use this to control attributes of the constants more comments below

#Size of the window created using pygame
WIDTH, HEIGHT = 400, 600

# How fast the game scrolls
SPEED = 5

# Determine how heavy the character is
GRAVITY = 1

# Speed at which the sprite goes up and down in accordance to the clicks
FLAP_POWER = 10 

BIRD_X = 50

#How often the pipes or in this case the "trees" appear on screen

PIPE_INTERVAL = 1600

# Draw the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the pipe/tree image
pipe_img = pygame.image.load('tree.png') # replace it with your own image as you please
restart_img = pygame.image.load('restart.png') # replace it with your own image as you please
start_button_img = pygame.image.load('start_button.png') # replace it with your own image as you please

class Bird:
    def __init__(self):
        self.y = HEIGHT / 2
        self.speed = 0
        self.animation_delay = 0  # delay counter for animation of the bird sprite, increase or decrease to add/subtract delay
        self.animation_speed = 5  # how many frames per animation state change

        # loads and sets the sprite image state to 0
        self.states = [pygame.image.load(f'bird{i}.png') for i in range(1, 4)]
        self.state = 0
        self.rect = self.states[self.state].get_rect(midleft=(BIRD_X, self.y))

    def flap(self):
        self.speed = -FLAP_POWER

    def move(self):
        self.speed += GRAVITY
        self.y += self.speed
        self.rect.center = (BIRD_X, self.y)

        # delays the animation update
        self.animation_delay += 1
        if self.animation_delay >= self.animation_speed:
            self.animation_delay = 0
            self.state = (self.state + 1) % len(self.states)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - pipe_img.get_height())
        self.passed = False

    def move(self):
        self.x -= SPEED

class Button:
    def __init__(self, x, y, image):
        self.rect = image.get_rect(center=(x, y))
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

def start_screen():
    logo_img = pygame.image.load('logo.png') # feel free to replace with your own logo
    logo_img = pygame.transform.scale(logo_img, (128, 128))  # uses pygame.transform to resize the logo
    copyright_text = "© 2023 Christian Tejada." # you can add your own copyright information here
    second_line_text = "Images from Freepik" #freepik attribution - required if you use freepiks images

    start_button = Button(WIDTH // 2, HEIGHT // 2 + 100, start_button_img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked():
                    return

        screen.fill((255, 255, 255))  # game background color, change as you'd like

        # draws logo on the splash screen
        logo_rect = logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(logo_img, logo_rect)

        # draws the copyright text on the splashscreen
        font = pygame.font.Font(None, 24)
        copyright_surf = font.render(copyright_text, True, (0, 0, 0))
        second_line_surf = font.render(second_line_text, True, (0, 0, 0))
        copyright_rect = copyright_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        second_line_rect = second_line_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(copyright_surf, copyright_rect)
        screen.blit(second_line_surf, second_line_rect)

        # draws start button
        start_button.draw(screen)

        pygame.display.flip()
        pygame.time.wait(17)  

def run_game():
    bird = Bird()
    pipes = []
    score = 0

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
            elif not pipe.passed and pipe.x + pipe_img.get_width() < bird.rect.centerx:
                pipe.passed = True
                score += 1

        bird.move()

        screen.fill((255, 255, 255))  # defines the background screen for the game
        screen.blit(bird.states[bird.state], (BIRD_X, bird.y))
        for pipe in pipes:
            screen.blit(pipe_img, (pipe.x, HEIGHT - pipe.height))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        if bird.y < 0 or bird.y > HEIGHT:
            return
        for pipe in pipes:
            pipe_rect = pipe_img.get_rect(topleft=(pipe.x, HEIGHT - pipe.height))
            if bird.rect.colliderect(pipe_rect):
                return

        pygame.time.wait(17) 

def game_over_screen():
    restart_button = Button(WIDTH // 2, HEIGHT // 2, restart_img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked():
                    return

        screen.fill((255, 255, 255))  # defines the background screen color for the "game over screen"
        restart_button.draw(screen)

        pygame.display.flip()
        pygame.time.wait(17)  

start_screen()
while True:
    run_game()
    game_over_screen()

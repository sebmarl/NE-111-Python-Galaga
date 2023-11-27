import pygame
import math

class Enemy:
    def __init__(self, screen, x, y, speed, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.angle = 0

    def draw(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.radius)

    def move(self):
        self.angle += self.speed
        self.x = self.screen.get_width() / 2 + self.radius * math.cos(self.angle)
        self.y = self.screen.get_height() / 2 + self.radius * math.sin(self.angle)

    def update(self):
        self.move()
        self.draw()

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Enemy')

enemy = Enemy(screen, 400, 300, 0.01, 20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 255))

    enemy.update()

    pygame.display.flip()
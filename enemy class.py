SM -Sebastian Marion-landais
import pygame
import math
import os 

class Enemy:
    zapdos = os.path.join(os.path.expanduser('~'), 'Desktop', 'downloads', 'zapdossprite.png')
    def __init__(self, screen, x, y, speed, radius, zapdos):
        
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.angle = 0
        self.image = pygame.image.load(zapdos)
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))

    def draw(self):
        self.screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def move(self):
        self.angle += self.speed
        self.x = self.screen.get_width() / 2 + self.radius * math.cos(self.angle)
        self.y = self.screen.get_height() / 2 + self.radius * math.sin(self.angle)

    def update(self):
        self.move()
        self.draw()


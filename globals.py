import pygame
import math
from pygame import Vector2 as v2

pygame.init()


class Circle:
    def __init__(self, pos: v2, radius: float) -> None:
        self.pos = pos
        self.radius = radius

    def collidepoint(self, point: v2):
        return math.dist(self.pos, point) <= self.radius


screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Smart Rockets")
height = screen.get_height()
width = screen.get_width()
center = pygame.Vector2(width / 2, height / 2)
frames = 200
max_rockets = 50
max_force = 0.04

font = pygame.font.SysFont(None, 48)

target = Circle(v2(center.x, 100), 40)

obstacle1 = pygame.Rect(50, 300, 500, 20)
obstacle2 = pygame.Rect(450, 700, 500, 20)

objects = []
# objects.extend([target, obstacle1, obstacle2])
objects.extend([target, obstacle1])

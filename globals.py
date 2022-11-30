import pygame
import math
from pygame import Vector2 as v2

pygame.init()


class Circle:
    def __init__(self, pos: v2, radius: float) -> None:
        self.pos = pos
        self.radius = radius

    def collidepoint(self, point: v2):
        return (point.x - self.pos.x) ** 2 + (point.y - self.pos.y) ** 2 < self.radius


def heading(v: pygame.Vector2):
    # if v.x > 0:
    #     if v.y > 0:
    #         return math.atan(v.y / v.x)
    #     if v.y < 0:
    #         return -math.atan(abs(v.y / v.x))
    #     return 0
    # if v.x < 0:
    #     if v.y > 0:
    #         return math.pi - math.atan(abs(v.y / v.x))
    #     if v.y < 0:
    #         return math.atan(abs(v.y / v.x)) - math.pi
    #     return math.pi
    # return math.pi / 2
    if v == v2(0, 0):
        return math.pi / 2
    return math.atan2(v.y, v.x)


screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Smart Rockets")
height = screen.get_height()
width = screen.get_width()
center = pygame.Vector2(width / 2, height / 2)
frames = 200
max_rockets = 250
max_force = 0.04

font = pygame.font.SysFont(None, 48)

target = Circle(v2(center.x, 100), 40)

obstacle1 = pygame.Rect(50, 300, 500, 20)
obstacle2 = pygame.Rect(450, 700, 500, 20)

objects = []
objects.extend([target, obstacle1, obstacle2])

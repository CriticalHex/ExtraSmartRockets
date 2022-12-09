import pygame  # game library
import math  # math stuff
from pygame import Vector2 as v2  # rename "pygame.Vector2" to v2
import random  # the random libary, generates random numbers

pygame.init()  # initialize pygame


class Circle:
    """A VERY rudimentary circle handler"""

    def __init__(self, pos: v2, radius: float) -> None:
        """Creates a circle at pos with radius radius"""
        self.pos = pos
        self.radius = radius

    def collidepoint(self, point: v2):
        """Circle collision, returns if the point provided is within the circle"""
        return math.dist(self.pos, point) <= self.radius


def rand(start: int, end: int, *, digits: int = 10):
    """Returns a random number between two numbers to a given amount of digits"""
    d = 10**digits  # a number with as many digits as specified
    s = random.randint(
        start * d, end * d
    )  # get a random number between the two numbers with as many digits as specified
    return s / d  # return that number scaled back down to starting values


def draw_text(text: str, pos: pygame.Vector2):
    """Draws provided string at provided position"""
    f = font.render(text, True, (0, 0, 255))  # create str drawable
    screen.blit(f, pos)  # draw str drawable to screen


screen = pygame.display.set_mode(
    (0, 0), pygame.FULLSCREEN
)  # define the screen to be fullscreen
pygame.display.set_caption("Smart Rockets")  # caption the screen
height = screen.get_height()  # global height value
width = screen.get_width()  # global width value
center = pygame.Vector2(width / 2, height / 2)  # global center value
frames = 400  # frames to run each generation for
max_rockets = 25  # rockets per generation
max_speed = 10  # max rocket speed

net_settings = [8, 4, 2]
# the inputs, hidden layers, nodes per hidden layer, and outputs of the AI

font = pygame.font.SysFont(None, 48)  # a font to use across all files

target = Circle(v2(center.x, 100), 40)  # the target circle object

obstacle1 = pygame.Rect(50, 300, 500, 20)  # obstacles to avoid
obstacle2 = pygame.Rect(450, 700, 500, 20)

objects: list[pygame.Rect | Circle] = []
objects.extend([target, obstacle1, obstacle2])
# objects.extend([target])  # create a list of things to collide with.

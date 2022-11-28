from math import dist
import pygame
from pygame import Vector2 as v2
import globals as g
from dna import DNA
from numpy import interp


class Rocket:
    def __init__(self, dna: DNA = None) -> None:
        self.flying = True
        self.hit_target = False

        self.pos = v2(g.center.x, g.height - 100)
        self.vel = v2(0, 0)
        self.acc = v2(0, 0)

        self.initial_dist = dist(self.pos, g.targetpos)
        # print(self.initial_dist)

        if not dna:
            self.dna = DNA()
        else:
            self.dna = dna

        self.score = 0
        self.hit_at = g.frames

        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.image.fill((pygame.Color(0, 0, 0, 0)))
        self.irect = pygame.Rect(0, 0, 50, 10)
        self.irect.center = self.image.get_rect().center
        pygame.draw.rect(self.image, (255, 255, 255), self.irect)
        self.rect = self.image.get_rect(center=(self.pos))

    def update(self, frame: int):
        if self.flying and not self.hit_target:
            self.collision(frame)
            self.acc += self.dna.genes[frame]
            self.accelerate()

    def accelerate(self):
        self.vel += self.acc
        self.pos += self.vel
        # if (x := self.vel.magnitude()) > 6:
        #     self.vel *= 6 / x
        # self.acc *= 0
        self.rect.center = self.pos

    def draw(self):
        image = pygame.transform.rotate(
            self.image, -g.math.degrees(g.heading(self.vel))
        )
        g.screen.blit(image, self.rect)

    def stop(self):
        self.flying = False
        self.image.set_alpha(100)

    def collision(self, frame: int):
        self.target_distance = dist(self.pos, g.targetpos)
        if self.target_distance <= g.targetrad:
            self.hit_target = True
            self.hit_at = frame
        if (
            (
                self.pos.y <= 0
                or self.pos.y >= g.height
                or self.pos.x <= 0
                or self.pos.x >= g.width
            )
            or (self.rect.colliderect(g.obstacle1))
            or (self.rect.colliderect(g.obstacle2))
            or self.hit_target
        ):
            self.stop()

    def eval(self):
        self.score = self.initial_dist / self.target_distance
        # self.score *= g.frames / self.hit_at
        if self.hit_target:
            self.score *= 20
        else:
            pass
            self.score /= 2

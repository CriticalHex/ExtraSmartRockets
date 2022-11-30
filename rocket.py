from math import dist, sin, cos, radians
import pygame
from pygame import Vector2 as v2
import globals as g
from dna import DNA
from numpy import interp, arange


def vectorize(point: v2, angle: float, distance: float):
    return v2(distance * cos(angle) + point.x, distance * sin(angle) + point.y)


def trace(start: v2, angle: float, resolution: float):
    line: list[v2] = []
    end = vectorize(start, angle, 1000)
    for i in arange(0, 1, resolution):
        p = point(start, end, i)
        line.append(p)
        if p.y <= 0 or p.y >= g.height or p.x <= 0 or p.x >= g.width:
            return 0, line
        for o in g.objects:
            if o.collidepoint(p):
                t = type(o)
                if t == g.Circle:
                    return 1, line
                if t == pygame.Rect:
                    return -1, line
    return 0, line


# def trace(start: v2, direction: v2, resolution: float):
#     line: list[v2] = []
#     if direction != v2(0, 0):
#         direction.normalize_ip()
#     end = start + (direction * 1000)
#     for i in arange(0, 1, resolution):
#         p = point(start, end, i)
#         line.append(p)
#         if p.y <= 0 or p.y >= g.height or p.x <= 0 or p.x >= g.width:
#             return 0, line
#         for o in g.objects:
#             if o.collidepoint(p):
#                 t = type(o)
#                 if t == g.Circle:
#                     return 1, line
#                 if t == pygame.Rect:
#                     return -1, line
#     return 0, line


def point(p1: v2, p2: v2, t: float):
    return v2(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)


class Rocket:
    def __init__(self, dna: DNA = None) -> None:
        self.flying = True
        self.hit_target = False

        self.pos = v2(g.center.x, g.height - 100)
        self.vel = v2(0, 0)
        self.acc = v2(0, 0)

        self.initial_dist = dist(self.pos, g.target.pos)
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
            self.look()
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
        if self.flying and not self.hit_target:
            self.draw_rays()

    def stop(self):
        self.flying = False
        self.image.set_alpha(100)

    def collision(self, frame: int):
        self.target_distance = dist(self.pos, g.target.pos)
        if self.target_distance <= g.target.radius:
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

    def look(self):
        self.looking1, self.line1 = trace(self.pos, g.heading(self.vel), 0.01)
        self.looking2, self.line2 = trace(
            self.pos, g.heading(self.vel) - radians(45), 0.01
        )
        self.looking0, self.line0 = trace(
            self.pos, g.heading(self.vel) + radians(45), 0.01
        )

        # self.looking1, self.line1 = trace(self.pos, self.vel, 0.01)
        # self.looking2, self.line2 = trace(
        #     self.pos,
        #     v2(
        #         self.vel.x * 0.7071 - self.vel.y * -0.7071,
        #         self.vel.x * -0.7071 + self.vel.y * 0.7071,
        #     ),
        #     0.01,
        # )
        # self.looking0, self.line0 = trace(
        #     self.pos,
        #     v2(
        #         self.vel.x * 0.7071 - self.vel.y * 0.7071,
        #         self.vel.x * 0.7071 + self.vel.y * 0.7071,
        #     ),
        #     0.01,
        # )

    def draw_rays(self):
        if len(self.line1) >= 2:
            pygame.draw.lines(
                pygame.display.get_surface(), (0, 255, 0), False, self.line1
            )
        if len(self.line2) >= 2:
            pygame.draw.lines(
                pygame.display.get_surface(), (0, 255, 0), False, self.line2
            )
        if len(self.line0) >= 2:
            pygame.draw.lines(
                pygame.display.get_surface(), (0, 255, 0), False, self.line0
            )

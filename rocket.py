from math import dist, sin, cos, radians, atan2, pi
import pygame
from pygame import Vector2 as v2
import globals as g
from neural import Network as Net
from numpy import arange

# from dna import DNA


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


"""def trace(start: v2, direction: v2, resolution: float):
    line: list[v2] = []
    if direction != v2(0, 0):
        direction.normalize_ip()
    end = start + (direction * 1000)
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
    return 0, line"""


def point(p1: v2, p2: v2, t: float):
    return v2(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)


def limit(val: float, min: float, max: float):
    if val > max:
        return max
    if val < min:
        return min
    return val


def setMag(v: v2, mag):
    if (m := v.magnitude()) != 0:
        return v * (mag / v.magnitude())
    return v


def heading(v: pygame.Vector2):
    """if v.x > 0:
        if v.y > 0:
            return math.atan(v.y / v.x)
        if v.y < 0:
            return -math.atan(abs(v.y / v.x))
        return 0
    if v.x < 0:
        if v.y > 0:
            return math.pi - math.atan(abs(v.y / v.x))
        if v.y < 0:
            return math.atan(abs(v.y / v.x)) - math.pi
        return math.pi
    return math.pi / 2"""
    if v == v2(0, 0):
        return pi / 2
    return atan2(v.y, v.x)


class Rocket:
    def __init__(self, net: Net = None) -> None:
        self.flying = True
        self.hit_target = False

        self.pos = v2(g.center.x, g.height - 100)
        self.vel = v2(0, -1)
        self.thrust = 0

        self.heading = heading(self.vel)

        self.initial_dist = dist(self.pos, g.target.pos)

        if not net:
            self.net = Net(7, 7, 2)
            # inputs:
            # x, y, 3 looking vars,
            # thrust (might be 3 later)
            # heading
            # arbitrary 7 hidden
            # outputs:
            # heading, thrust
        else:
            self.net = net

        self.score = 0
        self.hit_at = g.frames

        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.image.fill((pygame.Color(0, 0, 0, 0)))
        self.irect = pygame.Rect(0, 0, 50, 10)
        self.irect.center = self.image.get_rect().center
        pygame.draw.rect(self.image, (255, 255, 255), self.irect)
        self.rect = self.image.get_rect(center=(self.pos))

    def compile_inputs(self):
        # x, y, 3 looking vars, thrust, heading
        return [
            self.pos.x,
            self.pos.y,
            self.looking0,
            self.looking1,
            self.looking2,
            self.thrust,
            self.heading,
        ]

    def update(self, frame: int):
        if self.flying and not self.hit_target:
            self.heading = heading(self.vel)
            self.look()
            self.collision(frame)
            self.net.compute(self.compile_inputs())
            # output_values = [heading, thrust]
            self.heading += radians(self.net.output_values[0])
            self.thrust += self.net.output_values[1]
            self.thrust = limit(self.thrust, 0, 100)
            self.vel = setMag(self.vel, self.thrust)
            self.move()

    def move(self):
        self.pos += self.vel
        self.rect.center = self.pos

    def draw(self):
        image = pygame.transform.rotate(self.image, -g.math.degrees(self.heading))
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
            # or (self.rect.colliderect(g.obstacle2))
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
        res = 0.02
        self.looking1, self.line1 = trace(self.pos, self.heading, res)
        self.looking2, self.line2 = trace(self.pos, self.heading - radians(15), res)
        self.looking0, self.line0 = trace(self.pos, self.heading + radians(15), res)

        """self.looking1, self.line1 = trace(self.pos, self.vel, 0.01)
        self.looking2, self.line2 = trace(
            self.pos,
            v2(
                self.vel.x * 0.7071 - self.vel.y * -0.7071,
                self.vel.x * -0.7071 + self.vel.y * 0.7071,
            ),
            0.01,
        )
        self.looking0, self.line0 = trace(
            self.pos,
            v2(
                self.vel.x * 0.7071 - self.vel.y * 0.7071,
                self.vel.x * 0.7071 + self.vel.y * 0.7071,
            ),
            0.01,
        )"""

    def draw_rays(self):
        if len(self.line1) >= 2:
            if self.looking1 == 0:
                pygame.draw.lines(g.screen, pygame.Color(0, 0, 255), False, self.line1)
            elif self.looking1 == -1:
                pygame.draw.lines(g.screen, pygame.Color(255, 0, 0), False, self.line1)
            elif self.looking1 == 1:
                pygame.draw.lines(g.screen, pygame.Color(0, 255, 0), False, self.line1)
        if len(self.line2) >= 2:
            if self.looking2 == 0:
                pygame.draw.lines(g.screen, pygame.Color(0, 0, 255), False, self.line2)
            elif self.looking2 == -1:
                pygame.draw.lines(g.screen, pygame.Color(255, 0, 0), False, self.line2)
            elif self.looking2 == 1:
                pygame.draw.lines(g.screen, pygame.Color(0, 255, 0), False, self.line2)
        if len(self.line0) >= 2:
            if self.looking0 == 0:
                pygame.draw.lines(g.screen, pygame.Color(0, 0, 255), False, self.line0)
            elif self.looking0 == -1:
                pygame.draw.lines(g.screen, pygame.Color(255, 0, 0), False, self.line0)
            elif self.looking0 == 1:
                pygame.draw.lines(g.screen, pygame.Color(0, 255, 0), False, self.line0)

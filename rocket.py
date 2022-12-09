"""Rockets"""

import math  # all the math things used in this file
import pygame  # game library
from pygame import Vector2 as v2  # rename "pygame.Vector2" to v2
import globals as g  # things that files need access to
from neural import NeuralNetwork as Net  # the AI framework
from numpy import arange  # range but with floats


def vectorize(point: v2, angle: float, distance: float):
    """Return a point a provided angle and distance away from provided point"""
    return v2(
        distance * math.cos(angle) + point.x, distance * math.sin(angle) + point.y
    )


def trace(start: v2, angle: float, resolution: float):
    """Raytracing, returns what a line cast from a provided
    position at a provided angle across a provided distance,
    hits, and the points in the line, using a provided resolution"""
    line: list[v2] = []  # initialize the list of points in the line traced
    end = vectorize(
        start, angle, g.width
    )  # get the point that would be at the end of the desired ray
    for i in arange(0, 1, resolution):  # percentages at a resolution
        p = point(
            start, end, i
        )  # gets a point between start and end position at the i percentage
        line.append(p)  # put that point in the line
        if (
            p.y <= 0 or p.y >= g.height or p.x <= 0 or p.x >= g.width
        ):  # if hitting a wall
            return 0, line  # return a value and the line
        for o in g.objects:  # for all collidable objects
            if o.collidepoint(p):  # if the point hits one
                t = type(o)  # get the type of object hit
                if t == g.Circle:  # if its a circle (the target)
                    return 1, line  # return a value and the line
                if t == pygame.Rect:  # if its a rect (obstacle)
                    return -1, line  # return a value and the line
    return 0, line  # otherwise return the wall value and the line


def point(p1: v2, p2: v2, t: float):
    """return a point a percentage of the way between two points"""
    return v2(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)


def limit(val: float, min: float, max: float):
    """returns a limited val given a val and the
    numbers that val should be between"""
    if val > max:  # if the number's too big
        return max  # return the numbers max
    if val < min:  # if it's too small
        return min  # return its minimum value
    return val  # otherwise return the number


def setMag(v: v2, mag):
    "Sets a vectors magnitude"
    if (m := v.magnitude()) != 0:  # if the magnitude isn't zero
        return v * (mag / v.magnitude())  # set magnitude
    # I feel like this should be a different else
    # but I don't know enough about vectors
    return v  # otherise don't.


def heading(v: pygame.Vector2):
    """Return the angle a vector is facing"""
    if v == v2(0, 0):
        return math.pi / 2
    return math.atan2(v.y, v.x)


class Rocket:  # the rocket
    def __init__(self, net: Net = None) -> None:
        """Creates the rocket. Takes optional network,
        will be provided when rockets reproduce via the population class"""
        self.flying = True  # is the rocket flying or stopped
        self.hit_target = False  # did the rocket hit the target

        self.pos = v2(g.center.x, g.height - 100)  # rocket location
        self.thrust = 0  # a percentage of the rockets max speed
        self.speed = 0  # the rockets speed

        self.sup = 0  # temp counters for the AI instructions
        self.sdown = 0
        self.hup = 0
        self.hdown = 0

        self.heading = heading(
            v2(g.rand(-1, 1), g.rand(-1, 1))
        )  # direction the rocket is facing to start with

        # self.heading = heading(v2(0, 0))  # direction the rocket is facing to start with

        self.initial_dist = math.dist(
            self.pos, g.target.pos
        )  # how far the rocket is from the target.
        # Currently unused, was meant for the scoring function

        if not net:  # if not given a network, create a random one
            self.net = Net(*g.net_settings)  # using the global network settings
            # inputs: bias(1), x, y, look0, look1, look2, thrust, heading
            # outputs: heading, thrust
        else:
            self.net = net

        self.score = 0  # rocket score, determined at end of life
        self.hit_at = (
            g.frames
        )  # when the rocket hit the target, if ever (started at max frames)

        self.image = pygame.Surface(
            (100, 100), pygame.SRCALPHA
        )  # rocket image, 100x100, allowing for alpha values
        self.image.fill((pygame.Color(0, 0, 0, 0)))  # make the image transparent
        self.irect = pygame.Rect(0, 0, 50, 10)  # the rectangle to draw on the image
        self.irect.center = self.image.get_rect().center  # center the rect on the image
        pygame.draw.rect(
            self.image, (255, 255, 255), self.irect
        )  # draw the rect on the image
        self.rect = self.image.get_rect(
            center=(self.pos)
        )  # set rocket rect to the image rect,
        # and center the image rect on the player position

    def update(self, frame: int):
        """Determine rocket behaviour"""
        if self.flying and not self.hit_target:  # if flying and didn't hit the target
            self.look()  # raytraces
            self.collision(
                frame
            )  # checks collision, passes frame because if the target was hit,
            # the frame it was hit is recorded in self.hit_at
            self.net.forward_propagation(self.normalize_inputs())
            # run the AI to get instructions, output_values = [heading, thrust]
            self.heading += math.radians(
                self.net.final_outputs[0]
            )  # change heading based on AI output
            if self.heading >= 2 * math.pi:
                self.heading -= 2 * math.pi
            elif self.heading <= -2 * math.pi:
                self.heading += 2 * math.pi
            self.thrust += float(
                self.net.final_outputs[1]
            )  # change thrust based on AI output
            self.thrust = limit(self.thrust, 0, 100)  # limit thrust
            self.speed = g.max_speed * (self.thrust / 100)  # set speed
            self.move()  # move the rocket

    def move(self):
        """Move the rocket"""
        self.pos = vectorize(
            self.pos, self.heading, self.speed
        )  # get the position to move to based on the speed and direction facing
        self.rect.center = self.pos  # move the image to the player

    def draw(self):
        """Draw the rocket and its rays"""
        image = pygame.transform.rotate(
            self.image, -g.math.degrees(self.heading)
        )  # rotate the image to the way the rocket is facing
        g.screen.blit(image, self.rect)  # draw the image on the screen
        if self.flying and not self.hit_target:  # if flying
            self.draw_rays()  # draw the rays
        # g.draw_text(str(self.score),(0,g.height - 50))

    def stop(self):
        """What to do when the rocket stops"""
        self.flying = False  # rocket is no longer flying
        self.image.set_alpha(100)  # make the image less opaque

    def collision(self, frame: int):
        """Determines if the rocket is hitting anything"""
        self.target_distance = math.dist(
            self.pos, g.target.pos
        )  # distance from the target
        if (
            self.target_distance <= g.target.radius
        ):  # if the distance to the target is less than the targets radius,
            # the rocket is hitting the target
            self.hit_target = True  # hit the target
            self.hit_at = frame  # when it hit the target
        if (
            (
                self.pos.y <= 0
                or self.pos.y >= g.height
                or self.pos.x <= 0
                or self.pos.x >= g.width
            )  # hitting the wall
            or (self.rect.colliderect(g.obstacle1)) #hitting an obstacle
            or (self.rect.colliderect(g.obstacle2))
            or self.hit_target  # hit the target
        ):
            self.stop()  # stop the rocket

    def eval(self):
        """Determines the rockets score at end of life"""
        self.score = self.initial_dist / self.target_distance
        if self.hit_target:
            self.score *= 20
        # invert distance to target to mean being closer is better
        # if self.looking0 == 1:
        #     self.score += 1
        # if self.looking1 == 1:
        #     self.score += 1
        # if self.looking2 == 1:
        #     self.score += 1

    def look(self):
        """Calcuate rays and what they're hitting"""
        res = 0.01  # resolution of the ray
        self.looking1, self.line1 = trace(
            self.pos, self.heading, res
        )  # in front of the rocket
        self.looking2, self.line2 = trace(
            self.pos, self.heading - math.radians(15), res
        )  # 15 degrees right
        self.looking0, self.line0 = trace(
            self.pos, self.heading + math.radians(15), res
        )  # 15 degrees left of center

    def draw_rays(self):
        """Draws rays, colored based on what the ray is seeing."""
        if len(self.line1) >= 2:
            if self.looking1 == 0:
                color = (0, 0, 255)
            elif self.looking1 == -1:
                color = (255, 0, 0)
            elif self.looking1 == 1:
                color = (0, 255, 0)
            pygame.draw.lines(g.screen, color, False, self.line1)
        if len(self.line2) >= 2:
            if self.looking2 == 0:
                color = (0, 0, 255)
            elif self.looking2 == -1:
                color = (255, 0, 0)
            elif self.looking2 == 1:
                color = (0, 255, 0)
            pygame.draw.lines(g.screen, color, False, self.line2)
        if len(self.line0) >= 2:
            if self.looking0 == 0:
                color = (0, 0, 255)
            elif self.looking0 == -1:
                color = (255, 0, 0)
            elif self.looking0 == 1:
                color = (0, 255, 0)
            pygame.draw.lines(g.screen, color, False, self.line0)

    def normalize_inputs(self):
        return [
            1,
            self.pos.x / g.width,
            self.pos.y / g.height,
            self.looking0,
            self.looking1,
            self.looking2,
            self.thrust / 100,
            self.heading / (2 * math.pi),
        ]

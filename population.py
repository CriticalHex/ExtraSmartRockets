import globals as g
from rocket import Rocket
import random
from neural import Network as Net
import pygame


def draw_text(text: str, pos: tuple[int, int]):
    font = g.font.render(text, True, (0, 0, 255))
    g.screen.blit(font, (pos[0] - font.get_width(), pos[1]))


class Population:
    def __init__(self) -> None:
        self.generations = 0
        self.font = g.font.render(f"Generations: {self.generations}", True, (0, 0, 255))
        self.rockets: list[Rocket] = []
        self.repro_pool: list[Rocket] = []
        for _ in range(g.max_rockets):
            self.rockets.append(Rocket())

    def reproduce(self):
        self.normalize_scores()
        for r in self.rockets:
            #r.net.mutate(r.hit_target)
            select = 0
            selector = random.random()
            while selector > 0:
                selector -= self.rockets[select].score
                select += 1
            select -= 1
            self.repro_pool.append(self.rockets[select])
        new_rockets = []
        for r in self.repro_pool:
            # mid = random.randrange(0, g.frames)
            # p1 = self.repro_pool[random.randrange(0, g.max_rockets)]
            # p2 = self.repro_pool[random.randrange(0, g.max_rockets)]
            new_net = Net(7, 4, 7, 2)
            # new_net.genes.clear()
            # new_net.genes.extend(p1.net.genes[0:mid])
            # new_net.genes.extend(p2.net.genes[mid : g.frames])
            new_rockets.append(Rocket(new_net))
        self.repro_pool.clear()
        self.rockets = new_rockets

    def update(self, frame: int):
        if frame == g.frames - 1:
            self.generations += 1
            self.font = g.font.render(
                f"Generations: {self.generations}", True, (0, 0, 255)
            )
            for r in self.rockets:
                r.eval()
            self.reproduce()
        for r in self.rockets:
            r.update(frame)

    def draw(self):
        g.screen.blit(self.font, (0, 0))
        for r in self.rockets:
            draw_text(f"sup: {r.sup}", (100, g.height - 40))
            draw_text(f"sdown: {r.sdown}", (300, g.height - 40))
            draw_text(f"hup: {r.hup}", (500, g.height - 40))
            draw_text(f"hdown: {r.hdown}", (700, g.height - 40))
            draw_text(f"Speed: {r.speed}", (g.width, 0))
            r.draw()

    def normalize_scores(self):
        total = 0
        for r in self.rockets:
            total += r.score
        for r in self.rockets:
            r.score /= total
            # print(r.score)

import globals as g  # globals
from rocket import Rocket  # rocket class
import random  # random number generation
from neural import Network as Net  # AI Class
import pygame  # game libary if necessary


class Population:
    """Handles all the rockets and their AI"""

    def __init__(self) -> None:
        """Creates a population"""
        self.hit = 0  # how many rockets hit the target
        self.generations = 0  # which iteration is this generation on
        self.gen_text = g.font.render(
            f"Generations: {self.generations}", True, (0, 0, 255)
        )  # text to display the generation
        self.hit_text = g.font.render(
            f"Hit last generation: {self.hit}", True, (0, 0, 255)
        )  # text to display the amount of rockets that hit the target
        self.rockets: list[Rocket] = []  # the populations current rockets
        self.repro_pool: list[Rocket] = []  # filled with rockets that did the best
        for _ in range(g.max_rockets):
            self.rockets.append(Rocket())  # create the rockets

    def reproduce(self):
        """Creates the next generation of rockets.

        All the rocket scores are normalized, meaning
        they're scaled to a value between 0 and 1,
        based on how well they all did. The best rocket would
        have a value of nearly 1 (I think), and the worst would
        have a value of 0 (I think). The reproduction pool is
        then filled such that if you were to pick a random rocket
        from the pool, the chance that you get any one rocket is
        equal to its normalized score (I think)."""
        self.normalize_scores()
        for r in self.rockets:  # mutate net and add the rocket to the gene pool
            r.net.mutate()
            selector = random.random()
            select = 0
            while selector > 0:
                selector -= self.rockets[select].score
                select += 1
            select -= 1
            self.repro_pool.append(self.rockets[select])
        new_rockets = []
        for r in self.repro_pool:
            new_net = self.create_net(r)
            new_rockets.append(Rocket(new_net))
        self.repro_pool.clear()
        self.rockets = new_rockets

    def update(self, frame: int):
        if frame == g.frames - 1:
            self.generations += 1
            self.gen_text = g.font.render(
                f"Generations: {self.generations}", True, (0, 0, 255)
            )
            self.hit = 0
            for r in self.rockets:
                if r.hit_target:
                    self.hit += 1
                r.eval()
            self.hit_text = g.font.render(
                f"Hit last generation: {self.hit}", True, (0, 0, 255)
            )
            self.reproduce()
        for r in self.rockets:
            r.update(frame)

    def draw(self):
        g.screen.blit(self.gen_text, (0, 0))
        g.screen.blit(self.hit_text, (0, self.gen_text.get_height() - 1))
        for r in self.rockets:
            # draw_text(f"sup: {r.sup}", (100, g.height - 40))
            # draw_text(f"sdown: {r.sdown}", (300, g.height - 40))
            # draw_text(f"hup: {r.hup}", (500, g.height - 40))
            # draw_text(f"hdown: {r.hdown}", (700, g.height - 40))
            # draw_text(f"Speed: {r.speed}", (g.width, 0))
            r.draw()

    def normalize_scores(self):
        total = max([i.score for i in self.rockets])
        # for r in self.rockets:
        #     total += r.score
        for r in self.rockets:
            r.score /= total

    def create_net(self, r: Rocket):
        new_net = Net(*g.net_settings)
        p1 = self.repro_pool[random.randrange(0, g.max_rockets)]
        p2 = self.repro_pool[random.randrange(0, g.max_rockets)]
        for i, layer in enumerate(r.net.hidden_layers):
            for j, node in enumerate(layer):
                mid = random.randrange(0, len(node.weights))
                new_net.hidden_layers[i][j].weights.clear()
                new_net.hidden_layers[i][j].weights.extend(
                    p1.net.hidden_layers[i][j].weights[0:mid]
                )
                new_net.hidden_layers[i][j].weights.extend(
                    p2.net.hidden_layers[i][j].weights[mid : len(node.weights)]
                )
        for i, node in enumerate(r.net.output_nodes):
            mid = random.randrange(0, len(node.weights))
            new_net.output_nodes[i].weights.clear()
            new_net.output_nodes[i].weights.extend(
                p1.net.output_nodes[i].weights[0:mid]
            )
            new_net.output_nodes[i].weights.extend(
                p2.net.output_nodes[i].weights[mid : len(node.weights)]
            )
        return new_net

    # def create_net(self, r: Rocket):
    #     new_net = Net(*g.net_settings)
    #     p1 = self.repro_pool[random.randrange(0, g.max_rockets)]
    #     new_net = p1.net
    #     return new_net

    def purge(self, frame):
        if frame > 100:
            for r in self.rockets:
                if r.pos.y > 800:
                    r.stop()
                    r.score = 0

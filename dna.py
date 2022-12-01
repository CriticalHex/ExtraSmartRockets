from pygame import Vector2 as v2
import random
import globals as g


def ra():
    vec = v2(random.randint(-1, 1), random.randint(-1, 1))
    if (x := vec.magnitude()) > g.max_speed:
        return vec * (g.max_speed / x)
    return vec


class DNA:
    def __init__(self) -> None:
        self.genes: list[v2] = []
        for _ in range(g.frames):
            self.genes.append(ra())

    def mutate(self, hit: bool):
        if hit:
            chance = 0.001
        else:
            chance = 0.1
        new_genes = []
        for i in range(g.frames):
            if random.random() <= chance:
                new_genes.append(ra())
            else:
                new_genes.append(self.genes[i])
        self.genes = new_genes

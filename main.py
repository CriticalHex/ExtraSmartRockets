import pygame
from population import Population
import globals as g
import cProfile


def draw_text(text: str, pos: pygame.Vector2):
    font = g.font.render(text, True, (0, 0, 255))
    g.screen.blit(font, pos)


def main():
    mouse = g.target.pos
    current_frame = 0
    population = Population()
    clock = pygame.time.Clock()
    speed = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.Vector2(*pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                g.target.pos = mouse
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                running = False
            if keys[pygame.K_LSHIFT]:
                population = Population()
            if keys[pygame.K_SPACE]:
                pass
            if keys[pygame.K_UP]:
                speed = 100
            if keys[pygame.K_DOWN]:
                speed = 1

        population.update(current_frame)

        if current_frame % speed == 0:
            clock.tick(60)
            g.screen.fill((0, 0, 0))
            pygame.draw.circle(g.screen, (0, 255, 0), g.target.pos, g.target.radius)
            pygame.draw.rect(g.screen, (255, 0, 0), g.obstacle1)
            # pygame.draw.rect(g.screen, (255, 0, 0), g.obstacle2)
            population.draw()
            pygame.display.flip()

        current_frame += 1
        current_frame %= g.frames
    pygame.quit()


if __name__ == "__main__":
    # cProfile.run("main()", sort="time")
    main()

import pygame  # game library
from population import Population  # manages all rockets
import globals as g  # things that files need access to
import cProfile  # for optimization


def main():
    mouse = g.target.pos  # where the mouse is (not actually at the target position)
    current_frame = 0  # for gauging how long a generation has been alive
    population = Population()  # all the rockets and their handling
    clock = pygame.time.Clock()  # for framerate limiting
    speed = 1  # simulation speed
    running = True  # program running state
    while running:  # while program is running
        for event in pygame.event.get():  # process all events per frame
            if event.type == pygame.MOUSEMOTION:  # if mouse moves
                mouse = pygame.Vector2(*pygame.mouse.get_pos())  # get mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:  # if clicking
                g.target.pos = mouse  # move the target to the mouse position
            if event.type == pygame.QUIT:  # if window closed
                running = False  # set program running state to not running
            keys = pygame.key.get_pressed()  # get pressed keys
            if keys[pygame.K_LCTRL]:  # if left ctrl pressed
                running = False  # set program running state to not running
            if keys[pygame.K_LSHIFT]:  # if left shift pressed
                population = Population()  # restart population
            if keys[pygame.K_SPACE]:
                pass
            if keys[pygame.K_UP]:  # if up arrow is pressed
                speed = 100  # speed up simulation (draw less)
            if keys[pygame.K_DOWN]:  # if down arrow is pressed
                speed = 1  # slow down simulation (draw every frame)

        population.update(
            current_frame
        )  # perform all calculations, move rockets, handle reproduction

        if current_frame % speed == 0:  # determine if program should draw
            clock.tick(60)  # limits framerate to 60 fps
            g.screen.fill((0, 0, 0))  # cover screen in black
            pygame.draw.circle(
                g.screen, (0, 255, 0), g.target.pos, g.target.radius
            )  # draw the target
            # pygame.draw.rect(g.screen, (255, 0, 0), g.obstacle1)  # draw obstacles
            # pygame.draw.rect(g.screen, (255, 0, 0), g.obstacle2) # ^^^
            population.draw()  # draw all the rockets and debug info
            pygame.display.flip()  # update screen

        current_frame += 1  # count frames elapsed
        current_frame %= g.frames  # reset to zero when the count hits a max
        # population.purge(current_frame)
    pygame.quit()  # close the window


if __name__ == "__main__":  # if this file was the one ran
    # cProfile.run("main()", sort="time") # time all things ran
    main()  # run main

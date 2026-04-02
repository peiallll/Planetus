import pygame as pg
import random as r

from settings import settings as s 
from physics.body import Body
from graphics.renderer import Renderer

run_once = True
body_list = []

renderer = Renderer()

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True

    while running:
        screen.fill((0,0,0))
        dt = clock.get_time() / 1000

        renderer.draw_background(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    body_list.append(Body(
                        r.randint(0, WIDTH),
                        r.randint(0, HEIGHT),
                        0,
                        0,
                        5,
                        8,
                        (r.randint(0,255),r.randint(0,255),r.randint(0,255))
                    ))
                    print(body_list)

        # rest of updating simulation here

        pg.display.flip()
        clock.tick(s.FPS)

    pg.quit()

if __name__ == "__main__":
    main()
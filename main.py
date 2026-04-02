import pygame as pg
import random as r

from settings import settings as s 

run_once = True

star_pos = []

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True

    while running:
        screen.fill((0,0,0))

        for x in range(150):
            new_point = [r.randint(0, WIDTH), r.randint(0, HEIGHT)]
            star_pos.append(new_point)
            
            pg.draw.circle(screen, (255, 255, 255), (star_pos[x]), 1, width=0)

        dt = clock.get_time() / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # rest of updating simulation here

        pg.display.flip()
        clock.tick(s.FPS)

    pg.quit()

if __name__ == "__main__":
    main()
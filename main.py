import pygame as pg

from settings import settings as s 

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True
    
    while running:
        dt = clock.get_time() / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # rest of updating simulation here

        screen.fill((0,0,0))
        pg.display.flip()
        clock.tick(s.FPS)

    pg.quit()

if __name__ == "__main__":
    main()
import pygame as pg
import random as r

from settings import settings as s 
from physics.body import Body
from graphics.renderer import Renderer
from physics.simulation import Simulation

renderer = Renderer()
simulation = Simulation()

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True

    current_mass = 5000

    while running:
        screen.fill((0,0,0))
        dt = clock.tick(s.FPS) / 1000

        renderer.draw_background(screen)
        renderer.draw_bodies(screen, simulation.bodies)

        keys = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    simulation.add_random_body()
                    print(simulation.bodies)

                if event.key == pg.K_SPACE:
                    simulation.toggle_pause()
                    
        if keys[pg.K_UP]:
            simulation.adjust_mass(10000)
        if keys[pg.K_DOWN]:
            simulation.adjust_mass(-10000)

        simulation.update(dt)

        renderer.draw_background(screen)
        renderer.draw_bodies(screen, simulation.bodies)

        renderer.draw_mass_text(screen, simulation.current_mass)
        renderer.enable_paused_text(screen, simulation.paused_text)

        pg.display.flip()
        clock.tick(s.FPS)

    pg.quit()

if __name__ == "__main__":
    main()
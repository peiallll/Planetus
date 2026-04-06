import pygame as pg
import pygame_widgets
from pygame_widgets.button import Button
import random as r

from settings import settings as s 
from physics.body import Body
from graphics.renderer import Renderer
from physics.simulation import Simulation

renderer = Renderer()
simulation = Simulation()

dotted_button = None
option = 1
arrow_enabled = True
btn_font = pg.font.SysFont('Arial', 20)

def toggle_trail():
    global option
    option += 1
    if option > 3:
        option = 1

    if option == 1:
        simulation.trail_enabled = True
        simulation.trail_decider_value = 1
        dotted_button.setText("SOLID")
    elif option == 2:
        simulation.trail_enabled = True
        simulation.trail_decider_value = 10
        dotted_button.setText("DOTTED")
    elif option == 3:
        simulation.trail_enabled = False
        dotted_button.setText("NO TRAIL")       

def toggle_arrow():
    simulation.arrow_enabled = not simulation.arrow_enabled
    if simulation.arrow_enabled:
        arrow_button.setText("ENABLED")
    else:
        arrow_button.setText("DISABLED")

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True

    drawing_line = False

    global dotted_button
    global arrow_button
    dotted_button = Button(screen, 10, 10, 100, 40, text='SOLID', font=btn_font, onClick=toggle_trail)
    arrow_button = Button(screen, 10, 60, 100, 40, text='ENABLED', font=btn_font, onClick=toggle_arrow)
    

    while running:
        screen.fill((0,0,0))
        dt = clock.tick(s.FPS) / 1000

        keys = pg.key.get_pressed()
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    if drawing_line:
                        continue        
                    drawing_line = True
                    simulation.add_random_body()
                    print(simulation.bodies)

                if event.key == pg.K_x:
                    simulation.bodies.clear()

                if event.key == pg.K_SPACE:
                    if drawing_line:
                        continue
                    simulation.toggle_pause()

                if event.key == pg.K_LSHIFT:
                    simulation.sim_speed = min(100, simulation.sim_speed + 1)
                if event.key == pg.K_LCTRL:
                    simulation.sim_speed = max(1, simulation.sim_speed - 1)
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if simulation.current_body:
                        drawing_line = False
                        simulation.current_body = None

        if keys[pg.K_UP]:
            simulation.adjust_mass(50)
        if keys[pg.K_DOWN]:
            simulation.adjust_mass(-50)

        if len(simulation.bodies) > 0:
            simulation.update(dt)

        renderer.draw_bodies(screen, simulation.bodies)
        renderer.draw_background(screen, simulation.sim_speed)
        renderer.draw_bodies(screen, simulation.bodies)
        renderer.draw_body_trail(screen, simulation.bodies)

        if not drawing_line and simulation.arrow_enabled:
            renderer.draw_direction_arrow(screen, simulation.bodies)

        if drawing_line and simulation.current_body:
            simulation.set_inital_velocity(simulation.current_body)
            ghost_path = simulation.ghost_orbit(simulation.current_body)

            if simulation.current_body_initial_velocity > 0:
                renderer.draw_ghost_orbit(screen, ghost_path) 

            renderer.draw_line(screen, simulation.current_body, simulation.current_body_initial_velocity)

        renderer.draw_mass_text(screen, simulation.current_mass)
        renderer.enable_paused_text(screen, simulation.paused_text)

        pygame_widgets.update(events) 
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()
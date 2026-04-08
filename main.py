import pygame as pg
import pygame_widgets
from pygame_widgets.button import ButtonArray
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

def trail_type():
    global option
    option += 1
    if option > 3:
        option = 1

    dotted_button = buttonArray.buttons[0] 

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
    arrow_button = buttonArray.buttons[1]

    simulation.arrow_enabled = not simulation.arrow_enabled
    if simulation.arrow_enabled:
        arrow_button.textColour = (0,200,0)
        arrow_button.setText("ENABLED")
    else:
        arrow_button.textColour = (200,0,0)
        arrow_button.setText("DISABLED")

def reset_time():
    simulation.elapsed_time = 0

def clear_bodies():
    simulation.bodies.clear()

def main():
    pg.init()

    WIDTH, HEIGHT = s.WIDTH, s.HEIGHT
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Planetus")

    clock = pg.time.Clock()
    running = True

    drawing_line = False
    drawing_ruler = False

    global buttonArray
    buttonArray = ButtonArray(
        screen, 10, 10, 150, 200, (1, 4), seperationThickness=50,
        colour = (0,0,0),
        texts=('SOLID', 'ENABLED', 'RESET TIME', 'CLEAR BODIES'),
        onClicks = (trail_type, toggle_arrow, reset_time, clear_bodies),
    )

    while running:
        screen.fill((0,0,0))
        dt = clock.tick(s.FPS) / 1000
        
        fps = int(clock.get_fps())

        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
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
                    drawing_ruler = True
                    start_place = event.pos
                    if simulation.current_body:
                        drawing_line = False
                        simulation.current_body = None

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing_ruler = False

        if keys[pg.K_UP]:
            simulation.adjust_mass(50)
        if keys[pg.K_DOWN]:
            simulation.adjust_mass(-50)

        if drawing_ruler and start_place and not drawing_line:
            mouse_x, mouse_y = pg.mouse.get_pos()
            ruler_length = simulation.ruler_length(start_place[0], mouse_x, start_place[1], mouse_y)
            renderer.draw_ruler(screen, start_place[0], start_place[1], mouse_x, mouse_y, ruler_length)

        if len(simulation.bodies) > 0:
            simulation.update(dt)

        renderer.draw_bodies(screen, simulation.bodies)
        renderer.draw_background(screen, simulation.sim_speed, fps, simulation.get_time(dt))
        renderer.draw_bodies(screen, simulation.bodies)
        renderer.draw_body_trail(screen, simulation.bodies)

        if not drawing_line and simulation.arrow_enabled:
            renderer.draw_direction_arrow(screen, simulation.bodies)

        if drawing_line and simulation.current_body:
            simulation.set_inital_velocity(simulation.current_body)
            ghost_path = simulation.ghost_orbit()

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
import pygame

import application_elements
import ui_elements
import camera_elements
import world_elements

WIDTH = 1920
HEIGHT = 1080


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # window size
    pygame.display.set_caption("Dinasty View")  # title
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("graphics\\alagard.ttf", 15)
    title_font = pygame.font.Font("graphics\\alagard.ttf", 25)

    # initialize camera and mouse position
    camera = camera_elements.Camera(0, 0, 9)
    mouse_x = 0
    mouse_y = 0

    # initialize basic tree ui
    texts_in_screen = []
    buttons_in_screen = []
    node_tree = ui_elements.NodeTree()

    #
    zoom_factor = 1.0
    worldmap = world_elements.WorldMap("graphics/worldmap.png")
    #
    application = application_elements.Application()
    dinasty_view_mode = application_elements.DinastyViewMode(WIDTH, HEIGHT, title_font)
    worldmap_view_mode = application_elements.WorldMapMode(WIDTH, HEIGHT, title_font)
    menu_mode = application_elements.MenuMode(WIDTH, HEIGHT, title_font)
    creation_mode = application_elements.CreationMode(WIDTH, HEIGHT, title_font)
    application.set_mode(menu_mode)

    running = True
    while running:
        clock.tick(120)  # FPS

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # close window
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if application.mode is not menu_mode:
                        texts_in_screen.clear()
                        buttons_in_screen.clear()
                        application.set_mode(menu_mode)
                    else:
                        running = False
                if application.mode is menu_mode:
                    menu_mode.controls()
                elif application.mode is creation_mode:
                    creation_mode.controls(event)
                elif application.mode is dinasty_view_mode:
                    dinasty_view_mode.controls(event, texts_in_screen, camera)
                elif application.mode is worldmap_view_mode:
                    worldmap_view_mode.controls()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        # keys for camera movement
        camera.move(keys)

        screen.fill('black')
        if application.mode is menu_mode:
            menu_mode.view(screen, texts_in_screen, buttons_in_screen)
        elif application.mode is creation_mode:
            creation_mode.view(screen, texts_in_screen, buttons_in_screen, mouse_x, mouse_y, game_font)
        elif application.mode is dinasty_view_mode:
            dinasty_view_mode.view(screen, texts_in_screen, camera, game_font, node_tree, mouse_x, mouse_y)
        elif application.mode is worldmap_view_mode:
            screen.fill(pygame.Color(0, 8, 20))
            # WORLDMAP
            worldmap.update(camera)
            worldmap.draw(screen)

        for text in texts_in_screen:
            text.draw(screen)

        for button in buttons_in_screen:
            if button.collidepoint((mouse_x, mouse_y)):
                button.color_background = "gray"
            else:
                button.color_background = "white"

            if button.collidepoint((mouse_x, mouse_y)) and pygame.mouse.get_pressed()[0]:
                if button.text == "Generate random World":
                    dinasty_view_mode.char, dinasty_view_mode.world = button.action()
                    buttons_in_screen.clear()
                    texts_in_screen.clear()
                    application.set_mode(dinasty_view_mode)
                elif button.text == "Custom World":
                    dinasty_view_mode.char, dinasty_view_mode.world = button.action()
                    buttons_in_screen.clear()
                    texts_in_screen.clear()
                    application.set_mode(dinasty_view_mode)
                else:
                    button.action()
                    break
            button.render()
            button.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()

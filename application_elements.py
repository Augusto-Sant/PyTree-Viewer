import pygame
import world_elements
import string
import ui_elements
import character_elements


class Application:
    def __init__(self):
        self.mode = None

    def set_mode(self, mode):
        if self.mode:
            self.mode.exit()
        self.mode = mode
        self.mode.enter()


class ApplicationMode:
    def __init__(self, width, height, font):
        self.name = None
        self.texts = []
        self.buttons = []
        self.width = width
        self.height = height
        self.font = font

    def create_texts(self):
        pass

    def create_buttons(self):
        pass

    def enter(self):
        self.create_texts()
        self.create_buttons()
        print(f'entered {self.name}')

    def exit(self):
        self.texts.clear()
        self.buttons.clear()
        print(f'exited {self.name}')


class MenuMode(ApplicationMode):
    def __init__(self, width, height, font):
        super().__init__(width, height, font)
        self.name = "menu_mode"

    def generate_random_world(self):
        world = world_elements.World("names.txt", "surnames.txt")
        world.generate_random_world_characters(200, 980, 8)

        # initialize first char for tree view
        id_char_searched = 74
        char = world.world_characters[id_char_searched]
        node_searched = None

        return char, world

    def generate_custom_world(self):
        world = world_elements.World("names.txt", "surnames.txt")
        aegon_i = character_elements.Character(world.id_generator.get_next_id(), "Aegon", "male", "Targaryen")
        aegon_i.set_genetics("pink", "white", "purple")
        aegon_i.beard = False
        maegor = character_elements.Character(world.id_generator.get_next_id(), "Maegor", "male", "Targaryen",
                                              father=aegon_i)
        aegon_i.children.append(maegor)
        maegor.set_genetics("pink", "white", "purple")
        for x in [aegon_i, maegor]:
            world.add_character(x)
        char = world.world_characters[0]
        return char, world

    def create_buttons(self):
        generate_button = ui_elements.Button((self.width // 2 - 195, 200), 400, 30, "Generate random World", self.font,
                                             self.generate_random_world)
        custom_world_button = ui_elements.Button((self.width // 2 - 195, 300), 400, 30, "Custom World", self.font,
                                                 self.generate_custom_world)
        self.buttons.append(generate_button)
        self.buttons.append(custom_world_button)

    def create_texts(self):
        title_menu = ui_elements.TextScreen("MENU", (self.width // 2, 50), self.font, 'white')
        self.texts.append(title_menu)

    def view(self, screen, texts_in_screen, buttons_in_screen):
        for button in self.buttons:
            button.render()
            if button not in buttons_in_screen:
                buttons_in_screen.append(button)

        for text in self.texts:
            if text not in texts_in_screen:
                texts_in_screen.append(text)

    def controls(self):
        pass


class CreationMode(ApplicationMode):
    def __init__(self, width, height, font):
        super().__init__(width, height, font)
        self.name = "creation_mode"
        self.letters_input = []
        self.new_characters_names = []
        self.new_name_word_limit = 30

    def create_buttons(self):
        accept_button = ui_elements.Button((self.width // 2, 300), 400, 30, "Add", self.font, None)
        accept_button.action = self.add_new_name
        self.buttons.append(accept_button)

    def create_texts(self):
        create_world_text = ui_elements.TextScreen("Create World", (self.width // 2, 50), self.font, "white")
        self.texts.append(create_world_text)
        text_new_character = ui_elements.TextScreen("New Founder Character (example: William McDonut)",
                                                    (self.width // 2, 150), self.font, "white")
        self.texts.append(text_new_character)

    def view(self, screen, texts_in_screen, buttons_in_screen, mouse_x, mouse_y, game_font):

        new_name_character = ui_elements.TextScreen("".join(self.letters_input), (self.width // 2, 175), self.font,
                                                    "white")
        new_name_character.background_color = "gray"
        new_name_character.draw(screen)
        count_characters = ui_elements.TextScreen(str(len(self.new_characters_names)), ((self.width // 2 + 100), 50),
                                                  self.font, "red")
        count_characters.draw(screen)
        for text in self.texts:
            if text not in texts_in_screen:
                texts_in_screen.append(text)

        for button in self.buttons:
            button.render()
            if button not in buttons_in_screen:
                buttons_in_screen.append(button)

    def add_new_name(self):
        new_name = "".join(self.letters_input)
        self.new_characters_names.append(f'{new_name}')
        self.letters_input.clear()

    def controls(self, event):
        if event.key == pygame.K_BACKSPACE:
            if len(self.letters_input) > 0:
                self.letters_input.pop()

        if len(self.letters_input) < self.new_name_word_limit:
            if event.unicode in string.ascii_letters or event.key == pygame.K_SPACE:
                self.letters_input.append(event.unicode)


class DinastyViewMode(ApplicationMode):
    def __init__(self, width, height, font):
        super().__init__(width, height, font)
        self.name = "dinasty_view_mode"
        self.world = None
        self.char = None
        self.node_searched = None

        # direct_* dinasty_* all_*
        self.tree_mode = "dinasty_tree"

    def create_texts(self):
        char_name = ui_elements.TextScreen(self.char.name, (0 + (len(self.char.name) * 10), 50), self.font, 'white')
        self.texts.append(char_name)
        control_instruction_text = ui_elements.TextScreen(
            "(e) to view Direct Tree   (d) to view Dinasty Tree   (a) to view All",
            (self.width // 2, 1080 - 100),
            self.font, pygame.Color(52, 58, 64, 126))
        self.texts.append(control_instruction_text)

    def view(self, screen, texts_in_screen, camera, game_font,
             node_tree, mouse_x, mouse_y):
        for text in self.texts:
            if text not in texts_in_screen:
                texts_in_screen.append(text)

        if self.tree_mode == "dinasty_tree":
            node_tree.tree = self.char.dinasty_tree()
            draw_lines = True
        elif self.tree_mode == "direct_tree":
            node_tree.tree = self.char.direct_ancestors_tree()
            draw_lines = True
        elif self.tree_mode == "all_tree":
            node_tree.tree = self.world.all_characters_tree()
            draw_lines = False

        nodes = node_tree.draw_tree(self.char, game_font, screen, camera, draw_lines)

        # see if mouse clicked one of the nodes in tree view
        for node in nodes:
            if node.circle_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                # change char to the one correspondent to the node clicked on
                self.char = node.character
                self.node_searched = node
                break

    def controls(self, event, texts_in_screen, camera):
        if event.key == pygame.K_d:
            self.tree_mode = "dinasty_tree"
            texts_in_screen.clear()
            self.texts.clear()
            self.create_texts()
            self.texts.append(ui_elements.TextScreen("Dinasty Tree", (960, 50), self.font, 'white'))
            self.texts.append(
                ui_elements.TextScreen(f"{self.char.surname}", (760, 50), self.font, pygame.Color(214, 40, 40)))
            camera.reset()
            if self.node_searched is not None:
                camera.position_x = self.node_searched.position[0]
                camera.position_y = self.node_searched.position[1]
        elif event.key == pygame.K_e:
            self.tree_mode = "direct_tree"
            texts_in_screen.clear()
            self.texts.clear()
            self.create_texts()
            self.texts.append(ui_elements.TextScreen("Direct Tree", (960, 50), self.font, 'white'))
            camera.reset()
            if self.node_searched is not None:
                camera.position_x = self.node_searched.position[0]
                camera.position_y = self.node_searched.position[1]
        elif event.key == pygame.K_a:
            self.tree_mode = "all_tree"
            texts_in_screen.clear()
            self.texts.clear()
            self.create_texts()
            self.texts.append(ui_elements.TextScreen("All Tree", (960, 50), self.font, 'white'))
            camera.reset()
            if self.node_searched is not None:
                camera.position_x = self.node_searched.position[0]
                camera.position_y = self.node_searched.position[1]


class WorldMapMode(ApplicationMode):
    def __init__(self, width, height, font):
        super().__init__(width, height, font)
        self.name = "worldmap_view_mode"

    def controls(self):
        pass

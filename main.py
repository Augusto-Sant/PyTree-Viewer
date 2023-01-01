import random
from character import Character, all_characters
from textUtils import Node, TextScreen
import pygame
import math

WIDTH = 1920
HEIGHT = 1080


class WorldMap:
    def __init__(self, filename):
        # Load the image
        self.image = pygame.image.load(filename)

        # Get the size of the image
        self.rect = self.image.get_rect()

        # Set the position of the image
        self.rect.x = 0
        self.rect.y = 0

    def update(self, camera):
        self.rect.x = 0 - camera.position_x
        self.rect.y = 0 - camera.position_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class IdGenerator:
    def __init__(self):
        self.id = -1

    def get_next_id(self):
        self.id += 1
        return self.id


def read_names(path):
    with open(path, "r", encoding='UTF-8') as file:
        lines = file.readlines()
    male_names = []
    female_names = []
    is_male = True
    for line in lines:
        if line.strip() == '@':
            is_male = False
        else:
            if is_male:
                male_names.append(line.strip())
            else:
                female_names.append(line.strip())
    names = [male_names, female_names]
    return names


def read_surnames(path):
    with open(path, 'r', encoding="UTF-8") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines


def draw_tree(tree_list, character_chosen, font, screen, camera_x, camera_y, draw_lines=True):
    # camera x and y for offset of objects after camera movement
    position_y = (HEIGHT // 2) - 150 - camera_y
    position_x = 200 - camera_x
    color = 'white'
    space = 300
    nodes = []

    for level in reversed(tree_list):
        max_value_length = len(max(tree_list.values(), key=len))

        i = 0
        for character in tree_list[level]:
            if i == 0:
                initial_space = max_value_length - len(tree_list[level])
                position_x += (initial_space * 130)

            circle_color = pygame.Color(0, 48, 73)
            if character is character_chosen:
                circle_color = pygame.Color(108, 117, 125)
            elif character.gender == 'female':
                circle_color = pygame.Color(95, 15, 64)
            else:
                circle_color = pygame.Color(0, 48, 73)

            node = Node(character, (position_x, position_y), font, color,
                        character.children, circle_color=circle_color)

            nodes.append(node)

            position_x += len(node.character.name) + space
            i += 1

        position_x = 200 - camera_x
        position_y += 200

    for node in nodes:
        if draw_lines is True:
            node_children = find_node_children(node, nodes)

            for child_node in node_children:
                line_color = pygame.Color(52, 58, 64, 126)
                pygame.draw.line(screen, line_color, node.position, child_node.position)

        node.draw(screen)

    # return to get nodes positions
    return nodes


def find_node_children(node, nodes):
    node_children = []
    # find the correspondent nodes of each character children
    if len(node.character.children) != 0:
        for child in node.character.children:
            for node_2 in nodes:
                if node_2.character is child:
                    node_children.append(node_2)
    return node_children


def create_founders(world_characters, names, surnames, id_generator):
    pairs_of_founders = 10
    for i in range(pairs_of_founders):
        # read names 0 male 1 female
        new_male_founder = Character(id_generator.get_next_id(), random.choice(names[0]), 'male',
                                     random.choice(surnames))
        new_female_founder = Character(id_generator.get_next_id(), random.choice(names[1]), 'female',
                                       random.choice(surnames))
        new_male_founder.spouse = new_female_founder
        new_female_founder.spouse = new_male_founder
        world_characters.append(new_male_founder)
        world_characters.append(new_female_founder)


def marry_event(world_characters, character):
    for character2 in world_characters:
        if (character2.gender != character.gender and character2.spouse is None
                and character.surname != character2.surname
                and (character2.father != character.father and character2.mother != character.mother)):
            character.spouse = character2
            character2.spouse = character


def generate_world_characters(years_to_pass, chance_to_marry, num_children_cap):
    # read names 0 male 1 female
    names = read_names("names.txt")
    surnames = read_surnames("surnames.txt")

    # characters in world
    id_generator = IdGenerator()
    world_characters = []
    create_founders(world_characters, names, surnames, id_generator)

    for i in range(years_to_pass):
        for character in world_characters:
            chance = random.randint(0, 1000)
            if character.alive:
                character.age += 1
                if chance + character.age > 1090:
                    character.alive = False
                    if character.spouse is not None:
                        character.spouse.spouse = None
                        character.spouse = None
                elif chance > chance_to_marry and character.spouse is not None and len(
                        character.children) < num_children_cap and len(character.spouse.children) < num_children_cap:
                    child = character.add_child(names, id_generator)
                    world_characters.append(child)
                elif chance > chance_to_marry and character.spouse is None:
                    marry_event(world_characters, character)

    # checks to see if any character in world has wrong id_key
    for i, character in enumerate(world_characters):
        if i != character.id_key:
            print(f'error {i} != {character.id_key}')
            break
        else:
            pass

    return world_characters


class Camera:
    def __init__(self, position_x, position_y, speed):
        self.position_x = position_x
        self.position_y = position_y
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.position_x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.position_x += self.speed
        elif keys[pygame.K_DOWN]:
            self.position_y += self.speed
        elif keys[pygame.K_UP]:
            self.position_y -= self.speed

    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.speed = 5


def main():
    world_characters = generate_world_characters(years_to_pass=400, chance_to_marry=980, num_children_cap=8)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # window size
    pygame.display.set_caption("Dinasty View")  # title
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("graphics\\alagard.ttf", 15)
    title_font = pygame.font.Font("graphics\\alagard.ttf", 25)

    # initialize camera and mouse position
    camera = Camera(0, 0, 9)
    mouse_x = 0
    mouse_y = 0

    # initialize first char for tree view
    id_char_searched = 74
    char = world_characters[id_char_searched]
    node_searched = None

    # initialize basic tree ui
    texts_in_screen = []
    dinasty_tree = True
    direct_tree = False
    all_tree = False
    #
    zoom_factor = 1.0
    worldmap = WorldMap("graphics/worldmap.png")
    #
    in_dinasty_view = True

    running = True
    while running:
        clock.tick(120)  # FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # close window
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:
                    if in_dinasty_view is True:
                        in_dinasty_view = False
                    else:
                        in_dinasty_view = True
                if in_dinasty_view:
                    if event.key == pygame.K_d:
                        texts_in_screen.clear()
                        dinasty_tree = True
                        direct_tree = False
                        all_tree = False
                        texts_in_screen.append(TextScreen("Dinasty Tree", (960, 50), title_font, 'white'))
                        texts_in_screen.append(
                            TextScreen(f"{char.surname}", (760, 50), title_font, pygame.Color(214, 40, 40)))
                        camera.reset()
                        if node_searched is not None:
                            camera.position_x = node_searched.position[0]
                            camera.position_y = node_searched.position[1]
                    elif event.key == pygame.K_e:
                        texts_in_screen.clear()
                        dinasty_tree = False
                        direct_tree = True
                        all_tree = False
                        texts_in_screen.append(TextScreen("Direct Tree", (960, 50), title_font, 'white'))
                        camera.reset()
                        if node_searched is not None:
                            camera.position_x = node_searched.position[0]
                            camera.position_y = node_searched.position[1]
                    elif event.key == pygame.K_a:
                        texts_in_screen.clear()
                        dinasty_tree = False
                        direct_tree = False
                        all_tree = True
                        texts_in_screen.append(TextScreen("All Tree", (960, 50), title_font, 'white'))
                        camera.reset()
                        if node_searched is not None:
                            camera.position_x = node_searched.position[0]
                            camera.position_y = node_searched.position[1]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        # keys for camera movement
        camera.move(keys)

        char = world_characters[id_char_searched]

        if in_dinasty_view:
            screen.fill('black')
            # DINASTY VIEW MODE
            char_name = TextScreen(char.name, (0 + (len(char.name) * 10), 50), title_font, 'white')
            char_name.draw(screen)
            control = TextScreen("(e) to view Direct Tree   (d) to view Dinasty Tree   (a) to view All",
                                 (WIDTH // 2, HEIGHT - 100),
                                 title_font, pygame.Color(52, 58, 64, 126))
            control.draw(screen)

            for text in texts_in_screen:
                text.draw(screen)

            if dinasty_tree:
                tree = char.dinasty()
                draw_lines = True
            elif direct_tree:
                tree = char.direct_ancestors()
                draw_lines = True
            elif all_tree:
                tree = all_characters(world_characters)
                draw_lines = False

            nodes = draw_tree(tree, char, game_font, screen, camera.position_x, camera.position_y, draw_lines)

            # see if mouse clicked one of the nodes in tree view
            for node in nodes:
                if node.circle_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    # change char to the one correspondent to the node clicked on
                    id_char_searched = node.character.id_key
                    node_searched = node
                    break
        else:
            screen.fill(pygame.Color(0, 8, 20))
            # MAIN GAME MODE
            worldmap.update(camera)
            worldmap.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()

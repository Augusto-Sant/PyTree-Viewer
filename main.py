import random
from character import Character
from textUtils import Node, TextScreen
import sys
import pygame

WIDTH = 1920
HEIGHT = 1080


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


def draw_tree(tree_list, font, screen):
    position_y = (HEIGHT//2)-150
    position_x = 200
    color = 'white'
    space = 200
    nodes = []

    for level in reversed(tree_list):
        max_value_length = len(max(tree_list.values(), key=len))

        i = 0
        for character in tree_list[level]:
            if i == 0:
                initial_space = max_value_length - len(tree_list[level])
                position_x += (initial_space * 130)

            node = Node(character, (position_x, position_y), font, color,
                        character.children)
            nodes.append(node)

            position_x += len(node.character.name) + space
            i += 1

        position_x = 200
        position_y += 50

    for node in nodes:
        node_children = []
        # find the correspondent nodes of each character children
        if len(node.character.children) != 0:
            for child in node.character.children:
                for node_2 in nodes:
                    if node_2.character is child:
                        node_children.append(node_2)

        for child_node in node_children:
            line_color = pygame.Color(214, 40, 40)
            pygame.draw.line(screen, line_color, node.position, child_node.position)

        node.draw(screen)


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
        if character2.gender != character.gender and character2.spouse is None:
            character.spouse = character2
            character2.spouse = character


def main():
    # read names 0 male 1 female
    names = read_names("names.txt")
    surnames = read_surnames("surnames.txt")
    # characters in world
    id_generator = IdGenerator()
    world_characters = []
    create_founders(world_characters, names, surnames, id_generator)
    # simulate world
    YEARS_TO_PASS = 100
    for i in range(YEARS_TO_PASS):
        for character in world_characters:
            chance = random.randint(0, 1000)
            if chance > 980 and character.spouse is not None:
                child = character.add_child(names, id_generator)
                world_characters.append(child)
            elif chance > 980 and character.spouse is None:
                marry_event(world_characters, character)

    for i, character in enumerate(world_characters):
        if i != character.id_key:
            print(f'erro {i} != {character.id_key}')
            print("!!")
            break
        else:
            print(character.id_key, character)

    # see detail
    # while True:
    #     choice = int(input(">:"))
    #     char = world_characters[choice]
    #     print(char)
    #     subchoice = int(input("? 1 direct 2 patrilineal (0 to exit): "))
    #     if subchoice == 1:
    #         print("-- DIRECT LINEAGE --")
    #         tree = char.direct_ancestors()
    #         print_tree(tree)
    #     elif subchoice == 2:
    #         print("-- DINASTY LINEAGE -- ")
    #         # tree = char.dinasty()
    #         print_tree(tree)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # TAMANHO JANELA
    pygame.display.set_caption("Dinasty View")  # TITULO
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("graphics\\alagard.ttf", 15)
    title_font = pygame.font.Font("graphics\\alagard.ttf", 25)

    texts_in_screen = []
    dinasty_tree = True
    direct_tree = False
    running = True
    while running:
        clock.tick(5)  # FPS

        # close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_d:
                    texts_in_screen.clear()
                    dinasty_tree = True
                    direct_tree = False
                    texts_in_screen.append(TextScreen("Dinasty Tree", (960, 50), title_font, 'white'))
                elif event.key == pygame.K_a:
                    texts_in_screen.clear()
                    dinasty_tree = False
                    direct_tree = True
                    texts_in_screen.append(TextScreen("Direct Tree", (960, 50), title_font, 'white'))

        screen.fill('black')
        char = world_characters[74]
        char_name = TextScreen(char.name, (0+(len(char.name)*10), 50), title_font, 'white')
        char_name.draw(screen)

        for text in texts_in_screen:
            text.draw(screen)

        if dinasty_tree:
            tree = char.dinasty()
        elif direct_tree:
            tree = char.direct_ancestors()

        draw_tree(tree, game_font, screen)

        pygame.display.update()


if __name__ == "__main__":
    main()

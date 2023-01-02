import pygame
import random
import character_elements


class IdGenerator:
    def __init__(self):
        self.id = -1

    def get_next_id(self):
        self.id += 1
        return self.id


class World:
    def __init__(self, names_path, surnames_path):
        self.world_characters = []
        self.names = []
        self.surnames = []
        self.read_names(names_path)
        self.read_surnames(surnames_path)

    def add_character(self, character):
        self.world_characters.append(character)

    def remove_character(self, character):
        for character_inside in self.world_characters:
            if character is character_inside:
                self.world_characters.remove(character)

    def all_characters_tree(self):
        all_chars = {}
        for character in self.world_characters:
            if character.father is None:
                character_elements.search_all_characters(character, all_chars, 0)

        changed_all_chars = {}
        for i, level in enumerate(reversed(all_chars)):
            changed_all_chars[i] = all_chars[level]

        return changed_all_chars

    def create_random_founders(self, id_generator, pairs_of_founders):
        for i in range(pairs_of_founders):
            # read names 0 male 1 female
            new_male_founder = character_elements.Character(id_generator.get_next_id(), random.choice(self.names[0]),
                                                            'male',
                                                            random.choice(self.surnames))
            new_female_founder = character_elements.Character(id_generator.get_next_id(), random.choice(self.names[1]),
                                                              'female',
                                                              random.choice(self.surnames))
            new_male_founder.spouse = new_female_founder
            new_female_founder.spouse = new_male_founder
            self.add_character(new_male_founder)
            self.add_character(new_female_founder)

        self.check_ids_characters()

    def generate_random_world_characters(self, years_to_pass, chance_to_marry, num_children_cap):
        # characters in world
        id_generator = IdGenerator()
        self.create_random_founders(id_generator, 10)

        for i in range(years_to_pass):
            for character in self.world_characters:
                chance = random.randint(0, 1000)
                if character.alive:
                    character.age += 1
                    if chance + character.age > 1090:
                        character.alive = False
                        if character.spouse is not None:
                            character.spouse.spouse = None
                            character.spouse = None
                    elif (chance > chance_to_marry and character.spouse is not None and len(
                            character.children) < num_children_cap and len(
                            character.spouse.children) < num_children_cap):
                        child = character.add_child(self.names, id_generator)
                        self.add_character(child)
                    elif chance > chance_to_marry and character.spouse is None:
                        self.marry_event(character)

        self.check_ids_characters()

    def check_ids_characters(self):
        # checks to see if any character in world has wrong id_key
        for i, character in enumerate(self.world_characters):
            if i != character.id_key:
                print(f'error {i} != {character.id_key}')
                break
            else:
                pass

    def marry_event(self, character):
        for character2 in self.world_characters:
            if (character2.gender != character.gender and character2.spouse is None
                    and character.surname != character2.surname
                    and (character2.father != character.father and character2.mother != character.mother)):
                character.spouse = character2
                character2.spouse = character

    def read_names(self, path):
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
        self.names = names

    def read_surnames(self, path):
        with open(path, 'r', encoding="UTF-8") as file:
            lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        self.surnames = lines


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

import random
import pygame


class Character:
    def __init__(self, id_key, name, gender, surname, father=None, mother=None, spouse=None):
        self.id_key = id_key
        self.name = name
        self.gender = gender
        self.surname = surname
        self.father = father
        self.mother = mother
        self.spouse = spouse
        self.children = []
        self.age = 0
        self.alive = True
        self.skin_color = random.choice(["brown", "white", "pink", "pardo"])
        self.hair_color = random.choice(["black", "brown", "blonde"])
        if self.gender == 'male':
            self.beard = random.choice([True, False])
            self.hair = random.choice([True, False])
        else:
            self.beard = False
            self.hair = True
        self.eye_color = random.choice(["blue", "green", "brown"])
        self.clothing_color = random.choice(["cyan", "purple", "red"])

        # images
        self.base_image = None
        self.eyes_image = None
        self.hair_image = None
        self.clothing_image = None
        self.beard_image = None
        self.set_images()

    def set_genetics(self, skin_color, hair_color, eye_color):
        self.skin_color = skin_color
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.set_images()

    def set_images(self):
        base_image_path = f'graphics/appearances/{self.skin_color}_skin.png'
        beard_image_path = f'graphics/appearances/{self.hair_color}_beard.png'
        if self.gender == 'male':
            hair_image_path = f'graphics/appearances/{self.hair_color}_hair.png'
        else:
            hair_image_path = f'graphics/appearances/{self.hair_color}_female_hair.png'

        eyes_image_path = f'graphics/appearances/{self.eye_color}_eyes.png'
        clothing_image_path = f'graphics/appearances/{self.clothing_color}_clothing.png'

        self.base_image = pygame.image.load(base_image_path)
        self.eyes_image = pygame.image.load(eyes_image_path)
        self.clothing_image = pygame.image.load(clothing_image_path)
        if self.hair:
            self.hair_image = pygame.image.load(hair_image_path)
        if self.beard:
            self.beard_image = pygame.image.load(beard_image_path)

    def draw_appearance(self, screen, node):
        screen.blit(self.base_image, node.position)
        if self.hair:
            screen.blit(self.hair_image, node.position)
        if self.beard:
            screen.blit(self.beard_image, node.position)
        screen.blit(self.eyes_image, node.position)
        screen.blit(self.clothing_image, node.position)

    def search_direct_lineage(self, family, level):
        if level in family:
            family[level].append(self)
        else:
            family.update({level: [self]})

        if self.mother is not None:
            self.mother.search_direct_lineage(family, level + 1)
        if self.father is not None:
            self.father.search_direct_lineage(family, level + 1)

    def direct_ancestors_tree(self):
        family = {}
        self.search_direct_lineage(family, 0)
        return family

    def search_dinasty(self, dinasty, level):
        if self.gender == 'male':
            if level - 1 in dinasty:
                dinasty[level - 1].extend(self.children)
            else:
                if len(self.children) > 0:
                    dinasty.update({level - 1: self.children})

        if self.father is not None:
            self.father.search_dinasty(dinasty, level + 1)
        if self.father is None:
            dinasty.update({level: [self]})

    def dinasty_tree(self):
        dinasty = {}
        self.search_dinasty(dinasty, 0)
        return dinasty

    def add_child(self, names, id_generator):
        new_gender = random.choice(['male', 'female'])
        if new_gender == 'male':
            new_name = random.choice(names[0])
        else:
            new_name = random.choice(names[1])

        if self.gender == 'male':
            child = Character(id_generator.get_next_id(), new_name, new_gender, self.surname, self, self.spouse)
        else:
            child = Character(id_generator.get_next_id(), new_name, new_gender, self.spouse.surname, self.spouse,
                              self)

        child_hair_color = random.choice([self.hair_color, self.spouse.hair_color])
        child_eye_color = random.choice([self.eye_color, self.spouse.eye_color])
        child_skin_color = random.choice([self.skin_color, self.spouse.skin_color])

        child.set_genetics(child_skin_color, child_hair_color, child_eye_color)

        self.children.append(child)
        self.spouse.children.append(child)
        return child

    def __str__(self):
        if self.gender == 'male':
            prefix = 'Sir'
        else:
            prefix = 'Lady'

        if self.father and self.mother:
            return f'{prefix} {self.name} {self.surname} child of {self.father.name} with {self.mother.name}'
        else:
            return f'founder {prefix} {self.name} of {self.surname}'


def search_all_characters(character, all_chars, level):
    is_inside = False
    for listchars in all_chars.values():
        if character in listchars:
            is_inside = True
            break

    if is_inside is False:
        if level in all_chars:
            all_chars[level].append(character)
        else:
            all_chars.update({level: [character]})

        if len(character.children) > 0:
            for child in character.children:
                search_all_characters(child, all_chars, level + 1)

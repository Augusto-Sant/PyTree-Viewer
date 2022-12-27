import random


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

    def search_direct_lineage(self, family, level):
        if level in family:
            family[level].append(self)
        else:
            family.update({level: [self]})

        if self.mother is not None:
            self.mother.search_direct_lineage(family, level + 1)
        if self.father is not None:
            self.father.search_direct_lineage(family, level + 1)

    def direct_ancestors(self):
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

    def dinasty(self):
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


def all_characters(world_characters):
    all_chars = {}
    for character in world_characters:
        if character.father is None:
            search_all_characters(character, all_chars, 0)

    changed_all_chars = {}
    for i, level in enumerate(reversed(all_chars)):
        changed_all_chars[i] = all_chars[level]

    return changed_all_chars

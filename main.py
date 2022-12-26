import random


class Character:
    def __init__(self, name, gender, surname, father=None, mother=None, spouse=None):
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

    def add_child(self, names):
        new_gender = random.choice(['male', 'female'])
        if self.gender == 'male':
            child = Character(random.choice(names[0]), new_gender, self.surname, self, self.spouse)
        else:
            child = Character(random.choice(names[1]), new_gender, self.spouse.surname, self.spouse, self)
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


def print_tree(tree_list):
    max_value_length = len(max(tree_list.values(), key=len))
    for level in reversed(tree_list):
        space = max_value_length - len(tree_list[level])
        print(f"{level}." + " " * space, end="")
        for character in tree_list[level]:
            print(f'|{character.name} {character.surname}|', end=" ")
        print()


def create_founders(world_characters, names, surnames):
    for i in range(20):
        # read names 0 male 1 female
        new_male_founder = Character(random.choice(names[0]), 'male', random.choice(surnames))
        new_female_founder = Character(random.choice(names[1]), 'female', random.choice(surnames))
        new_male_founder.spouse = new_female_founder
        new_female_founder.spouse = new_male_founder
        world_characters.append(new_female_founder)
        world_characters.append(new_male_founder)


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
    world_characters = []
    create_founders(world_characters, names, surnames)
    # simulate world
    YEARS_TO_PASS = 200
    for i in range(YEARS_TO_PASS):
        for character in world_characters:
            chance = random.randint(0, 1000)
            if chance > 980 and character.spouse is not None:
                child = character.add_child(names)
                world_characters.append(child)
            elif chance > 980 and character.spouse is None:
                marry_event(world_characters, character)

    for i, character in enumerate(world_characters):
        print(i, character)

    # see detail
    while True:
        choice = int(input(">:"))
        char = world_characters[choice]
        print(char)
        subchoice = int(input("? 1 direct 2 patrilineal (0 to exit): "))
        if subchoice == 1:
            print("-- DIRECT LINEAGE --")
            tree = char.direct_ancestors()
            print_tree(tree)
        elif subchoice == 2:
            print("-- DINASTY LINEAGE -- ")
            tree = char.dinasty()
            print_tree(tree)


if __name__ == "__main__":
    main()

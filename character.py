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
        if self.gender == 'male':
            child = Character(id_generator.get_next_id(), random.choice(names[0]), new_gender, self.surname, self, self.spouse)
        else:
            child = Character(id_generator.get_next_id(), random.choice(names[1]), new_gender, self.spouse.surname, self.spouse,
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

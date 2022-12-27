class Node:
    """
    Each Node of a Binary Tree for viewing each character information
    """

    def __init__(self, character, position, font, color, children):
        self.character = character
        self.position = position
        self.font = font
        self.color = color
        self.children = children

    def draw(self, screen):
        text = f'{self.character.id_key}. {self.character.name} {self.character.surname}'
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position
        screen.blit(text_surface, text_rect)

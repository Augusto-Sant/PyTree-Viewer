import pygame


class Node:
    """
    Each Node of a Binary Tree for viewing each character information
    """

    def __init__(self, character, position, font, color, children, circle_color):
        self.character = character
        self.position = position
        self.font = font
        self.color = color
        self.children = children

        self.circle_color = circle_color
        self.circle_radius = 20
        self.circle_rect = pygame.Rect(self.position[0] - self.circle_radius, self.position[1] - self.circle_radius,
                                       self.circle_radius * 2,
                                       self.circle_radius * 2)

    def draw(self, screen):
        text = f'{self.character.id_key}. {self.character.name} {self.character.surname}'
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.position[0], self.position[1] - 20)
        pygame.draw.circle(screen, self.circle_color, self.position, self.circle_radius)
        self.character.draw_appearance(screen, self)
        screen.blit(text_surface, text_rect)


class TextScreen:
    def __init__(self, text, position, font, color):
        self.text = text
        self.position = position
        self.font = font
        self.color = color

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position
        screen.blit(text_surface, text_rect)

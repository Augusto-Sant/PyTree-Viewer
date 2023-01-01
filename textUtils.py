import pygame


class Node:
    """
    Each Node of a Binary Tree for viewing each character information inside main loop pygame
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
        char_desc = f'{self.character.id_key}. {self.character.name} {self.character.surname}'
        char_desc_surface = self.font.render(char_desc, True, self.color)
        char_desc_rect = char_desc_surface.get_rect()
        char_desc_rect.center = (self.position[0], self.position[1] - 20)
        pygame.draw.circle(screen, self.circle_color, self.position, self.circle_radius)
        self.character.draw_appearance(screen, self)
        screen.blit(char_desc_surface, char_desc_rect)
        if len(self.children) > 0:
            num_children = f'{len(self.children)}'
            num_children_surface = self.font.render(num_children, True, pygame.Color(233, 196, 106, 126))
            num_children_rect = num_children_surface.get_rect()
            num_children_rect.center = (self.position[0] - 20, self.position[1] + 20)
            screen.blit(num_children_surface, num_children_rect)
        if self.character.alive is False:
            dead_status = f' D'
            dead_status_surface = self.font.render(dead_status, True, pygame.Color(230, 57, 70, 126))
            dead_status_rect = dead_status_surface.get_rect()
            dead_status_rect.center = (self.position[0] - 10, self.position[1] + 20)
            screen.blit(dead_status_surface, dead_status_rect)


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

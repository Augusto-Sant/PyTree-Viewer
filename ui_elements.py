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

    def find_node_children(self, nodes):
        node_children = []
        # find the correspondent nodes of each character children
        if len(self.character.children) != 0:
            for child in self.character.children:
                for node_2 in nodes:
                    if node_2.character is child:
                        node_children.append(node_2)
        return node_children


class TextScreen:
    def __init__(self, text, position, font, color):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.background_color = None

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position
        screen.blit(text_surface, text_rect)


class Button:
    def __init__(self, position, width, height, text, font, action):
        self.position = position
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.action = action

        self.surface = pygame.Surface((self.width, self.height))
        self.color_background = "white"
        self.rect = None

    def render(self):
        self.surface.fill(self.color_background)

        text_surface = self.font.render(self.text, True, (0, 0, 0))

        self.surface.blit(text_surface, (50, 10))

        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def draw(self, screen):
        screen.blit(self.surface, self.position)

    def collidepoint(self, position):
        # Check if the mouse is over the button
        return self.rect.collidepoint(position)


class NodeTree:
    def __init__(self):
        self.tree = {}

    def draw_tree(self, character_chosen, font, screen, camera, draw_lines=True):
        size = screen.get_size()
        HEIGHT = size[0]
        WIDTH = size[1]
        # camera x and y for offset of objects after camera movement
        position_y = (HEIGHT // 2) - 150 - camera.position_y
        position_x = 200 - camera.position_x
        color = 'white'
        space = 300
        nodes = []

        for level in reversed(self.tree):
            max_value_length = len(max(self.tree.values(), key=len))

            i = 0
            for character in self.tree[level]:
                if i == 0:
                    initial_space = max_value_length - len(self.tree[level])
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

            position_x = 200 - camera.position_x
            position_y += 200

        for node in nodes:
            if draw_lines is True:
                node_children = node.find_node_children(nodes)

                for child_node in node_children:
                    line_color = pygame.Color(52, 58, 64, 126)
                    pygame.draw.line(screen, line_color, node.position, child_node.position)

            node.draw(screen)

        # return to get nodes positions
        return nodes

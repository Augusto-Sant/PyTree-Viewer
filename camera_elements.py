import pygame


class Camera:
    def __init__(self, position_x, position_y, speed):
        self.position_x = position_x
        self.position_y = position_y
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.position_x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.position_x += self.speed
        elif keys[pygame.K_DOWN]:
            self.position_y += self.speed
        elif keys[pygame.K_UP]:
            self.position_y -= self.speed

    def reset(self):
        self.position_x = 0
        self.position_y = 0
        self.speed = 5

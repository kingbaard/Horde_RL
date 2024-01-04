import pygame
import numpy as np
import math

from Constants import *

# TODO: move constants to different location
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class GameObject:
    def __init__(self, x, y, width, height):
        self.x:float = x
        self.y:float = y
        self.width = width
        self.height = height
        self.is_delete_queued = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.slash_rect = None

    def render(self, screen):
        pass

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.slash_rect = None
        self.is_alive = True

    def slide(self, x, y):
        self.x += x
        self.y += y

    def render(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

    def slash(self, enemy, screen):
        slash_x = self.x + self.width
        slash_y = self.y + 2.5

        slash_rect = pygame.Rect(slash_x, slash_y, 25, 25)
        pygame.draw.rect(screen, (0, 255, 0), slash_rect)

        if slash_rect.colliderect(enemy.rect):
            print("Hit enemy!")

        slash_rect = None

class Enemy(GameObject):
    def render(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        rect_color = (255, 0, 0) 
        pygame.draw.rect(screen, rect_color, self.rect)

    def chase(self, player):
        theta = math.atan2(player.y - self.y, player.x - self.x)
        self.x +=  0.3 * np.cos(theta)
        self.y +=  0.3 * np.sin(theta)

class Bullet(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 3, 3)
        self.direction = direction

    def render(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        rect_color = (255, 255, 255) 
        pygame.draw.rect(screen, rect_color, self.rect)

    def move(self):
        if self.direction == UP:
            self.y -= BULLET_SPEED
        elif self.direction == RIGHT:
            self.x += BULLET_SPEED
        elif self.direction == DOWN:
            self.y += BULLET_SPEED
        elif self.direction == LEFT:
            self.x -= BULLET_SPEED

        #check if bullet should be destroyed
        if self.x < 0 or self. x > WIDTH or self.y < 0 or self.y > HEIGHT:
            is_delete_queued = True

class Obstacle(GameObject):
    def render(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y, self.width, self.height))

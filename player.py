import pygame
from constants import *

# This sprite class represents the player platform


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.image = pygame.image.load(IMAGE_PLAYER).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos - PLATFORM_WIDTH/2, SCREEN_HEIGHT - PLATFORM_HEIGHT)

    def update(self, pos):
        self.rect.left = pos - PLATFORM_WIDTH/2

        # check boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def posX(self):
        return self.rect.left + PLATFORM_WIDTH/2

    def posY(self):
        return SCREEN_HEIGHT - PLATFORM_HEIGHT

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)

import pygame
from constants import *

# This sprite class represents a brick. It can be customized to have
# certain health points and different image


class Brick(pygame.sprite.Sprite):
    def __init__(self, gridx, gridy, health, img):
        super(Brick, self).__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.health = health
        self.x = gridx
        self.y = gridy
        self.realx = GRID_PADDING_X + self.x * (BRICK_WIDTH + BRICK_SPACER)
        self.realy = GRID_PADDING_Y + self.y * (BRICK_HEIGHT + BRICK_SPACER)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.realx - BRICK_SPACER/2, self.realy - BRICK_SPACER/2)

    # handle collision if still health
    def collision(self, obj):
        return (self.health != 0 and pygame.sprite.collide_rect(self, obj))

    @staticmethod
    def CreateBrick(gridx, gridy, power):
        if power >= MIN_BRICK_POWER and power <= MAX_BRICK_POWER:
            return Brick(gridx, gridy, BRICKS[power]["health"], BRICKS[power]["image"])
        else:
            raise NotImplementedError("Brick power level, " + power + ", not implemented")

    def draw(self, display):
        if self.health != 0:
            display.blit(self.image, self.rect.topleft)

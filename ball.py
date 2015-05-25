import pygame
import math
from constants import *

# This sprite class represents the ball


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(IMAGE_BALL).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.velocity = BALL_INITIAL_VELOCITY
        self.direction = BALL_INITIAL_DIRECTION

    def bounce(self, difference):
        self.direction = (180 - self.direction - difference) % 360

    def update(self):

        # convert to use radians, requirement of cos, sin
        direction_radian = math.radians(self.direction)

        # update current position
        self.x += self.velocity * math.sin(direction_radian)
        self.y -= self.velocity * math.cos(direction_radian)

        # check for boundaries

        # top
        if self.y <= BALL_RADIUS:
            self.bounce(0)
            self.y = BALL_RADIUS

        # left
        if self.x <= BALL_RADIUS:
            self.bounce(0)
            self.x = BALL_RADIUS

        # right
        if self.x + BALL_RADIUS >= SCREEN_WIDTH:
            self.bounce(0)
            self.x = SCREEN_WIDTH - BALL_RADIUS

        # update image position
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)

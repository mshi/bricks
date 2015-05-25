import pygame
from pygame.locals import *
import math
import random

from ball import Ball
from brick import Brick
from player import Player
from constants import *

# This is main entry point of the game


class Game:

    # initialize resource files
    def __init__(self):
        # initialize pygame stuff
        pygame.init()
        pygame.mixer.init()

        self.display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(NAME + " v" + VERSION)

        self.clock = pygame.time.Clock()

        # initialize objects
        self.player = Player(SCREEN_WIDTH/2)
        self.ball = Ball(self.player.posX(), self.player.posY())

        self.grid = [[None for i in xrange(GRID_WIDTH)] for j in xrange(GRID_HEIGHT)]
        self.running = False
        self.state = STATES["IDLE"]

    # returns list of all elements in grid that are non-empty
    def bricks(self):
        ret = []
        for i in xrange(len(self.grid)):
            ret += filter(lambda x: x is not None, self.grid[i])
        return ret

    # Generate the bricks. Fill the grid for now. Todo: randomly generate or load from file
    def generateStage(self):
        for row in xrange(GRID_HEIGHT):
            for col in xrange(GRID_WIDTH):
                # randomize chance for "special" brick
                rand = random.randint(1, BRICK_RANDOM_CHANCE)
                if rand == 1:  # 1/10 for indestructable
                    self.grid[row][col] = Brick.CreateBrick(col, row, 0)
                elif rand <= 5:  # 1/2 for level 1
                    self.grid[row][col] = Brick.CreateBrick(col, row, 1)
                else:  # remaining is split evenly
                    self.grid[row][col] = Brick.CreateBrick(col, row, rand - (BRICK_RANDOM_CHANCE - MAX_BRICK_POWER))

    def handleEvents(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONDOWN:
            self.state = STATES["STARTED"]
        elif event.type == KEYDOWN:
            # handle keyboard inputs
            if event.key == K_ESCAPE:
                # self.state = STATES["MENU"]
                self.running = False
            elif event.key == K_SPACE:
                self.state = STATES["STARTED"]

    def handleKeyInput(self):
        pressed = pygame.key.get_pressed()
        if self.state == STATES["STARTED"] or self.state == STATES["IDLE"]:
            if pressed[K_LEFT]:
                if self.player.move(-PLAYER_SPEED) and self.state == STATES["IDLE"]:
                    self.ball.move(-PLAYER_SPEED, 0)
            if pressed[K_RIGHT]:
                if self.player.move(PLAYER_SPEED) and self.state == STATES["IDLE"]:
                    self.ball.move(PLAYER_SPEED, 0)

    def drawSprites(self):
        self.display.fill(WHITE)
        self.player.draw(self.display)
        self.ball.draw(self.display)
        for brick in self.bricks():
            brick.draw(self.display)

    # main game loop
    def loop(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.handleEvents(event)
            self.handleKeyInput()
            self.drawSprites()
            pygame.display.update()

    # start game method
    def start(self):
        self.generateStage()
        self.running = True
        self.loop()

game = Game()

game.start()
pygame.display.quit()

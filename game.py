import pygame
from pygame.locals import *
import random

from ball import Ball
from brick import Brick
from player import Player
from constants import *
from menu import Menu

# This is main entry point of the game


class Game:

    # initialize resource files
    def __init__(self):
        # initialize pygame stuff
        pygame.init()
        pygame.mixer.init()
        self.sound_player_collide = pygame.mixer.Sound(SOUND_PLAYER_COLLIDE)
        self.sound_brick_collide = pygame.mixer.Sound(SOUND_BRICK_COLLIDE)
        self.sound_start = pygame.mixer.Sound(SOUND_GAME_START)
        self.sound_gameover = pygame.mixer.Sound(SOUND_GAME_OVER)
        self.sound_win = pygame.mixer.Sound(SOUND_WIN)

        self.display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(NAME + " v" + VERSION)

        self.clock = pygame.time.Clock()

        # initialize objects
        self.player = Player(SCREEN_WIDTH/2)
        self.ball = Ball(self.player.posX(), self.player.posY())

        self.grid = [[None for i in xrange(GRID_WIDTH)] for j in xrange(GRID_HEIGHT)]
        self.running = False
        self.state = STATES["IDLE"]
        self.points = 0
        self.background = pygame.image.load(IMAGE_BACKGROUND).convert_alpha()
        self.font = pygame.font.Font(None, 36)
        self.smallFont = pygame.font.Font(None, 16)
        self.largeFont = pygame.font.Font(None, 64)
        self.mouseMode = False

    # returns list of all elements in grid that are non-empty
    def objects(self):
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
            self.mouseMode = True
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

    def updateState(self):
        if self.state == STATES["STARTED"]:  # started state - ball is moving
            self.ball.update()
            if (self.ball.y >= SCREEN_HEIGHT - BALL_RADIUS*2):
                # game over
                self.gameover()
            # check collision with blocks and if any left
            blocksLeft = False
            for obj in self.objects():
                if obj.getHealth() != 0 and not blocksLeft:
                    blocksLeft = True
                result = obj.collision(self.ball)
                if result["collided"]:
                    self.sound_brick_collide.play()
                    self.points += result["points"]
                    self.ball.bounce(0)
            if not blocksLeft:
                self.win()
            # check collision with platform
            if self.player.collision(self.ball):
                self.sound_player_collide.play()
                angleDiff = self.player.angleDiff(self.ball)
                self.ball.bounce(angleDiff)
                # print "Angle: " + str(angleDiff)
            # print self.points

    def handleMouse(self):
        self.player.update(pygame.mouse.get_pos()[0])

    def drawSprites(self):
        self.display.fill(BLACK)
        self.player.draw(self.display)
        self.ball.draw(self.display)
        for obj in self.objects():
            obj.draw(self.display)

    def drawScore(self):
        text = self.smallFont.render("Score: " + str(self.points), True, WHITE)
        self.display.blit(text, [10, 5])

    def gameover(self):
        self.sound_gameover.play()
        display = True
        self.state = STATES["GAMEOVER"]
        self.running = False
        self.display.blit(self.background, (0, 0))
        text = self.largeFont.render("GAME OVER", True, WHITE)
        self.display.blit(text, [60, 60])
        pygame.display.flip()
        while display:
            e = pygame.event.wait()
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                display = False

    def win(self):
        self.sound_win.play()
        display = True
        self.state = STATES["GAMEOVER"]
        self.running = False
        self.display.blit(self.background, (0, 0))
        text = self.largeFont.render("You have won", True, WHITE)
        self.display.blit(text, [60, 60])
        pygame.display.flip()
        while display:
            e = pygame.event.wait()
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                display = False

    # main game loop
    def loop(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.handleEvents(event)
            if self.mouseMode:
                self.handleMouse()
            else:
                self.handleKeyInput()
            self.updateState()
            self.drawSprites()
            self.drawScore()
            pygame.display.update()

    # start game method
    def start(self):
        self.generateStage()
        self.running = True
        self.sound_start.play()
        self.loop()

    def instructions(self):
        display_instructions = True
        page = 1
        while display_instructions:
            # Get the next event
            e = pygame.event.wait()

            if e.type == pygame.QUIT:
                display_instructions = False
            elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                page += 1
                if page == 3:
                    display_instructions = False

            self.display.blit(self.background, (0, 0))

            if page == 1:
                # Draw instructions, page 1
                text = self.font.render("Instructions", True, WHITE)
                self.display.blit(text, [10, 10])

                text = self.font.render("Page 1", True, WHITE)
                self.display.blit(text, [10, 40])

                text = self.font.render("Welcome to break the bricks", True, WHITE)
                self.display.blit(text, [200, 60])

            if page == 2:
                # Draw instructions, page 2
                text = self.font.render("This game is about breaking bricks", True, WHITE)
                self.display.blit(text, [10, 10])

                text = self.font.render("Page 2", True, WHITE)
                self.display.blit(text, [10, 40])

                text = self.font.render("Use your arrow keys to control the board", True, WHITE)
                self.display.blit(text, [125, 100])

                text = self.font.render("Prevent the ball from falling down", True, WHITE)
                self.display.blit(text, [100, 140])

                text = self.font.render("Different bricks require different number of hits to break", True, WHITE)
                self.display.blit(text, [100, 180])

                text = self.font.render("They are worth different point value as well", True, WHITE)
                self.display.blit(text, [1250, 220])

            # Update the screen
            pygame.display.flip()

game = Game()

game.instructions()
game.start()
pygame.display.quit()

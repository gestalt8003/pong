# pong.py
import pygame, random
from .level import Level
from objects.paddle import Paddle
from objects.ball import Ball
import utils.colors as color
from utils.res import load_font, load_audio
from config import PLAYER1_CONTROLS, PLAYER2_CONTROLS, PADDLE_WIDTH, PADDLE_HEIGHT, WIDTH, HEIGHT


class PongLevel(Level):
    """Level for the pong game."""

    def __init__(self, mode):
        Level.__init__(self)
        self.mode = mode

        self.score = [0, 0]
        self.score_font = load_font(None, 100)

        self.player1 = Paddle("Player1", 0, HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER1_CONTROLS)
        if mode == 2:
            self.player2 = Paddle("Player2", WIDTH-PADDLE_WIDTH, HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER2_CONTROLS)
        elif mode == 1:
            self.player2 = Paddle("Player2", WIDTH-PADDLE_WIDTH, HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT, None)
        self.ball = Ball("Ball", WIDTH/2, HEIGHT/2, 10, 10)
        
        self.add_object(self.player1, self.player2, self.ball)

    def tick(self, game):
        self.logic(game)
        self.draw(game.screen)
        Level.tick(self, game)

    def logic(self, game):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            game.change_level("MAIN MENU")

        if self.ball.ballrect.colliderect(self.player1.paddlerect):
            self.ball.bounce(x=True, speed_mult=1.5)
            self.player1.shrink(0.9)
        elif self.ball.ballrect.colliderect(self.player2.paddlerect):
            self.ball.bounce(x=True, speed_mult=1.5)
            self.player2.shrink(0.9)

        if self.ball.ballrect.left < 0:
            self.ball.respawn(1)
            self.player1.reset_size()
            self.player2.reset_size()
            self.score[1] += 1
        elif self.ball.ballrect.right > WIDTH:
            self.ball.respawn(-1)
            self.player1.reset_size()
            self.player2.reset_size()
            self.score[0] += 1

        if self.mode == 1:
            self.player2.auto(self.ball.ballrect)

    def draw(self, screen):
        screen.fill(color.BLACK)

        # Draw the scores
        self.draw_score(screen, 0)
        self.draw_score(screen, 1)

        # Draw the dividing line
        divider = pygame.Rect(WIDTH/2-10, 0, 20, HEIGHT)
        pygame.draw.rect(screen, color.WHITE, divider)

    def draw_score(self, screen, player):
        score = self.score_font.render(str(self.score[player]), True, color.WHITE)
        score_rect = score.get_rect(y=50)
        if player == 0:
            score_rect.x = WIDTH/2 - score_rect.width * 2
        else:
            score_rect.x = WIDTH/2 + score_rect.width
        screen.blit(score, score_rect)



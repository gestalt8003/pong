# main_menu.py
import pygame, sys
from .level import Level
import utils.colors as color
from utils.res import load_font
from config import WIDTH


class MainMenuLevel(Level):

    def __init__(self):
        Level.__init__(self)

        self.title_font = load_font("good times rg.ttf", 100)
        self.reg_font = load_font(None, 50)

        self.select_buffer = pygame.time.Clock()
        self.last_select = 60

        self.selection = 0

    def tick(self, game):
        self.logic(game)
        self.draw(game.screen)
        Level.tick(self, game)

    def logic(self, game):
        self.select_buffer.tick()
        self.last_select += self.select_buffer.get_time()

        pressed = pygame.key.get_pressed()
        if self.last_select > 120:
            if pressed[pygame.K_UP]:
                self.advance_selection(-1)
                self.last_select = 0
            elif pressed[pygame.K_DOWN]:
                self.advance_selection()
                self.last_select = 0
            elif pressed[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        
        if pressed[pygame.K_RETURN]:
            if self.selection == 0: # 1 player
                game.change_level("1P")
            elif self.selection == 1: # 2 player
                game.change_level("2P")
            elif self.selection == 2: # quit
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        screen.fill(color.BLACK)
        
        # Draw title
        self.write_horiz_center(screen, "PONG", color.WHITE, self.title_font, 150)

        # Draw menu
        self.write_horiz_center(screen, "1 PLAYER", color.WHITE, self.reg_font, 350)
        self.write_horiz_center(screen, "2 PLAYER", color.WHITE, self.reg_font, 400)
        self.write_horiz_center(screen, "QUIT", color.WHITE, self.reg_font, 450)
        
        # Draw cursor
        self.draw_cursor(screen, self.selection, color.WHITE)

    def advance_selection(self, crement=1):
        self.selection += crement
        if self.selection > 2: self.selection = 0
        if self.selection < 0: self.selection = 2
    
    def write_horiz_center(self, screen, text, color, font, y):
        text = font.render(text, True, color)
        text_rect = text.get_rect(y=y)
        text_rect.x = (WIDTH - text_rect.width) / 2
        screen.blit(text, text_rect)

    def draw_cursor(self, screen, selected, color):
        cursor = self.reg_font.render(">", True, color)
        cursor_rect = cursor.get_rect(y=350 + selected*50)
        cursor_rect.x = (WIDTH - cursor_rect.width) / 2 - 100
        screen.blit(cursor, cursor_rect)
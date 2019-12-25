import pygame
from Board import Board

class Drawer:

    BACKGROUND = pygame.Color('WHITE')

    def __init__(self, cell_w=30, cell_h=30, margin=5, display_w=640, display_h=480):
        self.cell_width = cell_w
        self.cell_height = cell_h
        self.margin = margin
        self.display_w = display_w
        self.display_h = display_h
        self.screen = pygame.display.set_mode((self.display_w, self.display_h))
        self.screen.fill(self.BACKGROUND)
        # map Cell enum values to pygame colors
        self.colors = dict([
            (1, pygame.Color('GRAY')),
            (2, pygame.Color('BLACK')),
            (3, pygame.Color('RED'))
        ])

    def draw_board(self, board: Board, color=None) -> None:

        for col in range(board.width):
            for row in range(board.height):

                self.draw_cell(col, row, board.cells[col, row], update=False)
        pygame.display.update()

    def draw_cell(self, col, row, player, update=False):
        color = self.colors[player.value]
        xpos = col * (self.cell_width + self.margin) + self.margin
        ypos = row * (self.cell_height + self.margin) + self.margin
        pygame.draw.rect(self.screen, color, (xpos, ypos, self.cell_width, self.cell_height), 0)
        if update:
            pygame.display.update()

    def show_message(self, msg):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(msg, True, pygame.Color('green'), pygame.Color('blue'))
        self.textRect = text.get_rect()
        self.textRect.center = (self.display_w // 2, 4 * self.display_h // 5)
        self.screen.blit(text, self.textRect)
        pygame.display.update(self.textRect)

    def clear_message(self):
        '''
        Clears the current textbox at the bottom of the GUI
        '''
        self.textRect = pygame.draw.rect(self.screen, self.BACKGROUND, self.textRect)
        pygame.display.update(self.textRect)

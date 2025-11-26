import pygame
from .utility.file_manager import FileManager
from .text import Text
from .ui import Ui
#make shape changeable

class Button(Ui):
    def __init__(self, screen, width, height, text=" ", xpos=0, ypos=0):
        super().__init__("button", width, height, xpos, ypos)
        self.screen = screen
        self.colors["primary"]=(25,25,25)
        self.text = Text(screen, text, self.dim[0], self.dim[1], self.pos[0], self.pos[1])
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.text.rect=self.rect
        self.text.setColor("primary", (255,255,255))

    def setTextSize(self, size):
        self.text.resize(size)
        self.text.rect = self.rect
    def draw(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        self.text.draw()

    def buttonClicked(self, xpos, ypos):
        if self.rect.collidepoint(xpos, ypos):
            return True

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.text.setPos(xpos+(self.dim[0]/10), ypos+(self.dim[1]/9))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.text.rect = self.rect
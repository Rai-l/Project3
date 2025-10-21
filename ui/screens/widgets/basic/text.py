import pygame
from .utility.file_manager import FileManager

class Text:
    def __init__(self, screen, text, xpos=0, ypos=0, type="normal"):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.color = tuple(self.data["color"]["text"])
        self.size = self.data["text"]["size"][type]
        self.font = pygame.font.SysFont(self.data["text"]["font"][type], self.size, bold=True)
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.text = text
        self.renderText = self.font.render(self.text, True, self.color)

    def setText(self, text):
        self.text=text
        self.renderText = self.font.render(self.text, True, self.color)

    def setPos(self, xpos, ypos):
        self.xpos=xpos
        self.ypos=ypos

    def draw(self):
        self.screen.blit(self.renderText, (self.xpos,self.ypos))
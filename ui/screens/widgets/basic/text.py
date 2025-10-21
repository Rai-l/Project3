import pygame
from utility.file_manager import FileManager

class Text:
    def __init__(self, screen, text, xpos=0, ypos=0, type="normal"):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.color = tuple(self.data["color"]["text"])
        self.size = self.data["text"]["size"][type]
        self.font = pygame.font.SysFont(self.data["text"]["font"][type], self.size, bold=False)
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.text = text

    def setText(self, text):
        self.text=text

    def setPos(self, xpos, ypos):
        self.xpos=xpos
        self.ypos=ypos

    def draw(self):
        text = self.font.render(self.text, True, self.color)
        self.screen.blit(text, (self.xpos,self.ypos))
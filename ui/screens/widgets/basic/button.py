import pygame
from .utility.file_manager import FileManager
from .text import Text
#make shape changeable

class Button:
    def __init__(self, screen, text=" ", xpos=0, ypos=0):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.height = self.data["ui_size"]["box"]["height"]
        self.width = self.data["ui_size"]["box"]["width"]
        self.xpos = xpos
        self.ypos = ypos
        self.color = self.data["color"]["border"]
        self.screen = screen
        self.rect = pygame.Rect(xpos, ypos, self.width, self.height)
        self.text = Text(screen, text)

    def draw(self):
        centerCoord = self.text.renderText.get_rect(center=self.rect.center)
        self.text.setPos(centerCoord[0], centerCoord[1])
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.text.draw()

    def setPos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.rect = pygame.Rect(xpos, ypos, self.width, self.height)

    def overrideDimension(self, newWidth, newHeight):
        self.height=newHeight
        self.width=newWidth
    def overrideColor(self, newColor):
        self.color=newColor
    def buttonClicked(self, xpos, ypos):
        if self.rect.collidepoint(xpos, ypos):
            return True

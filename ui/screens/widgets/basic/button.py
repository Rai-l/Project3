import pygame
from utility.file_manager import FileManager
from text import Text


class Button:
    def __init__(self, screen, text, xpos=0, ypos=0):
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
        centerCoord = self.text.get_rect(center=self.rect.center)
        self.text.setPos(centerCoord[0], centerCoord[1])
        self.text.drawText()
        pygame.draw.rect(self.screen, self.color, self.rect)

    def setPos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def button_clicked(self, xpos, ypos):
        if self.rect.collidepoint(xpos, ypos):
            return True

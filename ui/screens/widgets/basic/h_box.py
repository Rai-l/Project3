import pygame
from .utility.file_manager import FileManager

class HBox:
    def __init__(self, xpos, ypos, height, width, xalign=True, yalign=True):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.items = []
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.spacing = self.data["padding"]["yspacing"]
        self.xalign = self.data["padding"]["xalign"] if xalign else 0
        self.yalign = self.data["padding"]["yalign"] if yalign else 0
        self.rect = pygame.Rect(xpos, ypos, self.width, self.height)

    def insert(self, object):
        self.items.append(object)
        pass

    def draw(self):
        xpos = self.xpos + (self.xalign * self.xpos)
        ypos = self.ypos + (self.yalign * self.ypos)
        self.items[0].setPos(xpos, ypos)
        self.items[0].draw()
        xpos += self.spacing
        for i in range(1, len(self.items)):
            self.items[i].setPos(xpos, ypos)
            self.items[i].draw()
            xpos += self.spacing
        pass
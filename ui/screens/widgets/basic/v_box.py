import pygame
from .utility.file_manager import FileManager

class VBox:
    def __init__(self, xpos, ypos, height, width, xalign=True, yalign=True):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.items = []
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.spacing = self.data["padding"]["xspacing"]
        self.xalign = self.data["padding"]["xalign"] if xalign else 0
        self.yalign = self.data["padding"]["yalign"] if yalign else 0
        self.rect = pygame.Rect(xpos, ypos, self.width, self.height)

    def insert(self, object):
        self.items.append(object)
        pass

    def draw(self):
        ypos = self.ypos + (self.yalign * self.ypos)
        xpos = self.xpos + (self.xalign * self.xpos)
        self.items[0].setPos(xpos, ypos)
        self.items[0].draw()
        ypos += self.spacing
        for i in range(1,len(self.items)):
            self.items[i].setPos(xpos, ypos)
            self.items[i].draw()
            ypos += self.spacing
        pass
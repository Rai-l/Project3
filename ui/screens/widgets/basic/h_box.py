import pygame
from utility.file_manager import FileManager

class VBox:
    def __init__(self, xpos, ypos, height, width, align=True, spacing=True):
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.items = []
        self.xalign = self.data["padding"]["xalign"]
        self.yalign = self.data["padding"]["yalign"]
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.spacing = self.data["padding"]["spacing"]
        self.alignB=align
        self.spacingB=spacing

    def insert(self, object):
        self.items.append(object)
        pass

    def draw(self):
        ypos = self.ypos + (self.yalign * self.ypos)
        self.items[0].setPos(ypos, self.ypos)
        for i in range(1, self.items.count()):
            self.items[i].setPos(self.xpos,ypos)
            self.items[i].draw()
            ypos += self.spacing
        pass
import pygame
from .utility.file_manager import FileManager
from abc import ABC, abstractmethod
class Ui(ABC):
    def __init__(self, type, width, height, xpos=0, ypos=0):
        self.pos=(xpos, ypos)
        self.dim=(width, height)
        self.fileManager = FileManager("ui_data")
        self.data = self.fileManager.currData
        self.type=type
        self.colors={
            "primary":(255,255,255),
            "secondary":(0,0,0)
        }
        self.visibility=True

    def setPos(self, xpos, ypos):
        self.pos=(xpos,ypos)
        #reposition other ui after running this func so to repos rect, elements etc.

    def overrideDimension(self, newWidth, newHeight):
        self.dim=(newWidth, newHeight)

    @abstractmethod
    def draw(self):
        pass

    def setColor(self, color, values):
        self.colors[color]=values

    def setVisibility(self, bool):
        self.visibility=bool

    def getVisibility(self):
        return self.visibility
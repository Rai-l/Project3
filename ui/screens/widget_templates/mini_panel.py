import pygame
from .basic_templates.h_box import HBox
from .basic_templates.text import Text
from .basic_templates.ui import Ui

class MiniPanel(Ui):
    def __init__(self, screen, label1, object, width, height, xpos=0, ypos=0, bckgd=False):
        super().__init__("minipanel", width, height, xpos, ypos)
        self.screen=screen
        self.hBox=HBox(self.pos[0], self.pos[1], self.dim[0],self.dim[1])
        self.bckgd = bckgd
        self.setUp(label1, object)
        pass

    def setUp(self, label, object):
        text=Text(self.screen, label,self.dim[0]/2, self.dim[1])
        self.hBox.insert(text)
        self.hBox.insert(object)

    def draw(self):
        if self.bckgd:
            rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
            pygame.draw.rect(self.screen, self.colors["primary"], rect)
        self.hBox.draw()
        pass

    def updateObject(self, object):
        self.hBox[1]=object
        pass

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.hBox.setPos(xpos, ypos)
import pygame
from .basic_templates.v_box import VBox
from .basic_templates.text import Text
from .mini_panel import MiniPanel
from .basic_templates.ui import Ui
class Panel(Ui):
    def __init__(self, screen, width, height, items=6, xpos=0, ypos=0, bckgd=False):
        super().__init__("panel", width, height, xpos, ypos)
        self.screen=screen
        self.vBox = VBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.bckgd = bckgd
        self.items=items

    def __getitem__(self, item):
        return self.vBox[item]

    def insert(self, label, object):
        line=MiniPanel(self.screen, label, object, self.dim[0], self.dim[1]/self.items)
        self.vBox.insert(line)
        pass

    def draw(self):
        if self.bckgd:
            rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
            pygame.draw.rect(self.screen, self.colors["primary"], rect)
        self.vBox.draw()

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.vBox.setPos(xpos,ypos)


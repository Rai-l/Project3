import pygame
from .utility.file_manager import FileManager
from .ui import Ui
class Text(Ui):
    def __init__(self, screen, text, width, height, xpos=0, ypos=0, type="normal", align="center"):
        super().__init__("text", width,height, xpos, ypos)
        self.size = self.data["text"]["size"][type]
        self.font = pygame.font.SysFont(self.data["text"]["font"][type], self.size, bold=True)
        self.colors["primary"]=(0,0,0)
        self.fontName = self.data["text"]["font"][type]
        self.screen = screen
        self.text = text
        self.align=align
        self.minSize=9
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])

    def setText(self, text):
        self.text=text

    def resize(self, size):
        if size>=self.minSize:
            self.size=size
            self.font = pygame.font.SysFont(self.fontName, self.size, bold=True)

    def draw(self):
        renderText = self.font.render(self.text, True, self.colors["primary"])
        centerCoord=renderText.get_rect(center=self.rect.center)
        placement=centerCoord
        if self.align=="top_left":
            placement=(self.pos[0], self.pos[1])
        self.screen.blit(renderText, (placement))

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
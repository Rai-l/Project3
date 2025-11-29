import pygame
from .basic_templates import Ui, HBox, Button, VBox, InputBox
class TextPanel(Ui):
    def __init__(self, screen, xpos, ypos, width, height):
        super().__init__("text_panel", width, height, xpos, ypos)
        self.elements = {}
        self.screen = screen
        self.hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.setUp()
        pass

    def setUp(self):
        elemDim = (self.dim[0] * (3 / 5), self.dim[1] * (7 / 8))
        inputBox = InputBox(self.screen, elemDim[0]+10, elemDim[1], "text")
        self.elements["input_box"] = inputBox
        self.hbox.insert(inputBox)
        vbox = VBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        button = Button(self.screen, elemDim[0]/3, 16, "Submit")
        vbox.insert(button)
        vbox.setPadding(0, 0, 0, 0.1)
        self.elements["submit"] = button
        self.hbox.insert(vbox)
        self.hbox.setPadding(20, 0, 0.02, 0.05)

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        self.hbox.draw()
        pass

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.hbox.setPos(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])

    def buttonClicked(self, xpos, ypos):
        if self.elements["submit"].buttonClicked(xpos, ypos):
            return "input"

    def getInput(self):
        return self.elements["input_box"].getInput()

    def checkConds(self, event):
        self.elements["input_box"].checkConds(event)
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.visibility:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
import pygame
from .panel import Panel
from .basic_templates import Ui, HBox, Button, VBox, InputBox

class FilePanel(Ui):
    '''
    stores inputs from user with InputBox and submit through "submit" Button that helps signal input to higher level ui that is able to store signal

    inherited from Ui
    Attributes:
        elements(dictionary): stores string keys with respective object
        hbox(HBox): container for drawable objects for setting positions and drawing
        rect(pygame.Rect): store a pygame.Rect object for collision references and visual
    '''
    def __init__(self, screen, xpos, ypos, width, height):
        super().__init__("file_panel", width, height, xpos, ypos)
        self.elements = {}
        self.screen = screen
        self.hbox=HBox(self.pos[0], self.pos[1]+3, self.dim[0], self.dim[1])
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.setUp()
        pass

    def setUp(self):
        elemDim = (self.dim[0]*(3/5), self.dim[1]*(2/3))
        inputBox = InputBox(self.screen, elemDim[0]+40, elemDim[1], "file")
        self.elements["input_box"] = inputBox
        self.hbox.insert(inputBox)
        vbox = VBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        button = Button(self.screen, elemDim[0]/3, 16, "Submit")
        vbox.insert(button)
        vbox.setPadding(0,0,0,0.1)
        self.elements["submit"] = button
        self.hbox.insert(vbox)
        self.hbox.setPadding(20,0,0.02, 0.1)

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
        '''
        Returns event signal when collision with "submit" button is detected
        :param event(pygame.event):
        :return(string): return string if signal is triggered else None
        '''
        self.elements["input_box"].checkConds(event)
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and self.visibility:
            if event.type==pygame.MOUSEBUTTONDOWN:
                return self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
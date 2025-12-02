import pygame
from .utility.file_manager import FileManager
from .text import Text
from .ui import Ui
#make shape changeable

class Button(Ui):
    '''
    Creates a button

    Inherits from Ui

    Attributes:
        screen(pygame.Screen): stores an pygame.screen instance needed to draw ui on
        text(Text): stores Text object
        rect(pygame.Rect): stores an pygame.Rect instance for collision and visual purpose
    '''

    def __init__(self, screen, width, height, text=" ", xpos=0, ypos=0, wrap=False):
        '''
        Initializes a Button instance.

        :param screen(pygame.Screen): a pygame.Screen instance
        :param width(int): width of Button
        :param height(int): height of Button
        :param text(string): text to display on button
        :param xpos(int): x coord of button- top left anchor
        :param ypos(int): y coord of button- top left anchor
        :param wrap(boolean): if wrapping is needed
        '''
        super().__init__("button", width, height, xpos, ypos)
        self.screen = screen
        self.colors["primary"]=(25,25,25)
        self.text = Text(screen, text, self.dim[0], self.dim[1], self.pos[0], self.pos[1], wrap)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.text.rect=self.rect
        self.text.setColor("primary", (255,255,255))

    def setTextSize(self, size):
        '''
        Resizes the text attribute in Button
        :param size(int): size of the new text- can be override if wrapping
        :return: None
        '''
        self.text.resize(size)
        self.text.rect = self.rect
    def draw(self):
        '''
        Draws any objects that are drawable
        :return: None
        '''
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        self.text.draw()

    def buttonClicked(self, xpos, ypos):
        '''
        Takes in xy coords and determines if collided with Button
        :param xpos(int): x coord of point that want to test if collision
        :param ypos(int): y coord of point that want to test if collision
        :return(boolean): if collision
        '''
        if self.rect.collidepoint(xpos, ypos):
            return True
        return False

    def setPos(self, xpos, ypos):
        '''
        Calls setPos from base to modify pos attribute and additional modifications to other attributes if needed
        :param xpos(int): new x coord of the new position- top left anchor
        :param ypos(int): new y coord of the new position- top left anchor
        :return: None
        '''
        super().setPos(xpos, ypos)
        self.text.setPos(xpos+(self.dim[0]/10), ypos+(self.dim[1]/9))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.text.rect = self.rect
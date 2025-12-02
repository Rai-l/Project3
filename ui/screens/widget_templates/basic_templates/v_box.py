import pygame
from .utility.file_manager import FileManager
from .ui import Ui
from .container import Container
class VBox(Container):
    '''
    A vertical box object

    Inherits from Container
    '''
    def __init__(self, xpos, ypos, width, height, stack="down"):
        super().__init__(xpos, ypos, width, height)
        self.type="vbox"
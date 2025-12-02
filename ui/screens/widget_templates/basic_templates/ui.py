import pygame
from .utility.file_manager import FileManager
from abc import ABC, abstractmethod
class Ui(ABC):
    '''
    Base class for other ui classes.

    Attributes:
        pos(tuple): a tuple containing current xy coord respectively
        dim(tuple): a tuple containung current width and height respectively
        fileManger(FileManager): stores an instance of FileManager
        data(dict): contains parsed dictionary of ui_data file
        type(string): stores name identifier of the ui object
        colors(dictionary): a dict containing the default keys primary and secondary with values in tuple containing RBG values for determinating color
        visibility(bool): if ui object is currently visible
    '''
    def __init__(self, type, width, height, xpos=0, ypos=0):
        '''
        Initializes an Ui class

        :param type(string): the type of object being creates; used as an identifier
        :param width(int): width of object
        :param height(int): height of object
        :param xpos(int): x coord of object-top left anchor
        :param ypos(int): y coord of object-top left anchor
        '''
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
        '''
        Basic Repositioning of ui object --excludes any additional object such as rect-- need additional manual implementation
        :param xpos(int): the new x coord of object- top left anchor
        :param ypos(int): the new y coord of object- top left anchor
        :return: None
        '''
        self.pos=(xpos,ypos)
        #reposition other ui after running this func so to repos rect, elements etc.

    def overrideDimension(self, newWidth, newHeight):
        '''
        Sets new width and height for given object--excluding additional object such as rect--need additional manual implementation
        :param newWidth(int): the new width of object
        :param newHeight(int): the new height of object
        :return: None
        '''
        self.dim=(newWidth, newHeight)

    @abstractmethod
    def draw(self):
        '''
        Draws any drawable object in ui object given drawable is visible
        :return: None
        '''
        pass

    def setColor(self, color, values):
        '''
        Set new color for colors attribute
        :param color(string): key of the color to change, can be non-existant in colors dict eg. primary, secondary, should always be lowercase key with seperation of underscores when needed
        :param values(tuple): new value to be replaced in colors attribute
        :return: None
        '''
        self.colors[color]=values

    def setVisibility(self, bool):
        '''
        Sets visibility status of the object
        :param bool(boolean): boolean of the new visibility
        :return: None
        '''
        self.visibility=bool

    def getVisibility(self):
        '''
        Returns visibility status
        :return(boolean): if visible
        '''
        return self.visibility
from .ui import Ui

class Container(Ui):
    '''
    Base class for containers eg. VBox, HBox

    Inherited from Ui

    Attributes:
        items(list): stores a list of ui related objects with expectation the object contains setPos, and draw function
        xspacing(int): horizontal spacing between objects
        yspacing(int): vertical spacing between objects
        xalign(float): an inital x offset multiplier based on width such that offset=xalign*width
        yalign(float): an inital y offset multiplier based on width such that offset=yalign*height
    '''

    def __init__(self, xpos, ypos, width, height):
        '''
        Initializes Container object
        :param xpos(int): x coord of object- top left anchor
        :param ypos(int): y coord of object- top left anchor
        :param width(int): width of container
        :param height(int): height of container
        '''
        super().__init__("container", width, height, xpos, ypos)
        self.items = []
        self.xspacing=0
        self.yspacing=0
        self.xalign=0
        self.yalign=0.01
    def setPadding(self, xspacing=0, yspacing=0, xalign=0, yalign=0):
        '''
        Edits padding of container
        :param xspacing(int): new horizontal spacing
        :param yspacing(int): new vertical spacing
        :param xalign(float): new x offset multiplier
        :param yalign(float): new y offset multiplier
        :return:
        '''
        self.xspacing=xspacing
        self.yspacing=yspacing
        self.xalign=xalign
        self.yalign=yalign
        pass

    def __getitem__(self, item):
        '''
        Locates a specific item by its index
        :param item(int): index of the item to be retrieved
        :return: item at the corresponding index
        '''
        return self.items[item]

    def insert(self, object):
        '''
        Appends an object into items attribute
        :param object(any): an object with functions setPos and draw
        :return: None
        '''
        self.items.append(object)
        pass

    def size(self):
        '''
        Returns the length of items attribute
        :return(int): length of items attribute
        '''
        return len(self.items)

    def draw(self):
        '''
        draws all item in items attribute by modifying their position by Container's initial position, offset, and spacing then calling draw() on the item
        :return: None
        '''
        xpos = self.pos[0] + (self.xalign * self.dim[0])
        ypos = self.pos[1] + (self.yalign * self.dim[1])
        for i in range(0, len(self.items)):
            if self.items[i].type=="button":
                self.items[i].setPos(xpos, ypos)
            else:
                self.items[i].setPos(xpos, ypos)
            self.items[i].draw()
            if self.type == "hbox":
                xpos += self.items[i].dim[0]+self.xspacing
            else:
                ypos += self.items[i].dim[1]+self.yspacing
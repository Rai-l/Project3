import pygame

from .basic_templates import Button, Ui
class Node(Ui):
    '''A graphical representation of a node in a graph, with adjacency information and interactive capabilities.
    
    Attributes:
        adj (dict): Adjacency list representing connected nodes and their weights.
        maxR (int): Maximum radius for scaling the node.
        id (str): Identifier for the node.
        scaling (float): Scaling factor for the node's size.
        selected (bool): Indicates if the node is currently selected.
        highlight (bool): Indicates if the node is currently highlighted.
        screen (pygame.Surface): The surface on which the node is drawn.'''

    def __init__(self, screen, id, adjVals, posCoord, radius):
        '''Initializes the Node with its properties and interactive button.
            Parameters:
                screen (pygame.Surface): The surface on which the node is drawn.
                id (str): Identifier for the node.
                adjVals (dict): Adjacency list representing connected nodes and their weights.
                posCoord (tuple): Position coordinates (x, y) of the node.
                radius (int): Radius of the node.'''
        super().__init__("node", radius, radius, posCoord[0], posCoord[1])
        self.adj=adjVals
        self.maxR=radius
        self.id=id
        self.scaling = 1
        self.selected=False
        self.screen = screen
        self.selected=False
        # use _highlight to avoid name collision with the highlight() method
        self._highlight=False
        self.button=Button(screen,self.dim[0]*3/5, self.dim[0]*3/5, self.id, self.pos[0], self.pos[1], True)
        self.button.setTextSize(int(self.dim[0]*2/3))
        self.button.overrideDimension(radius,radius)
        self.button.colors["primary"]=(20,20,20)
        self.button.text.colors["primary"]=(255,255,255)
        self.colors["primary"]=(20,20,20)
        self.colors["selected"]=(200,200,200)
        self.colors["highlighted"] = (155,155,155)
    def isSelected(self):
        return self.selected
    def deselect(self):
        self.selected=False

    def isHighlighted(self):
        return self._highlight
    def highlight(self):
        self._highlight=True

    def unhighlight(self):
        self._highlight=False

    def buttonClicked(self,xpos,ypos):
        if (self.button.buttonClicked(xpos, ypos)):
            self.selected = True
            return True
        else:
            self.selected=False
            return False

    def setScaling(self, scaling):
        self.scaling=scaling

    def draw(self):
        '''Draws the node on the screen with its current properties.''' 
        offset = ((self.pos[0]) * self.scaling, (self.pos[1]) * self.scaling)
        pygame.draw.circle(self.screen, self.colors["primary"], self.pos, self.dim[0])
        if (self.selected or self._highlight):
            border=self.colors["selected"] if self.selected else self.colors["highlight"]
            pygame.draw.circle(self.screen, border, self.pos, self.self.dim[0], 2)
        self.button.draw()

    def drawOffset(self, xoff, yoff, width=0, height=0):
        '''Draws the node with specified offsets and optional dimensions.
            Parameters:
                xoff (int): X-axis offset for drawing the node.
                yoff (int): Y-axis offset for drawing the node.
                width (int): Optional width for scaling the node.
                height (int): Optional height for scaling the node.'''
        offset=(((self.pos[0]*self.scaling)+xoff+(width/2)), ((self.pos[1]*self.scaling)+yoff+(height/2)))
        if self.dim[0]>self.maxR:
            self.dim=(self.maxR, self.maxR)
        pygame.draw.circle(self.screen, self.colors["primary"], offset, self.dim[0])
        if self.selected or self._highlight:
            border = self.colors["selected"] if self.selected else self.colors["highlighted"]
            pygame.draw.circle(self.screen, border, offset, self.dim[0], 2)
        #self.button.overrideDimension(self.dim[0]*self.scaling*3/5, self.dim[0]*self.scaling*3/5)
        self.button.setPos(offset[0]-(self.dim[0]/2), offset[1]-(self.dim[0]/2))
        self.button.draw();





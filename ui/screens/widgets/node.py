import pygame

from basic.button import Button

class Node:
    def __init__(self, screen, id, adjVals, posCoord, radius):
        self.adj=adjVals
        self.id=id
        self.position=posCoord#tuple of numbers
        self.selected=False
        self.screen = screen
        self.radius=radius
        self.selected=False
        self.highlight=False
        self.button=Button(screen, id, self.position[0]-radius/2, self.position[1]-radius/2)
        self.button.overrideDimension(radius,radius)
        self.primaryColor=(20,20,20)
        self.button.overrideColor(self.primaryColor)
        self.color={"select":(155,155,155),"Highlight":(200,200,200)}
        #maybe derv button later
    def isSelected(self):
        return self.selected
    def deselect(self):
        self.selected=False

    def isHighlighted(self):
        return self.highlight
    def highlight(self):
        self.highlight=True

    def unhighlight(self):
        self.highlight=False

    def button_clicked(self,xpos,ypos):
        if (self.button.buttonClicked(xpos, ypos)):
            self.selected = True

    def draw(self):
        pygame.draw.circle(self.screen, self.primaryColor, self.position, self.radius)
        if (self.selected or self.highlight):
            border=self.color["select"] if self.selected else self.color["highlight"]
            pygame.draw.circle(self.screen, border, self.position, self.radius, 5)
        self.button.draw();






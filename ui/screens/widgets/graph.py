import pygame
from coord_generator import CoordGenerator
from node import Node

class Graph:
    def __init__(self, screen, xpos, ypos, data=None):
        self.height=500
        self.width=500
        self.xpos=xpos
        self.ypos=ypos #ui
        self.xrange=500
        self.yrange=500
        self.scaling=0.1
        self.scaleBounds=[0.1,1.25]
        sampleData = {
            "N0": {"N1": 12, "N3": 5},
            "N1": {"N2": 3, "N4": 8},
            "N2": {"N0": 9},
            "N3": {"N2": 4, "N5": 7},
            "N4": {"N3": 6},
            "N5": {}
        }
        self.data=data if data else sampleData
        coordGenerator=CoordGenerator()
        coordGenerator.generateCoords(data)
        self.graphCoords=coordGenerator.offset(self.xpos,self.ypos)
        self.graphDimensions=coordGenerator.getDimension()
        self.currPos=(0,0)
        self.rect=pygame.Rect(xpos, ypos, self.width, self.height)
        self.primary=(255,255,255)
        self.mode="Dijkastra"
        self.highlighted={}

    def createNodes(self):
        pass


    def draw(self):
        pass

    def select(self, xpos, ypos):
        pass

    def toggleMode(self):
        self.mode="DFS"if self.mode=="Dijkastra" else "Dijkastra"



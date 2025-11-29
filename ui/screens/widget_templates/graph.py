import pygame
from .coord_generator import CoordGenerator
from .node import Node
from rtree import index
from .basic_templates.ui import Ui

class Graph(Ui):
    def __init__(self, screen, width, height, xpos, ypos, graphData=None):
        super().__init__("graph", width, height, xpos, ypos)
        self.screen=screen
        self.stepping = 1
        self.scaling = 40
        self.xrange=width/30
        self.yrange=height/30
        self.scaleBounds=[25,50]
        self.inRange=[]
        sampleData = {
            "N0": {"N1": 12, "N3": 5},
            "N1": {"N2": 3, "N4": 8},
            "N2": {"N0": 9},
            "N3": {"N2": 4, "N5": 7},
            "N4": {"N3": 6},
            "N5": {}
        }
        self.initialPt=(0,0)
        self.dragStartPos=(0,0)
        self.graphData=graphData if graphData else sampleData
        self.coordGenerator=CoordGenerator(graphData)
        self.graphCoords =self.coordGenerator.getCoords()
        self.graphDimensions=self.coordGenerator.getDimensions()
        self.currPos=(0,0)
        self.rect=pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.mode="Dijkastra"
        self.highlighted={}
        self.nodes={}
        self.idx=index.Index()
        self.selectedNode=None
        self.sourceNode=None
        self.colors["primary"]=(45,45,45)
        self.radius=15
        self.dragging = False
        self.createNodes()
        self.drawn=set()


    def updateScale(self):
        for key, val in self.nodes.items():
            val.overrideDimension(self.radius*(1+self.scaling), self.radius)
            val.setScaling(self.scaling)
    def createNodes(self):
        count=0
        for key,val in self.graphData.items():
            coord=self.graphCoords[key]
            self.nodes[count] = Node(self.screen, key, val, self.graphCoords[key], self.radius)
            self.idx.insert(count, (coord[0]-self.radius/2, coord[1]-self.radius/2, coord[0]+self.radius/2, coord[1]+self.radius/2))
            count+=1
        self.updateScale()
    def draw(self):
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        rDist = (self.xrange*self.scaling , self.yrange*self.scaling )
        self.inRange=list(self.idx.intersection(((self.currPos[0]-rDist[0]), (self.currPos[1]-rDist[1]), (self.currPos[0]+rDist[0]), (self.currPos[1]+rDist[1]))))
        self.interpretInRange()
        self.drawn=set()
        for n in self.inRange:
            self.drawBranches(n)
        for n in self.inRange:
            n.drawOffset((self.pos[0] + self.currPos[0]), (self.pos[1] + self.currPos[1]), self.dim[0], self.dim[1])
        pass

    def interpretInRange(self):
        temp=[]
        for n in self.inRange:
            temp.append(self.nodes[n])
        self.inRange=temp
    def toggleMode(self):
        self.mode="DFS"if self.mode=="Dijkastra" else "Dijkastra"

    def highlightPath(self, nodes):
        if nodes==None: return
        if len(self.highlighted)>0:
            for key, val in self.highlighted.items():
                val.unhighlight()
        self.highlighted=nodes
        for key, val in self.highlighted.items():
            val.highlight()
        pass

    def buttonClicked(self,xpos,ypos):
        for key, val in self.nodes.items():
            if val.buttonClicked(xpos,ypos):
                if val==self.selectedNode:
                    self.sourceNode=val
                    return "source"
                elif self.selectedNode != val and self.selectedNode:
                    self.selectedNode.deselect()
                self.selectedNode=val
                return "selected"
        return "deselected"

    def drawBranches(self, node):
        initBranch=node.pos
        branches=[]
        color=[]
        offset=(self.pos[0]+self.currPos[0], self.pos[1]+self.currPos[1])
        for adj in node.adj:
            for node in self.inRange:
                if adj not in self.drawn and node.id==adj:
                    branches.append(node.pos)
                    if node.isHighlighted() and not node.isSelected():
                        color.append((150, 150, 150))
                    elif node.isSelected():
                        color.append((200,200,200))
                    else:
                        color.append((0,0,0))
        for i in range(len(branches)):
            #draw line from init to n
            #(self.pos[0]+self.currPos[0]), (self.pos[1]+self.currPos[1])
            #((self.pos[0]*self.scaling)+xoff+(width/2)), ((self.pos[1]*self.scaling)+yoff+(height/2))
            offsetinit=((initBranch[0]*self.scaling)+offset[0]+(self.dim[0]/2), (initBranch[1]*self.scaling)+offset[1]+(self.dim[1]/2))
            offsetBranch=((branches[i][0]*self.scaling)+offset[0]+(self.dim[0]/2), (branches[i][1]*self.scaling)+offset[1]+(self.dim[1]/2))
            pygame.draw.line(self.screen, color[i], offsetinit, offsetBranch, 2)
            pass
        pass

    def setDim(self, width, height):
        super().overrideDimension(width, height)
        self.xrange=width/60
        self.yrange=height/60
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])

    def checkConds(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                sig=self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if sig=="deselected":
                    if self.selectedNode:
                        self.selectedNode.deselect()
                    self.selectedNode=None
                    self.initialPt = pygame.mouse.get_pos()
                    self.dragStartPos = self.currPos
                    self.dragging = True
                return sig
            if self.dragging and event.type==pygame.MOUSEMOTION:
                mx, my = event.pos
                ix, iy = self.initialPt

                dx = (mx - ix)
                dy = (my - iy)

                self.currPos = (self.dragStartPos[0] + dx,
                                self.dragStartPos[1] + dy)
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and self.scaling>self.scaleBounds[0]:
                    self.scaling-=self.stepping
                    self.updateScale()
                elif event.y > 0 and self.scaling<self.scaleBounds[1]:
                    self.scaling += self.stepping
                    self.updateScale()
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        pass
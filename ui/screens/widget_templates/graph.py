import pygame
from .coord_generator import CoordGenerator
from .node import Node
from rtree import index
from .basic_templates.ui import Ui

class Graph(Ui):
    '''
    Builds a graph with generated nodes set with randomly generated nodes drawn when camera is in range and given dimensions and xy coord(top left anchor)

    Attributes:
        stepping(int): stepping when incr or decr scaling by user
        scaling(int): current scaling factor
        xrange(int): int that is used with scaling to determine x position and dimension of Nodes when zooming in/out and dragging
        yrange(int): int that is used with scaling to determine y position and dimension of Nodes when zooming in/out and dragging
        scaleBounds(list): a list of the lower and upper bound of scaling
        inRange(list): list of int representing keys of nodes attribute
        initialPt(tuple): records initial position in screen before dragging
        dragStartPosition(tuple): records initial world position before dragging
        graphData(dictionary): adjacent list containing string keys representing nodes and dict values that represent edges
        coordGenerator(CoordGenerator): stores an instance of CoordGenerator
        graphDimensions(tuple): stores a tuple made of width and height respectively of the generated graph's width and height
        currPos(tuple): stores the current world position within the graph, centered in the middle of the graph
        rect(pygame.Rect): stores an instance of pygame.Rect
        mode(string): stores current mode of path finding algorithm
        highlighted(dictionary): stores a dictionary of string keys and Node values that are highlighted
        nodes(dictionary): stores a dictionary of int keys and Node values
        idx(index.Index()): stores index.Index() from rtree module
        selectedNode(Node): stores an instance of Node that is considered selected
        sourceNode(Node): stores an instance of Node that is considered the source node used to compute shortest path
        radius(int): stores the default radius to draw nodes
        dragging(bool): if dragging the graph
        drawn(set): a set containing all string id of Nodes that have been drawn
    '''
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

        norm = {}
        for k, v in (self.graphData.items()):
            nk = k.strip() if isinstance(k, str) else k
            if isinstance(v, dict):
                nv = { (kk.strip() if isinstance(kk, str) else kk): vv for kk, vv in v.items() }
            elif isinstance(v, (list, tuple, set)):
                nv = [ (ii.strip() if isinstance(ii, str) else ii) for ii in v ]
            else:
                nv = v
            norm[nk] = nv
        self.graphData = norm

        self.coordGenerator = CoordGenerator(self.graphData)
        self.graphCoords = self.coordGenerator.getCoords()

        self.graphDimensions=self.coordGenerator.getDimensions()
        self.currPos=(0,0)
        self.rect=pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.mode="dijkstra"
        self.highlighted={}
        self.nodes={}
        self.idx=index.Index()
        self.selectedNode=None
        self.sourceNode=None
        self.nodeMap = {}
        self.colors["primary"]=(45,45,45)
        self.radius=15
        self.dragging = False
        self.createNodes()
        self.drawn={}


    def updateScale(self):
        for key, val in self.nodes.items():
            val.overrideDimension(self.radius*(1+self.scaling), self.radius)
            val.setScaling(self.scaling)

    def createNodes(self):
        count=0
        for key,val in self.graphData.items():
            coord=self.graphCoords[key]
            self.nodes[count] = Node(self.screen, key, val, self.graphCoords[key], self.radius)
            self.nodeMap[key] = self.nodes[count]
            self.idx.insert(count, (coord[0]-self.radius/2, coord[1]-self.radius/2, coord[0]+self.radius/2, coord[1]+self.radius/2))
            count+=1
        self.updateScale()
    def draw(self):
        '''
        Draws drawable object and Nodes specifically in range of the graph and avoid generating those too far using intersection.
        :return:
        '''
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        rDist = (self.xrange*self.scaling , self.yrange*self.scaling )
        self.inRange=list(self.idx.intersection(((self.currPos[0]-rDist[0]), (self.currPos[1]-rDist[1]), (self.currPos[0]+rDist[0]), (self.currPos[1]+rDist[1]))))
        self.interpretInRange()
        self.drawn= {}

        self.screen_positions = {}
        xoff = (self.pos[0] + self.currPos[0])
        yoff = (self.pos[1] + self.currPos[1])
        for n in self.inRange:
            sx = int((n.pos[0] * self.scaling) + xoff + (self.dim[0] / 2))
            sy = int((n.pos[1] * self.scaling) + yoff + (self.dim[1] / 2))
            self.screen_positions[n.id] = (sx, sy)

        for n in self.inRange:
            self.drawBranches(n)
        for n in self.inRange:
            n.drawOffset((self.pos[0] + self.currPos[0]), (self.pos[1] + self.currPos[1]), self.dim[0], self.dim[1])
        pass

    def interpretInRange(self):
        '''
        redefine inRange's items which consist of int into string values
        :return:
        '''
        temp=[]
        for n in self.inRange:
            temp.append(self.nodes[n])
        self.inRange=temp
    def toggleMode(self):
        self.mode="BFS"if self.mode=="dijkstra" else "dijkstra"

    def highlightPath(self, nodes):
        '''
        Unhighlight prev highlighted nodes and highlight given nodes in the form of dict with string keys and Node vals
        :param nodes(dictionary): copy of a dictionary consisting of string key; node names and their respective Node objects
        :return: None
        '''
        if nodes==None: return
        if len(self.highlighted)>0:
            for key, val in self.highlighted.items():
                val.unhighlight()
        self.highlighted=nodes
        for key, val in self.highlighted.items():
            val.highlight()
        pass

    def buttonClicked(self,xpos,ypos):
        '''
        detect collision and perform specific action based on object collided.
        On click of a Node, Node is marked selected, if Node was already selected, set as the new source Node
        On click of the graph, selected Node is deselected
        All actiong are recorded by returning the name that identifies the action
        :param xpos(int):
        :param ypos(int):
        :return(string): action made
        '''
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

    def drawBranches(self, currNode):
        '''
        For adjacent nodes in node, draw a line from node to adjacent given
        :param node: current node to draw a branch from
        :return: None
        '''
        if not hasattr(self, 'screen_positions'):
            return
        init_screen = self.screen_positions.get(currNode.id)
        if not init_screen:
            return

        branches=[]
        colors=[]

        inrange_ids = {n.id for n in self.inRange}

        neigh_ids = currNode.adj.keys() if isinstance(currNode.adj, dict) else currNode.adj

        for adj_id in neigh_ids:
            target = self.nodeMap.get(adj_id)
            if not target:
                continue
            if target.id not in inrange_ids:
                continue

            target_screen = self.screen_positions.get(target.id)
            if not target_screen:
                continue

            branches.append(target_screen)

            if self.selectedNode is not None and (currNode == self.selectedNode or currNode.isSelected()):
                edge_color = (200, 200, 200)
            elif self.highlighted and (currNode.id in self.highlighted and target.id in self.highlighted):
                edge_color = (150, 150, 150)
            else:
                edge_color = (0, 0, 0)

            colors.append(edge_color)

        for i, bpos in enumerate(branches):
            pygame.draw.line(self.screen, colors[i], init_screen, bpos, 2)
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
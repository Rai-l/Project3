import pygame
from .display_panel import DisplayPanel
from .widget_templates.graph import Graph
from .data_manager import DataManager
from .widget_templates.basic_templates.text import Text
class MainScreen():
    def __init__(self, screen, width, height):
        self.height=height
        self.width=width
        self.screen=screen
        self.elements={}
        self.primary=(43, 45, 48)
        self.rect = pygame.Rect(0, 0, width, height)
        self.dataManager = DataManager()
        self.setUpScreen()
        pass

    def setUpScreen(self):
        displayPanel = DisplayPanel(self.screen, self.width, self.height)
        self.elements["display_panel"]=displayPanel
        graph = Graph(self.screen,self.width-420, self.height, 420,0, self.dataManager.data)
        self.elements["graph"]=graph
        self.update("preset")
        text= Text(self.screen, "Shortest Weighted Path Finder", 200, 100, 420/4)
        text.resize(25)
        text.setColor("primary", (255,255,255))
        self.elements["label"] = text
        pass

    def update(self, elemName):
        panel=self.elements["display_panel"]
        graph=self.elements["graph"]
        dataManager=self.dataManager
        if elemName=="selected" or elemName=="deselected":
            nodeName=graph.selectedNode.id if graph.selectedNode else "None"
            panel.updateData("selected", nodeName)
            if nodeName!="None":
                panel.updateData("selected_adj", dataManager.getAdj(nodeName))
            else:
                panel.updateData("selected_adj", nodeName)
        elif elemName=="source":
            newNode = graph.sourceNode.id
            dataManager.setSource(newNode)
            graph.highlightPath(dataManager.path)
            panel.updateData("computed", dataManager.source)
            panel.updateData("computed_adj", dataManager.getAdj(newNode))
            panel.updateData("computed_path", dataManager.getPath())
        elif elemName=="mode":
            dataManager.setMode(panel.data["curr_mode"])
            graph.highlightPath(dataManager.path)
            panel.updateData("computed_path", dataManager.getPath())
        elif elemName=="input":
            self.loadGraph(panel.input, panel.inputType)
            self.update("preset")
        elif elemName=="preset":
            panel.updateData("num_nodes", str(dataManager.num_nodes))
            panel.updateData("selected", "None")
            panel.updateData("selected_adj", "None")
            panel.updateData("computed", "None")
            panel.updateData("computed_adj", "None")
            panel.updateData("computed_path", "None")
        elif elemName == "random":
            self.loadGraph("random", "random")
            self.update("preset")


    def loadGraph(self, input, type="text"):
        dataManager=self.dataManager
        self.dataManager.loadData(input, type)
        self.elements["graph"]=Graph(self.screen,self.width-420, self.height, 420,0, dataManager.data)




    def draw(self):
        rect = pygame.Rect(0, 0, 430, self.height)
        self.elements["graph"].draw()
        pygame.draw.rect(self.screen, self.primary, rect)
        for key, val in self.elements.items():
            if key!="graph":
                val.draw()


    def setDim(self, width, height):
        self.width=width
        self.height=height
        self.elements["display_panel"].setPos(10, self.height-(310))
        self.elements["graph"].setDim(self.width-420, self.height)

    def checkConds(self, event):
        displaySig=self.elements["display_panel"].checkConds(event)
        graphSig=self.elements["graph"].checkConds(event)
        if displaySig and len(displaySig)>0:
            self.update(displaySig)
        if graphSig and len(graphSig)>0:
            self.update(graphSig)
        if event.type==pygame.VIDEORESIZE:
            self.setDim(event.w, event.h)

        pass
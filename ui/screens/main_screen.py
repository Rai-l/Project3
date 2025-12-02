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
        # subscribe graph to path updates from data manager so highlighting is automatic
        def _on_path_update(path_list, path_info, path_dict):
            try:
                # path_list is preferred (ordered), fall back to keys of path_dict
                if path_list and len(path_list) > 0:
                    self.elements["graph"].highlightPath(path_list)
                elif isinstance(path_dict, dict) and len(path_dict) > 0:
                    self.elements["graph"].highlightPath(list(path_dict.keys()))
                else:
                    self.elements["graph"].highlightPath(None)
            except Exception:
                pass

        self.dataManager.on_path_update = _on_path_update
        self.update("preset")
        # initialize computed num_nodes
        self.elements["display_panel"].updateData("num_nodes", str(self.dataManager.num_nodes))
        text= Text(self.screen, "Shortest Path Finder", 200, 100, 420/4)
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
        elif elemName == "source":
            newSource = graph.sourceNode.id
            dataManager.setSource(newSource)
            panel.updateData("computed", dataManager.source)
            panel.updateData("computed2", dataManager.end)
            panel.updateData("computed_path", dataManager.getPath())
        elif elemName=="end_node":
            newEnd = graph.endNode.id
            dataManager.setEnd(newEnd)
            if len(dataManager.path)>0: graph.highlightPath(dataManager.path)
            panel.updateData("computed", dataManager.source)
            panel.updateData("computed2", dataManager.end)
            panel.updateData("computed_path", dataManager.getPath())
        elif elemName=="mode":
            print("mode")
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
            panel.updateData("computed2", "None")
            panel.updateData("computed_path", "None")
        elif elemName == "random":
            self.loadGraph("random", "random")
            self.update("preset")


    def loadGraph(self, input, type="text"):
        dataManager=self.dataManager
        self.dataManager.loadData(input, type)
        # recreate graph with new data
        self.elements["graph"] = Graph(self.screen, self.width-420, self.height, 420, 0, dataManager.data)

        # re-subscribe graph to path updates so highlighting remains automatic after recreation
        def _on_path_update(path_list, path_info, path_dict):
            try:
                if path_list and len(path_list) > 0:
                    self.elements["graph"].highlightPath(path_list)
                elif isinstance(path_dict, dict) and len(path_dict) > 0:
                    self.elements["graph"].highlightPath(list(path_dict.keys()))
                else:
                    self.elements["graph"].highlightPath(None)
            except Exception:
                pass

        self.dataManager.on_path_update = _on_path_update

        # refresh display panel to show new graph metadata
        self.update("preset")


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
            print(displaySig)
            self.update(displaySig)
        if graphSig and len(graphSig)>0:
            self.update(graphSig)
        if event.type==pygame.VIDEORESIZE:
            self.setDim(event.w, event.h)

        pass
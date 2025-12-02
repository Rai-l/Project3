
from .widget_templates.basic_templates import VBox, HBox, Text, Button
from .widget_templates.panel import Panel
from .widget_templates.basic_templates.input_box import InputBox
from .widget_templates.file_panel import FilePanel
from .widget_templates.text_panel import TextPanel

import pygame

class DisplayPanel():
    '''A panel for displaying and managing graph data and user interactions.
    
    Attributes:
        screen (pygame.Surface): The main display surface.
        dim (tuple): Dimensions of the panel (width, height).
        pos (tuple): Position of the panel (x, y).
        panel (Panel): The main panel UI element.
        elements (dict): Dictionary of UI elements within the panel.
        inputType (str): Type of input selected ("file" or "text").
        input (str): The actual input data provided by the user.
        data (dict): Data to be displayed in the panel.'''

    def __init__(self, screen, screen_w, screen_h):
        '''Initializes the DisplayPanel with UI elements and default data.'''
        self.screen=screen
        self.dim=(400, 300)
        self.pos=(10, screen_h-(self.dim[1]+10))
        self.panel=Panel(screen, self.dim[0], self.dim[1], 8 , self.pos[0], self.pos[1]+5)
        self.elements={}
        self.inputType=None
        self.input=None
        self.data={
            "num_nodes": "0",
            "selected": "None",
            "selected_adj": "None",
            "computed":"None",
            "computed_adj":"None",
            "computed_path":"None",
            "curr_mode": "dijkstra"
        }
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.textSize=12
        self.setUp()
        pass

    def setUp(self):
        '''Sets up the UI elements within the DisplayPanel.'''      
        elemDim=(self.dim[0]/8, self.dim[1]/10)
        hbox=HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        button=Button(self.screen, elemDim[0] , elemDim[1]*(4/5), "Text")
        self.elements["text_input"]=button
        hbox.insert(button)
        button = Button(self.screen, elemDim[0], elemDim[1]*(4/5),"File")
        self.elements["file_input"] = button
        hbox.insert(button)
        hbox.setPadding(60)
        self.panel.insert("Please Select an Input", hbox)
        text = Text(self.screen,self.data["num_nodes"],elemDim[0], elemDim[1])
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0,0,0.13)
        self.elements["num_nodes"] = text
        self.panel.insert("Number of Nodes:", hbox)
        text = Text(self.screen, self.data["selected"], elemDim[0]+40, elemDim[1],0,0,True)
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.08)
        self.elements["selected"] = text
        self.panel.insert("Selected Node:", hbox)
        text = Text(self.screen, self.data["selected_adj"], elemDim[0]+40, elemDim[1],0,0,True)
        self.elements["selected_adj"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.08)
        self.panel.insert("Selected Adjacents:", hbox)
        text = Text(self.screen, self.data["computed"], elemDim[0]+40, elemDim[1],0,0,True)
        self.elements["computed"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.08)
        self.panel.insert("Computed Node:", hbox)
        text = Text(self.screen, self.data["computed_adj"], elemDim[0]+40, elemDim[1],0,0,True)
        self.elements["computed_adj"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.08)
        self.panel.insert("Computed Node Adjacents:", hbox)
        text = Text(self.screen, self.data["computed_path"], elemDim[0]+40, elemDim[1],0,0,True)
        self.elements["computed_path"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.08)
        self.panel.insert("Computed Path:", hbox)
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        button = Button(self.screen, elemDim[0]+15, elemDim[1]*(4/5), "Dijkstra")
        hbox.insert(button)
        self.elements["dijkstra_mode"] = button
        button = Button(self.screen, elemDim[0], elemDim[1]*(4/5), "BFS")
        hbox.insert(button)
        self.elements["BFS_mode"] = button
        hbox.setPadding(60)
        self.panel.insert("Mode:", hbox)
        filePanel = FilePanel(self.screen, self.pos[0], self.pos[1] - 40, self.dim[0], 30)
        textPanel = TextPanel(self.screen, self.pos[0], self.pos[1] - (self.dim[1] * (4 / 5) + 10), self.dim[0],
                                   self.dim[1] * (4 / 5))
        filePanel.setVisibility(False)
        textPanel.setVisibility(False)
        self.elements["filePanel"] = filePanel
        self.elements["textPanel"] = textPanel
        pass

    def updateData(self, elemName, newData):
        elem=self.elements[elemName]
        if elem.type == "text":
            self.data[elemName]=newData if newData else "None"
        elem.resize(self.textSize)
        elem.setText(self.data[elemName])

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect)
        self.panel.draw()
        if self.elements["filePanel"].getVisibility() and not self.elements["textPanel"].getVisibility(): self.elements["filePanel"].draw()
        if self.elements["textPanel"].getVisibility() and not self.elements["filePanel"].getVisibility(): self.elements["textPanel"].draw()
        pass


    def buttonAction(self, name):
        '''Handles button actions based on the button name clicked.
        Parameters:
            name (str): The name of the button clicked.
        Returns:
            str: A signal indicating the action taken, if applicable.'''

        if name=="text_input":
            #set text box visib to true
            if self.elements["textPanel"].getVisibility():
                self.elements["textPanel"].setVisibility(False)
            else:
                self.elements["textPanel"].setVisibility(True)
                self.elements["filePanel"].setVisibility(False)
            pass
        elif name=="file_input":
            # set file box visib to true
            if self.elements["filePanel"].getVisibility():
                self.elements["filePanel"].setVisibility(False)
            else:
                self.elements["filePanel"].setVisibility(True)
                self.elements["textPanel"].setVisibility(False)
            pass
        elif name == "dijkstra_mode":
            #generate Dijk path and set to new data
            if self.data["curr_mode"]!="dijkstra":
                self.data["curr_mode"] = "dijkstra"
                return "mode"
        elif name == "BFS_mode":
            if self.data["curr_mode"] != "BFS":
                self.data["curr_mode"] = "BFS"
                return "mode"
        pass

    def buttonClicked(self, xpos, ypos):
        for key, val in self.elements.items():
            if (val.type=="button" or val.type=="file_panel" or val.type=="text_panel") and val.getVisibility() and val.buttonClicked(xpos,ypos):
                return self.buttonAction(key)

        pass

    def checkConds(self, event):
        '''Checks conditions based on events and updates the panel state accordingly.
        Parameters:
            event (pygame.event.Event): The event to check.
        Returns:
            str: A signal indicating any action taken, if applicable.'''
        sig=None
        if self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                sig=self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) if self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) else sig
        if self.elements["filePanel"].checkConds(event):
            sig= self.elements["filePanel"].checkConds(event)
            self.inputType="file"
            self.input=self.elements["filePanel"].getInput()
        if self.elements["textPanel"].checkConds(event):
            sig = self.elements["textPanel"].checkConds(event)
            self.inputType = "text"
            self.input = self.elements["textPanel"].getInput()
        return sig

    def setPos(self, xpos, ypos):
        '''Sets the position of the DisplayPanel and its elements.
        Parameters:
            xpos (int): The x-coordinate of the new position.
            ypos (int): The y-coordinate of the new position.'''
        self.pos=(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.panel.setPos(xpos, ypos)
        self.elements["filePanel"].setPos(xpos, ypos-40)
        self.elements["textPanel"].setPos(xpos, ypos-(self.dim[1]*(4/5)+10))


    def size(self):
        return len(self.elements)
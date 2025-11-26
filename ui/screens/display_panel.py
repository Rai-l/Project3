
from .widget_templates.basic_templates.h_box import HBox
from .widget_templates.basic_templates.v_box import VBox
from .widget_templates.panel import Panel
from .widget_templates.basic_templates.text import Text
from .widget_templates.basic_templates.input_box import InputBox
from .widget_templates.basic_templates.button import Button
import pygame

class DisplayPanel():

    def __init__(self, screen, screen_w, screen_h):
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
            "curr_mode": "Dijkastra"
        }
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.setUp()
        pass

    def setUp(self):
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
        text = Text(self.screen, self.data["selected"], elemDim[0], elemDim[1])
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.13)
        self.elements["selected"] = text
        self.panel.insert("Selected Node:", hbox)
        text = Text(self.screen, self.data["selected_adj"], elemDim[0], elemDim[1])
        self.elements["selected_adj"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.13)
        self.panel.insert("Selected Adjacents:", hbox)
        text = Text(self.screen, self.data["computed"], elemDim[0], elemDim[1])
        self.elements["computed"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.13)
        self.panel.insert("Computed Node:", hbox)
        text = Text(self.screen, self.data["computed_adj"], elemDim[0], elemDim[1])
        self.elements["computed_adj"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.13)
        self.panel.insert("Computed Node Adjacents:", hbox)
        text = Text(self.screen, self.data["computed_path"], elemDim[0], elemDim[1])
        self.elements["computed_path"] = text
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        hbox.insert(text)
        hbox.setPadding(0, 0, 0.13)
        self.panel.insert("Computed Path:", hbox)
        hbox = HBox(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        button = Button(self.screen, elemDim[0]+15, elemDim[1]*(4/5), "Dijkastra")
        hbox.insert(button)
        self.elements["dijkastra_mode"] = button
        button = Button(self.screen, elemDim[0], elemDim[1]*(4/5), "DFS")
        hbox.insert(button)
        self.elements["DFS_mode"] = button
        hbox.setPadding(60)
        self.panel.insert("Mode:", hbox)
        pass

    def updateData(self, elemName, newData):
        elem=self.elements[elemName]
        if elem.type == "text":
            self.data[elemName]=newData if newData else "None"
        elem.setText(self.data[elemName])

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect)
        self.panel.draw()
        pass


    def buttonAction(self, name):
        if name=="text_input":
            #set text box visib to true
            pass
        elif name=="file_input":
            # set file box visib to true
            pass
        elif name == "dijkastra_mode":
            #generate Dijk path and set to new data
            if self.data["curr_mode"]!="dijkastra":
                self.data["curr_mode"] = "dijkastra"
                return "mode"
        elif name == "DFS_mode":
            if self.data["curr_mode"] != "DFS":
                self.data["curr_mode"] = "DFS"
                return "mode"
        pass

    def buttonClicked(self, xpos, ypos):
        for key, val in self.elements.items():
            if val.type=="button" and val.getVisibility() and val.buttonClicked(xpos,ypos):
                return self.buttonAction(key)

        pass

    def checkConds(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            if event.type == pygame.MOUSEBUTTONDOWN:
                sig=self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                return sig
        pass

    def size(self):
        return len(self.elements)
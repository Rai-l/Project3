from .ui import Ui

class Container(Ui):

    def __init__(self, xpos, ypos, width, height):
        super().__init__("container", width, height, xpos, ypos)
        self.items = []
        self.xspacing=0
        self.yspacing=0
        self.xalign=0
        self.yalign=0.01
    def setPadding(self, xspacing=0, yspacing=0, xalign=0, yalign=0):
        self.xspacing=xspacing
        self.yspacing=yspacing
        self.xalign=xalign
        self.yalign=yalign
        pass

    def __getitem__(self, item):
        return self.items[item]

    def insert(self, object):
        self.items.append(object)
        pass

    def size(self):
        return len(self.items)

    def draw(self):
        #rect=pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
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
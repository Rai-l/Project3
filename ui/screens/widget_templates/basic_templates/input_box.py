import pygame
from .ui import Ui
from .text import Text
class InputBox(Ui):
    def __init__(self, screen, width, height, inputType="text", xpos=0, ypos=0):
        super().__init__("input", width, height, xpos, ypos)
        self.screen=screen
        self.inputType=inputType
        self.selected=False
        self.lines=[""]
        self.cursorPos=[0,0]#row, col
        self.maxPos=[0,0]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
        self.text=Text(self.screen, "a test text", self.dim[0], self.dim[1], self.pos[0], self.pos[1], False, True, "top_left", "char")
        self.text.setColor("primary", (255,255,255))
        self.lineSlots=round(self.dim[1]/self.text.getFont().get_height())
        self.offset=0
        self.colors["primary"]=(0,0,0)
        self.cursor=pygame.Rect(self.pos[0], self.pos[1], 1, self.text.getFont().get_height())

    def updateCursorPos(self, xpos, ypos):
        self.cursor = pygame.Rect(xpos+self.pos[0], ypos+self.pos[1]+2, 2, self.text.getFont().get_height()-5)
    def select(self):
        self.selected=True

    def deselect(self):
        self.selected=False

    def calcPos(self, xpos, ypos):
        '''
        init_y=0
        for i in range(self.offset, min(self.offset + self.lineSlots, len(self.lines))):
            self.text.setText(self.lines[i])
            self.text.setPos(self.pos[0], self.pos[1] + init_y)
            if (self.text.pos[1]+self.text.dim[1])<=ypos:
                self.cursorPos[0]=i
            for j in range(len(self.text.text)):
                for k in range(len(self.text.text[j])):
                    width = self.text.getFont().size(self.text.text[j][:k])[0]+self.text.pos[0]
                    if width <= xpos:
                        self.cursorPos[1] = k

            init_y += self.text.getFont().get_height() * len(self.text.text)
        '''
        pass

    def editInput(self, input):
        if input=="delete":
            beforeR = self.lines[self.cursorPos[0]][:self.cursorPos[1] - 1] if self.cursorPos[1] - 1 > 0 else ""
            afterR = self.lines[self.cursorPos[0]][self.cursorPos[1]:] if len(self.lines[self.cursorPos[0]]) >= self.cursorPos[1] + 1 else ""
            self.lines[self.cursorPos[0]] = "".join([beforeR, afterR])
            self.cursorPos[1] = min(max(self.cursorPos[1]-1,0), len(self.lines[self.cursorPos[0]]))

            #self.cursorPos[0]=max(0, self.cursorPos[0]-1)
            #self.cursorPos[1]=len(self.lines[self.cursorPos[0]])
        elif input=="enter":
            self.cursorPos[0]+=1
            if len(self.lines)-1<=self.cursorPos[0]:
                self.lines.append("")
            self.cursorPos[1] = len(self.lines[self.cursorPos[0]])
        else:
            while len(self.lines)<=self.cursorPos[0]:
                self.lines.append("")
            beforeR = self.lines[self.cursorPos[0]][:self.cursorPos[1]] if self.cursorPos[1] > 0 else ""
            afterR = self.lines[self.cursorPos[0]][self.cursorPos[1]:] if len(self.lines[self.cursorPos[0]]) > \
                                                                          self.cursorPos[1] + 1 else ""
            self.lines[self.cursorPos[0]]="".join([beforeR, input, afterR])
            self.cursorPos[1]=min(self.cursorPos[1]+1, len(self.lines[self.cursorPos[0]]))

        self.updateMax()

    def buttonClicked(self, xpos, ypos):
        if self.rect.collidepoint(xpos, ypos):
            self.select()
            self.calcPos(xpos, ypos)
            return True
        self.deselect()
        return False

    def checkConds(self, event):
        if self.visibility:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if (event.type==pygame.KEYDOWN) and self.selected:
                if event.key==pygame.K_LEFT:
                    if self.cursorPos[1]-1>-1:
                        self.cursorPos[1]-=1
                    else:
                        self.cursorPos[1]=max(0, self.cursorPos[1]-1)
                elif event.key == pygame.K_RIGHT:
                    if self.cursorPos[1]<len(self.lines):
                        self.cursorPos[1]+=1
                    else:
                        self.cursorPos[1] = min(len(self.lines[self.cursorPos[0]]), self.cursorPos[1] + 1)
                elif event.key == pygame.K_UP:
                    if self.cursorPos[0]-1>=0:
                        self.cursorPos[0]-=1
                elif event.key == pygame.K_DOWN:
                    if self.cursorPos[0]+1<len(self.lines):
                        self.cursorPos[0]+=1
                elif event.key==pygame.K_BACKSPACE:
                    self.editInput("delete")
                elif event.key==pygame.K_RETURN:
                    self.editInput("enter")
                elif event.type==pygame.K_v and ((pygame.key.get_mods() & pygame.KMOD_CTRL) or (pygame.key.get_mods() & pygame.KMOD_META)or (pygame.K_LSUPER)):
                    pasted=pygame.scrap.get(pygame.SCRAP_TEXT)
                    if pasted:
                        text=pasted.decode('utf-8')
                        oldText="\n".join(self.lines)
                        self.lines=(oldText+text).split("\n")
                else:
                    self.editInput(event.unicode)
            if event.type == pygame.MOUSEWHEEL and self.selected:
                if event.y < 0 and self.offset<len(self.lines):
                    self.offset+=1
                elif event.y > 0 and self.offset>0:
                    self.offset-=1
            if event.type==pygame.DROPFILE and self.inputType=="file":
                if self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    self.lines=[event.file]
            if event.type == pygame.DROPTEXT:
                if self.buttonClicked(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    text=event.text
                    oldText = "\n".join(self.lines)
                    self.lines = (oldText + text).split("\n")


    def getInput(self):
        return "\n".join(self.lines)
    def updateMax(self):
        self.maxPos=[len(self.lines), len(self.lines[len(self.lines)-1])]

    def draw(self):
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        init_y=0
        self.text.setPos(self.pos[0], self.pos[1])
        for i in range(self.offset,min(self.offset+self.lineSlots, len(self.lines))):
            self.text.setText(self.lines[i])
            self.text.setPos(self.pos[0], self.pos[1] + init_y)
            if i==self.cursorPos[0]:
                cursorOff=self.text.getFont().size(self.lines[self.cursorPos[0]][:self.cursorPos[1]])
                if cursorOff[0]>self.dim[0]:
                    temp=self.cursorPos[1]
                    print(self.cursorPos[1])
                    for j in range(len(self.text.text)):
                        if temp<=len(self.text.text[j]):
                            print("smaller")
                            cursorOff = self.text.getFont().size(self.text.text[j][:temp])
                            break
                        temp -= len(self.text.text[j])
                        print("minus"+str(len(self.text.text[j]))+"="+str(temp))
                    self.updateCursorPos(cursorOff[0], init_y+((len(self.text.text)-1)*cursorOff[1]))
                else:
                    self.updateCursorPos(cursorOff[0], init_y)
                pygame.draw.rect(self.screen, (255,255,255), self.cursor)
            self.text.draw()
            init_y+=self.text.getFont().get_height()*len(self.text.text)
        pass

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])

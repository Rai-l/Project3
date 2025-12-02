import pygame
from .ui import Ui
from .text import Text
class InputBox(Ui):
    '''
    An InputBox object that is interactable when selected and collects key pressed to collect user input.

    Inherits from Ui
    Attributes:
        inputType(string): input type is expected to be either "text" or "file"
        selected(bool): if InputBox is selected
        lines(list): stores a list of strings editable by user
        cursorPos(list): a list of two items with the fist indicating the row and the second indicating the col the user is editing
        maxPos(list): a list of two items with the fist indicating the max row index and the second indicating the max col index
        rect(pygame.Rect): stores a pygame.Rect instance
        text(Text): stores a Text object used to draw a line in lines with char based wrapping in place
        lineSlots(int): max number of lines that can be generated when the length of lines is bigger than lineSlots
        offset(int): an offset for which initial line to generate from
        cursor(pygame.Rect): stores a pygame.Rect that acts as a visual element for cursor or where the user is editing
    '''
    def __init__(self, screen, width, height, inputType="text", xpos=0, ypos=0):
        '''
        Initializes InputBox object

        :param screen(pygame.Screen): a pygame.Screen instance
        :param width(int): width of input box
        :param height(int): height of input box
        :param inputType(string): "text" or "file"
        :param xpos: x coord of position- top left anchor
        :param ypos:y coord of position- top left anchor
        '''
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
        '''
        Updates cursor position with offset by the inputbox's own position and dimension
        :param xpos(int): new x coord of new position of cursor
        :param ypos(int): new y coord of new position of cursor
        :return: None
        '''
        self.cursor = pygame.Rect(xpos+self.pos[0], ypos+self.pos[1]+2, 2, self.text.getFont().get_height()-5)
    def select(self):
        self.selected=True

    def deselect(self):
        self.selected=False

    def calcPos(self, xpos, ypos):
        '''
        Based on given global xy coord, calculate the new cursor position in lines attribute
        '''
        lx = xpos - self.pos[0]
        ly = ypos - self.pos[1]

        y = 0
        for line_index in range(self.offset, min(self.offset + self.lineSlots, len(self.lines))):
            self.text.setText(self.lines[line_index])
            font = self.text.getFont()
            line_height = font.get_height()

            for sub_idx, sub in enumerate(self.text.text):
                top = y
                bottom = y + line_height
                if ly >= top and ly <= bottom:
                    rel_x = lx
                    char_index_in_sub = 0
                    for k in range(len(sub) + 1):
                        w = font.size(sub[:k])[0]
                        if w >= rel_x:
                            char_index_in_sub = k
                            break
                    else:
                        char_index_in_sub = len(sub)

                    prev_len = sum(len(s) for s in self.text.text[:sub_idx])
                    col = prev_len + char_index_in_sub
                    self.cursorPos = [line_index, min(col, len(self.lines[line_index]))]

                    cursor_x_pixels = font.size(self.lines[line_index][:self.cursorPos[1]])[0]
                    self.updateCursorPos(cursor_x_pixels, top)
                    return

                y += line_height
        if len(self.lines) > 0:
            last = min(self.offset + self.lineSlots, len(self.lines)) - 1
            self.cursorPos = [last, len(self.lines[last])]
            cursor_x_pixels = self.text.getFont().size(self.lines[last])[0]
            self.updateCursorPos(cursor_x_pixels, (min(self.lineSlots, len(self.lines)) - 1) * self.text.getFont().get_height())
        else:
            self.cursorPos = [0, 0]
            self.updateCursorPos(0, 0)

    def editInput(self, input):
        '''
        Given an input, eval what function to perform;
        delete removes char in a lines based on current cursor position and moves cursor position forward (to the left; prev col) by one if col position is not 0,
        enter always moves to end of next line and if there's no next line, it creates a new line by appending a "" to lines
        any other input would be directly append to the position of cursorPos attribute and moves cursor backward (to the right; next col) by one
        :param input(string): a string data of either "delete", "enter", or a unicode char such as 'a', 'b', ' '
        :return: None
        '''
        if input=="delete":
            beforeR = self.lines[self.cursorPos[0]][:self.cursorPos[1] - 1] if self.cursorPos[1] - 1 > 0 else ""
            afterR = self.lines[self.cursorPos[0]][self.cursorPos[1]:] if len(self.lines[self.cursorPos[0]]) >= self.cursorPos[1] + 1 else ""
            self.lines[self.cursorPos[0]] = "".join([beforeR, afterR])
            self.cursorPos[1] = min(max(self.cursorPos[1]-1,0), len(self.lines[self.cursorPos[0]]))

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
        '''
        Checks if the given xy coord collided with InputBox and handles on click by calling select and calculating the new cursorPos or the new position the user is able to edit and
        not clicked which calls deselect to deselect the object
        :param xpos(int): x coord of event
        :param ypos(int): y coord of event
        :return:
        '''
        if self.rect.collidepoint(xpos, ypos):
            self.select()
            self.calcPos(xpos, ypos)
            return True
        self.deselect()
        return False

    def checkConds(self, event):
        '''
        for given event, check for action.

        :param event(pygame.event):
        :return: None
        '''
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
        '''
        Returns a joined list of lines with "\n" as deliminator
        :return(string): a joined list of lines with "\n" as deliminator
        '''
        return "\n".join(self.lines)

    def updateMax(self):
        self.maxPos=[len(self.lines), len(self.lines[len(self.lines)-1])]

    def draw(self):
        '''
        Draws all drawable object contained in InputBox
        :return: None
        '''
        pygame.draw.rect(self.screen, self.colors["primary"], self.rect)
        init_y = 0
        self.text.setPos(self.pos[0], self.pos[1])

        prev_clip = self.screen.get_clip()
        self.screen.set_clip(self.rect)

        for i in range(self.offset, min(self.offset + self.lineSlots, len(self.lines))):
            self.text.setText(self.lines[i])
            self.text.setPos(self.pos[0], self.pos[1] + init_y)

            self.text.draw()

            if i == self.cursorPos[0]:
                font = self.text.getFont()
                col = self.cursorPos[1]
                acc = 0
                sub_y = 0
                cursor_x_pixels = 0
                for sub in self.text.text:
                    if col <= acc + len(sub):
                        idx = max(0, col - acc)
                        cursor_x_pixels = font.size(sub[:idx])[0]
                        cursor_y_pixels = sub_y
                        break
                    acc += len(sub)
                    sub_y += font.get_height()
                else:
                    if len(self.text.text) > 0:
                        cursor_x_pixels = font.size(self.text.text[-1])[0]
                        cursor_y_pixels = max(0, sub_y - font.get_height())
                    else:
                        cursor_x_pixels = 0
                        cursor_y_pixels = 0

                self.updateCursorPos(cursor_x_pixels, cursor_y_pixels + init_y)
                pygame.draw.rect(self.screen, (255, 255, 255), self.cursor)

            line_height = self.text.getFont().get_height()
            init_y += line_height * max(1, len(self.text.text))

        self.screen.set_clip(prev_clip)
        pass

    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])

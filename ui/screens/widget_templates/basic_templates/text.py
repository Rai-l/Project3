import pygame
from .utility.file_manager import FileManager
from .ui import Ui
class Text(Ui):
    '''
    Creates a Text object used to store and draw text with certain modifiers.

    Attributes:
        size(int): size of text to be drawn
        font(pygame.font): stores a pygame.font instance
        fontName(string): name of font to be used in rendering text eg. "Arial"
        wrap(string): store either "word" or "char" to indicate how to wrap
        align(string): store either "center" or "top_left" to alter rendered text position in rect attribute
        minSize(int): holds the min size a text can be resized to
        wrapping(boolean): determine if full wrapping is needed; wrapping logic depends on wrap attribute
        scrolling(boolean): auto sets wrap to char
        text(string)
    '''
    def __init__(self, screen, text, width, height, xpos=0, ypos=0, wrapping=False, scrolling=False, align="center", wrapType="word"):
        super().__init__("text", width,height, xpos, ypos)
        self.size = self.data["text"]["size"]["normal"]
        self.font = pygame.font.SysFont(self.data["text"]["font"]["normal"], self.size, bold=True)
        self.colors["primary"]=(0,0,0)
        self.fontName = self.data["text"]["font"]["normal"]
        self.wrap=wrapType
        self.screen = screen
        self.align=align
        self.minSize=9
        self.wrapping = True if wrapping and not scrolling else False
        self.scrolling = True if scrolling and not wrapping else False
        self.text = self.getWrapped(text) if (wrapping or scrolling) else [text]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])
    def setWrapping(self, bool):
        self.wrapping=bool

    def setText(self, text):
        '''
        Sets a new text for rendering
        :param text(string): new text to be used in font attribute
        :return: None
        '''
        self.text=self.getWrapped(text) if self.wrapping or self.scrolling else [text]

    def resize(self, size):
        '''
        Resizes a text as long as the new size is larger or equal to the minSize attribute
        :param size(int): new size
        :return: None
        '''
        if size>=self.minSize:
            self.size=size
            self.font = pygame.font.SysFont(self.fontName, self.size, bold=True)
        self.text = self.getWrapped("".join(self.text)) if self.wrapping or self.scrolling else ["".join(self.text)]

    def getFont(self):
        return self.font

    def getCollision(self, xpos, ypos):
        if self.rect.collidepoint(xpos, ypos):
            return True
        else:
            return False
    def draw(self):
        ypos=0
        for word in self.text:
            renderText = self.font.render(word, True, self.colors["primary"])
            centerCoord = renderText.get_rect(center=self.rect.center)
            placement = (centerCoord[0],self.pos[1])
            if self.align == "top_left":
                placement = (self.pos[0], self.pos[1])
            self.screen.blit(renderText, (placement[0],placement[1]+ypos))
            ypos+=self.font.get_height()


    def setPos(self, xpos, ypos):
        super().setPos(xpos, ypos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.dim[0], self.dim[1])


    def getWrapped(self, text, delim="\n"):
        if self.wrapping:
            while self.size>self.minSize:
                if self.font.size(text)[0]>self.dim[0] or self.font.size(text)[1]>self.dim[1]:
                    self.size-=1
                else:
                    break
        self.font = pygame.font.SysFont(self.fontName, self.size, bold=True)
        newText = self.wrapWord(text) if self.wrap=="word" else self.wrapChar(text)
        if self.wrapping:
            while self.size>self.minSize:
                if self.font.size("".join(newText))[0]>self.dim[0] or self.font.size("".join(newText))[1]>self.dim[1]:
                    self.size-=1
                else:
                    break
        self.font = pygame.font.SysFont(self.fontName, self.size, bold=True)
        return newText

    def wrapChar(self, text, delim="\n"):
        '''
        wraps text by width of rect attribute, new line when char appended exceed width
        :param text(string):
        :param delim(string):
        :return:
        '''
        oldText = [text]
        line = ""
        newText = []
        if len(oldText) == 1 and len(oldText[0])<=5: return [text]
        for i in range(len(oldText)):
            for j in range(len(oldText[i])):
                if self.font.size(line + oldText[i][j])[0] <= self.dim[0]:
                    line += oldText[i][j]
                else:
                    newText.append(line)
                    line = oldText[i][j]
            newText.append(line)
        return newText

    def wrapWord(self, text,delim="\n"):
        '''
        wraps text by width of rect attribute, new line when word appended exceed width
        :param text(string):
        :param delim(string):
        :return:
        '''
        oldText = [text]
        line = ""
        newText = []
        if len(oldText) == 1 and len(oldText[0])<=5: return [text]
        for word in oldText:
            if self.font.size(line + word)[0] <= self.dim[0] and word!=delim:
                line += word
            else:
                if word==delim:
                    newText.append(line)
                    line = ""
                else:
                    newText.append(line)
                    line = word
            newText.append(line)
        return newText


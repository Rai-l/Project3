
#sample of tested code w. proper output/visual
"""
import pygame
import sys
from ui.screens.widgets.basic import Button, VBox, HBox, Text
from ui.screens.widgets.basic.utility.file_manager import FileManager

clock=pygame.time.Clock()
FPS=60

def main():
    pygame.init()
    fileManager=FileManager("ui_data")
    data=fileManager.currData
    width = data["ui_size"]["window"]["width"]
    height = data["ui_size"]["window"]["height"]
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Project3")
    running = True
    button1=Button( screen, "Hi, I'm a textB :)")
    text1=Text(screen, "I'm also a texttttttttt :)")
    text2 = Text(screen, "I'm also a text1 :)")
    vbox1=HBox(200, 400, 100, 100, False, False)
    vbox1.insert(text1)
    vbox1.insert(text2)
    vbox1.insert(button1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(data["color"]["background"])
        #button1.draw()
        text1.draw()
        vbox1.draw()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

"""
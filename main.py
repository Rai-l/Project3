#main file for main software ui setups
import pygame
import sys
from ui.screens.widget_templates.basic_templates.utility.file_manager import FileManager
from ui.screens.main_screen import MainScreen

clock=pygame.time.Clock()
FPS=60

def main():
    pygame.init()
    fileManager=FileManager("ui_data")
    data=fileManager.currData
    width = data["ui_size"]["window"]["width"]
    height = data["ui_size"]["window"]["height"]
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Project3")
    running = True
    mainScreen=MainScreen(screen, width, height)
    #add state if more screens
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                mainScreen.checkConds(event)
        mainScreen.draw()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
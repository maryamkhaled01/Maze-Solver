import pygame
import pygame_gui
import sys
from constants import *
import button

pygame.init()

font3 = pygame.font.SysFont(F3,40)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Input")

manager = pygame_gui.UIManager((WIDTH,HEIGHT))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 250), (400, 100)), manager=manager,object_id='#main_text_entry')
 

clock = pygame.time.Clock()

def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))


def get_input():
    while True:

        screen.fill(GREY)
        UI_REFRESH_RATE = clock.tick(60)/1000
        draw_text("Enter discount factor ", font3 , BLACK, 100, 150)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                gamma_str = event.text
                gamma = float(gamma_str)
                return gamma
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        manager.draw_ui(screen)

        pygame.display.update()

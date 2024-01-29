import pygame
import pygame_gui
import sys
from constants import *

def parse_and_remove_plus(input_string):
    words = input_string.split()
    result_string = ' '.join(word.replace('+', '') for word in words)
    result_string = result_string.split()
    return result_string


pygame.init()

font3 = pygame.font.SysFont(F3, 40)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Input")

manager = pygame_gui.UIManager((WIDTH,HEIGHT))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 300), (400, 100)), manager=manager,object_id='#main_text_entry')

clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
lines = []

def get_input(N):
    invalid=False
    while True:
        
        screen.fill(GREY)
        UI_REFRESH_RATE = clock.tick(60) / 1000
        draw_text("Enter grid ", font3, BLACK, 100, 150)
        draw_text("(N Lines will be taken)", font3, BLACK, 100, 200)
        if invalid:
            draw_text("Invalid Input", font3, BLACK, 400, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                grid_str = event.text
                if(len(parse_and_remove_plus(grid_str))==N):
                    lines.append(grid_str)
                    text_input.set_text("")
                    invalid=False
                    print(lines)
                    print(len(lines))
                else:
                    invalid=True
                    text_input.set_text("")
                if len(lines) == N:
                   for i in range(0,N):
                       lines[i]=parse_and_remove_plus(lines[i])

                   print(lines)
                   return lines
                # Display entered text in the text box
                manager.draw_ui(screen)
            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(screen)
        pygame.display.update()


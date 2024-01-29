import pygame
import button
from constants import *
import input1
import input2
import input3
import mode1
import mode2

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")

run = True

# Defining Fonts
font3 = pygame.font.SysFont(F3,40)

# Loading The Button Images
mode1_img = pygame.image.load('1.png').convert_alpha()
mode2_img = pygame.image.load('2.png').convert_alpha()

# Creating the Buttons
mode1_button = button.Button(100,250,mode1_img,1.5)
mode2_button = button.Button(100,390,mode2_img,1.5)

def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

while run:
    screen.fill(GREY)
    # Handling Functions from our Buttons
    if mode1_button.draw(screen) == 1:
        N = input1.get_input() 
        gamma =input2.get_input() 
        grid = input3.get_input(N) 
        mode1.display_maze(grid, gamma, N)
        #MODE1.play()
        run = False
       
    elif mode2_button.draw(screen):
        N = input1.get_input() 
        gamma =input2.get_input() 
        grid = input3.get_input(N) 
        mode2.display_maze(grid, gamma, N)
        run=False

    # The Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
    pygame.display.update()
pygame.quit()
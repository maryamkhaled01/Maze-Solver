# IMPORTS
import numpy as np
import copy
import pygame as pg
import sys
from constants import *
import button
import policy_iteration
import value_iteration
import time
#--------------------------------------------------------------------------------------#
#########################################################################################################
# Function to create maze, extract maze cells and rewards
def create_maze( grid,N):
        maze = [] # List to store maze cells
        rewards=np.zeros((N,N)) # 2D array to store rewards for each cell
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != "B" :
                    maze.append((row, col))
                if grid[row][col].isdigit():
                        rewards[row][col]=float(grid[row][col])
        return maze,rewards 
#########################################################################################################
# Function to solve the maze using value iteration
def solve_GUI(N,gamma,grid,surface):

    start_time = time.time()    
    maze, rewards= create_maze(grid,N)
    state_values = np.zeros_like(rewards)
    actions_str=['>', 'v', '<', '^'] # Representations for different actions


    theta= 1e-6 # Convergence threshold
    delta = float("inf")

    clean_screen2(grid, surface, N,state_values) 
    pg.display.update()  
    pg.time.wait(100)
    # Value iteration loop
    while delta > theta:
        
        delta = 0
        state_values_prev = state_values.copy()
        old_grid = copy.deepcopy(grid)

        # Iterate over each empty cell in the maze
        for i in range (len(maze)):
                possible_values = []

                # Iterate over possible actions (right, down, left, up)
                for action in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row, new_col = maze[i][0] + action[0], maze[i][1] + action[1]

                    # Check if the new position is within the maze boundaries
                    if 0 <= new_row < N and 0 <= new_col <N:
                        possible_values.append(rewards[ maze[i][0], maze[i][1]] + gamma * state_values_prev[new_row, new_col])
                    else:
                        possible_values.append(float('-inf'))

                # Choose the action that maximizes the expected value        
                best_action = np.argmax(possible_values)
                state_values[ maze[i][0],  maze[i][1]] = possible_values[best_action]

                # Update the grid with the chosen action (if the cell isn't terminal sate)
                if not grid[ maze[i][0]][maze[i][1]].isdigit():
                    grid[ maze[i][0]][maze[i][1]] = actions_str[best_action]

        # Calculate the maximum change in state values
        delta=np.max(np.abs(state_values - state_values_prev)) 

        # Check if the grid is the same as the old grid
        if grid == old_grid:
            break

        clean_screen2(grid, surface, N,state_values) 
        pg.display.update()  
        pg.time.wait(100)  

    end_time = time.time()
    elapsed_time = end_time - start_time

    # print(f"\nTotal time taken: {elapsed_time} seconds")

    # Print the final grid with optimal actions                
    # for i in range(N):
    #         print(grid[i][:])
    return state_values      
#########################################################################################################
def clean_screen2(grid, surface, N,state_values):
    # Calculate cube size relative to N
    CUBE_SIZE = min((WINDOW_SIZE[0] - 2 * MARGIN_SIZE) // N, (WINDOW_SIZE[1] - 2 * MARGIN_SIZE) // N)
    GRID_WIDTH = N * CUBE_SIZE
    GRID_HEIGHT = N * CUBE_SIZE

    HORIZONTAL_X1 = MARGIN_SIZE
    HORIZONTAL_X2 = GRID_WIDTH + MARGIN_SIZE
    VERTICAL_Y1 = MARGIN_SIZE
    VERTICAL_Y2 = GRID_HEIGHT + MARGIN_SIZE

    surface.fill(GREY)
    for i in range(0, N + 1):
        pg.draw.line(surface, BLACK, (MARGIN_SIZE + CUBE_SIZE * i, VERTICAL_Y1),
                     (MARGIN_SIZE + CUBE_SIZE * i, VERTICAL_Y2), 2)  # vertical line
        pg.draw.line(surface, BLACK, (HORIZONTAL_X1, MARGIN_SIZE + CUBE_SIZE * i),
                     (HORIZONTAL_X2, MARGIN_SIZE + CUBE_SIZE * i), 2)  # horizontal line
    
    for i in range(N):
        x=grid[i][:]
        for j in range(N):
            font = pg.font.Font(None, int(CUBE_SIZE*0.5))
            font2 = pg.font.Font(None, int(CUBE_SIZE*0.5)-30)
            position = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2)
            # position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE-70, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE-20) 
            position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2 + 45)


            text = font2.render(str(np.round(state_values[i, j], decimals=2)), True, RED)
            text_rect = text.get_rect(center=position2)
            surface.blit(text, text_rect)

            if grid[i][j] == 'B':
                cell_sqr = pg.Rect(MARGIN_SIZE + j * CUBE_SIZE + 1,
                                MARGIN_SIZE + i * CUBE_SIZE + 1,
                                CUBE_SIZE - 1, CUBE_SIZE - 1)
                pg.draw.rect(surface, BLUE, cell_sqr)
            
            elif  grid[i][j].isdigit():
                text = font.render(grid[i][j], True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)
            elif grid[i][j] != '.':
                text = font.render(grid[i][j], True, RED)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

#########################################################################################################
def clean_screen(grid, surface, N,state_values,solved):
    # Calculate cube size relative to N
    CUBE_SIZE = min((WINDOW_SIZE[0] - 2 * MARGIN_SIZE) // N, (WINDOW_SIZE[1] - 2 * MARGIN_SIZE) // N)
    GRID_WIDTH = N * CUBE_SIZE
    GRID_HEIGHT = N * CUBE_SIZE

    HORIZONTAL_X1 = MARGIN_SIZE
    HORIZONTAL_X2 = GRID_WIDTH + MARGIN_SIZE
    VERTICAL_Y1 = MARGIN_SIZE
    VERTICAL_Y2 = GRID_HEIGHT + MARGIN_SIZE

    surface.fill(GREY)
    for i in range(0, N + 1):
        pg.draw.line(surface, BLACK, (MARGIN_SIZE + CUBE_SIZE * i, VERTICAL_Y1),
                     (MARGIN_SIZE + CUBE_SIZE * i, VERTICAL_Y2), 2)  # vertical line
        pg.draw.line(surface, BLACK, (HORIZONTAL_X1, MARGIN_SIZE + CUBE_SIZE * i),
                     (HORIZONTAL_X2, MARGIN_SIZE + CUBE_SIZE * i), 2)  # horizontal line
    
    for i in range(N):
        x=grid[i][:]
        for j in range(N):
            font = pg.font.Font(None, int(CUBE_SIZE*0.5))
            font2 = pg.font.Font(None, int(CUBE_SIZE*0.5)-30)
            position = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2)
            # position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE-70, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE-20) 
            position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2 + 45)

            if solved:
                text = font2.render(str(np.round(state_values[i, j], decimals=2)), True, GREEN)
                text_rect = text.get_rect(center=position2)
                surface.blit(text, text_rect)


            if grid[i][j] == 'B':
                cell_sqr = pg.Rect(MARGIN_SIZE + j * CUBE_SIZE + 1,
                                MARGIN_SIZE + i * CUBE_SIZE + 1,
                                CUBE_SIZE - 1, CUBE_SIZE - 1)
                pg.draw.rect(surface, BLUE, cell_sqr)
            
            elif  grid[i][j].isdigit():
                text = font.render(grid[i][j], True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)
            elif grid[i][j] != '.':
                text = font.render(grid[i][j], True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            
# MAIN   
def display_maze(maze, gamma, N):  
    run = True
    solved = False
    pg.init()
    surface = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Maze Solver")

    state_values = np.zeros_like((N,N))
    CUBE_SIZE = min((WINDOW_SIZE[0] - 2 * MARGIN_SIZE) // N, (WINDOW_SIZE[1] - 2 * MARGIN_SIZE) // N)
    GRID_WIDTH = N * CUBE_SIZE

    # Loading The Button Images
    solve_img = pg.image.load('solve.png').convert_alpha()

    # Creating the Button at the right of the grid
    solve_button = button.Button(GRID_WIDTH + 65, 350, solve_img, 1.5)

    while run:
        clean_screen(maze, surface, N,state_values,solved)
        if solve_button.draw(surface) == 1:
                print("hi")            
                state_values=solve_GUI(N,gamma,maze,surface)
                
                value_iteration.solve(N,gamma,maze,surface)

                solved =True
                print("helloooo")
                clean_screen(maze, surface, N,state_values,solved)
                pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT: # Quit using quit bottom
                pg.quit()
                sys.exit()
        pg.display.update()


# Define maze parameters
N=7
gamma=0.99

# maze = [['100', '.', '.', '.', '10'],
#         ['.', 'B', '.', '.', '.'],
#         ['.', '.', '.', '.', '.'],
#         ['.', '.', '.', 'B', '.'],
#         ['.', '.', '50', '.', 'B']]

# maze = [['B', '70', 'B', '.', '10', '.'],
#         ['.', 'B', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.'],
#         ['.', '.', '20', 'B', '.', '.'],
#         ['.', '.', '.', 'B', '.', '.'],
#         ['.', '.', '50', '.', 'B', '.']]
        
maze = [['B', '.', 'B', '.', '10', '.', '.'],
        ['.', 'B', '.', '.', 'B', '.', '1000'],
        ['.', 'B', '.', 'B', '.', 'B', '.'],
        ['20', '.', '.', 'B', '.', '.', '.'],
        ['.', 'B', '30', 'B', '.', 'B', '.'],
        ['.', '.', '.', 'B', '.', '.', '.'],
        ['.', '.', '100', '.', 'B', '.', '.']]

# display_maze(maze,gamma, N)

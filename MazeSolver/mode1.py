# IMPORTS
import numpy as np
import copy
import pygame as pg
import sys
from constants import *
import button
import policy_iteration
import copy

#---------------------------------------------------------------------------------------------------------------------------------------#
# Display the generated maze
def clean_screen(grid, value_fns, policies, surface, N, color=RED):
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
    
    s = 0
    for i in range(N):
        for j in range(N):
            font = pg.font.Font(None, int(CUBE_SIZE*0.5))
            position = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2)
            font2 = pg.font.Font(None, int(CUBE_SIZE*0.25))
            position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2 + 50)

                
            if grid[i][j] == 'B':
                cell_sqr = pg.Rect(MARGIN_SIZE + j * CUBE_SIZE + 1,
                                MARGIN_SIZE + i * CUBE_SIZE + 1,
                                CUBE_SIZE - 1, CUBE_SIZE - 1)
                pg.draw.rect(surface, BLUE, cell_sqr)

            elif grid[i][j] == '.':
                policy = None
                
                if policies is not None:
                    policy = policies[s]
                else:
                    policy = grid[i][j]
                
                if policy == 'right':
                    text = font.render('>', True, color)
                    text_rect = text.get_rect(center=position)
                    surface.blit(text, text_rect)

                if policy == 'left':
                    text = font.render('<', True, color)
                    text_rect = text.get_rect(center=position)
                    surface.blit(text, text_rect)

                if policy == 'up':
                    text = font.render('^', True, color)
                    text_rect = text.get_rect(center=position)
                    surface.blit(text, text_rect)

                if policy == 'down':
                    text = font.render('v', True, color)
                    text_rect = text.get_rect(center=position)
                    surface.blit(text, text_rect)

            elif grid[i][j] != 'B' and grid[i][j] != '.':
                text = font.render(grid[i][j], True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            s+=1

    s = 0
    for i in range(N):
        for j in range(N):
            font2 = pg.font.Font(None, int(CUBE_SIZE*0.25))
            position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2 + 45)
            if grid[i][j] != 'B':
                if value_fns is not None:
                        text_value = str(round(value_fns[s],2))
                        text = font2.render(text_value, True, color)
                        text_rect = text.get_rect(center=position2)
                        surface.blit(text, text_rect)
            s+=1

#---------------------------------------------------------------------------------------------------------------------------------------#
# Display the generated maze
def clean_screen2(grid, value_fns, surface, N):
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
        for j in range(N):
            font = pg.font.Font(None, int(CUBE_SIZE*0.5))
            position = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2)
                
            if grid[i][j] == 'B':
                cell_sqr = pg.Rect(MARGIN_SIZE + j * CUBE_SIZE + 1,
                                MARGIN_SIZE + i * CUBE_SIZE + 1,
                                CUBE_SIZE - 1, CUBE_SIZE - 1)
                pg.draw.rect(surface, BLUE, cell_sqr)
            
            elif grid[i][j] == 'right':
                text = font.render('>', True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            elif grid[i][j] == 'left':
                text = font.render('<', True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            elif grid[i][j] == 'up':
                text = font.render('^', True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            elif grid[i][j] == 'down':
                text = font.render('v', True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

            elif grid[i][j] != '.':
                text = font.render(grid[i][j], True, BLACK)
                text_rect = text.get_rect(center=position)
                surface.blit(text, text_rect)

    s = 0
    for i in range(N):
        for j in range(N):
            font2 = pg.font.Font(None, int(CUBE_SIZE*0.25))
            position2 = (MARGIN_SIZE + CUBE_SIZE * j + CUBE_SIZE // 2, MARGIN_SIZE + CUBE_SIZE * i + CUBE_SIZE // 2 + 45)
            if grid[i][j] != 'B':
                if value_fns is not None:
                        text_value = str(round(value_fns[s],2))
                        text = font2.render(text_value, True, GREEN)
                        text_rect = text.get_rect(center=position2)
                        surface.blit(text, text_rect)
            s+=1

#--------------------------------------------------------------------------------------------------------------------------------------#
def tracing(temp_maze, discount_factor, N,  surface, convergence_threshold=1e-6, max_iterations=100):
    indx = policy_iteration.get_indx(N)
    next_states = policy_iteration.get_next_states(temp_maze, N)
    policies = policy_iteration.get_initial_policies(next_states, N)
    value_fns = np.zeros(N * N)
    rewards = policy_iteration.get_rewards(temp_maze, N)

    #turn = 0
    for i in range(max_iterations):
        # Policy Evaluation
        new_value_fns = policy_iteration.policy_evaluation(discount_factor, value_fns, rewards, policies, N, indx, i)

        # Policy Improvement
        new_policies = policy_iteration.policy_improvement(discount_factor, new_value_fns, next_states, rewards, indx, N, i)

        clean_screen(temp_maze, new_value_fns, new_policies, surface, N, RED)
        pg.display.update()
        pg.time.wait(100)

        # Check convergence using the value function
        value_function_difference = np.linalg.norm(new_value_fns - value_fns, ord=np.inf)

        if value_function_difference < convergence_threshold or policies == new_policies:
            break

        # Update policies and value functions
        policies = new_policies
        value_fns = new_value_fns


# MAIN   
def display_maze(maze, gamma, N):  
    run = True
    
    pg.init()
    surface = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Maze Solver")

    CUBE_SIZE = min((WINDOW_SIZE[0] - 2 * MARGIN_SIZE) // N, (WINDOW_SIZE[1] - 2 * MARGIN_SIZE) // N)
    GRID_WIDTH = N * CUBE_SIZE

    # Loading The Button Images
    solve_img = pg.image.load('solve.png').convert_alpha()

    # Creating the Button at the right of the grid
    solve_button = button.Button(GRID_WIDTH + 65, 350, solve_img, 1.5)

    end = 0
    while run:
        if end:
            clean_screen2(maze, value_fns, surface, N)
        else:
            clean_screen2(maze, None, surface, N)
        if solve_button.draw(surface) == 1:
            temp_maze = copy.deepcopy(maze)
            tracing(temp_maze, gamma, N, surface)
            print('\nPolicy Iteration')
            value_fns, policies = policy_iteration.policy_iteration(maze, gamma, N)
            clean_screen2(maze, value_fns, surface, N)
            end = 1
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

import numpy as np
import random
from typing import Tuple
from tqdm.auto import tqdm
from constants import *
import time
import copy
#########################################################################################################
def generate_maze(N):
    i = 0
    j = 0

    # Intialize the array with spaces
    mazeGrid = [[' ' for _ in range(N)] for _ in range(N)]

    # Move on the grid towards the bottom-right corner (The End cell)
    while i < N - 1 and j < N - 1:
        # Choose to move down or right randomly
        down_or_right = random.choice([True, False])
        
        # Add empty cell down (represented as a '.')
        if down_or_right  and i != N - 1 and mazeGrid[i + 1][j] == ' ':
            i = i + 1
            mazeGrid[i][j] = '.'
                
        # Add empty cell right
        elif down_or_right == False and j != N-1 and mazeGrid[i][j+1] == ' ':
            j = j + 1
            mazeGrid[i][j] = '.'
        else:
            continue

    # if i did not reach the end cell but j did 
    while i < N - 1:
        mazeGrid[i][j] = '.' # assign all remaining cells in the last column to be empty
        i = i + 1

    # if j did not reach the end cell but i did     
    while j < N - 1:
        mazeGrid[i][j] = '.' # assign all remaining cells in the last row to be empty
        j = j + 1
    
    # Loop over the grid
    for i in range(0, N):
        for j in range(0, N):
            # Add barriers in the remaining cells rondomly
            if mazeGrid[i][j] == ' ':
                barrier_or_empty = random.choice([True, False])
                if barrier_or_empty:
                    mazeGrid[i][j] = 'B'
                else:
                    mazeGrid[i][j] = '.'

    return mazeGrid

#########################################################################################################
# Function to create maze, extract maze cells and rewards
def create_maze( grid,N):
        maze = [] # List to store maze cells
        rewards=np.zeros((N,N)) # 2D array to store rewards for each cell
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != "B" :
                    maze.append((row, col))
                    rewards[row][col]=-1
                if grid[row][col].isdigit():
                        rewards[row][col]=float(grid[row][col])
        return maze,rewards 
#########################################################################################################
# Function to solve the maze using value iteration
def solve(N,gamma,grid):

    # set the start time of solving
    start_time = time.time()
    maze, rewards= create_maze(grid,N)
    state_values = np.zeros_like(rewards)
    actions_str=['>', 'v', '<', '^'] # Representations for different actions

    theta= 1e-6 # Convergence threshold
    delta = float("inf")

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
    
    # set the end time of solving
    end_time = time.time()

    # calculate the time of solving
    elapsed_time = end_time - start_time

    # PRINT total taken time of solving
    print(f"\nTotal time taken: {elapsed_time} seconds\n")
                
    # Print the final grid with optimal actions                
    # for i in range(N):
    #         print(grid[i][:])
    # for i in range(N):
    #         print(state_values[i][:])
    # return state_values         

# Define maze parameters
N=7
gamma=0.99


# Define the maze as a 2D grid with rewards and obstacles

# grid = [['100', '.', '.', '.', '10'],
#         ['.', 'B', 'B', '.', '.'],
#         ['B', '.', '.', '.', '.'],
#         ['.', '.', '.', 'B', '.'],
#         ['.', '.', '50', '.', 'B']]



# grid = [['B', '70', 'B', '.', '10', '.'],
#         ['.', 'B', '.', '.', '.', '.'],
#         ['.', '.', '.', '.', '.', '.'],
#         ['.', '.', '20', 'B', '.', '.'],
#         ['.', '.', '.', 'B', '.', '.'],
#         ['.', '.', '50', '.', 'B', '.']]


grid = [['B', '.', 'B', '.', '10', '.', '.'],
        ['.', 'B', '.', '.', 'B', '.', '1000'],
        ['.', 'B', '.', 'B', '.', 'B', '.'],
        ['20', '.', '.', 'B', '.', '.', '.'],
        ['.', 'B', '30', 'B', '.', 'B', '.'],
        ['.', '.', '.', 'B', '.', '.', '.'],
        ['.', '.', '100', '.', 'B', '.', '.']]

# Call the solve function to find optimal actions for each cell in the maze
# solve(N,gamma,grid)


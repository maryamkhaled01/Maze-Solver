# IMPORTS
import random
import numpy as np
import time

#-------------------------------------------------------------------------------------------------#
# Create a matrix NxN to store the index of each state
def get_indx(N):
    indx = [[0 for _ in range(N)] for _ in range(N)]
    s = 0
    for i in range(N):
        for j in range(N):
            indx[i][j] = s
            s += 1

    # Return (N,N) 2d array of indexes
    return indx

#-------------------------------------------------------------------------------------------------#
# Get the next available actions for each state
def get_next_states(maze, N):
    
    # Initialize the next states 2d array with spaces
    # any state which do not have next actions their row will remain ' '
    # and any state which do not have a specific direction to move to, its place will also remain as ' '
    next_states = [[' ' for _ in range(4)] for _ in range(N * N)]  # [down, right, up, left]

    s = 0
    for i in range(N):
        for j in range(N):
            if maze[i][j] != 'B': # for non barrier state

                # for each direction if the next state will not be out of the bounds and not a barrier
                # add the action of this diraction to the next actions of this state
                if i + 1 <= N - 1 and maze[i + 1][j] != 'B': 
                    next_states[s][0] = 'down'
                if j + 1 <= N - 1 and maze[i][j + 1] != 'B':
                    next_states[s][1] = 'right'
                if i - 1 >= 0 and maze[i - 1][j] != 'B':
                    next_states[s][2] = 'up'
                if j - 1 >= 0 and maze[i][j - 1] != 'B':
                    next_states[s][3] = 'left'
            s += 1

    # PRINT the available next actions of each state
    print(f'\nAvailable Next Actions of each state:')
    for i, row in enumerate(next_states):
        row = [x for x in row if x != ' ']
        print(f'Actions({i}): {row}')

    # Return a (NxN, 4) 2d array contains the next available actions of each state
    return next_states

#-------------------------------------------------------------------------------------------------#
# Initialize The policies randomly according to each state's available next actions
def get_initial_policies(next_states, N):
    k = 0
    policies = [' ' for _ in range(N * N)]

    while k < N * N:
       
        # remove any spaces from the row of available actions for each state
        next_states[k] = [x for x in next_states[k] if x != ' ']

        # if this state has at least one avavlabe next action 
        # choose a random policy from its available next actions
        if next_states[k]:
            rand = random.choice(next_states[k])
            policies[k] = rand
        k += 1

    # PRINT Initial randomized policy of each state
    print(f'\nInitial Randomized Policy of each state:')
    for i, row in enumerate(policies):
        print(f'Policy({i}): {row}')

    # Return (N*N) array for policies
    return policies

#-------------------------------------------------------------------------------------------------#
# Get the immediate reward of each state 
def get_rewards(maze, N):
    rewards = [0 for _ in range(N * N)]
    k = 0
    for i in range(N):
        for j in range(N):

            # take the value given in the grid for terminal states
            if maze[i][j] != '.' and maze[i][j] != 'B':
                rewards[k] = float(maze[i][j])

            # put an immediate reward -1 for empty states
            if maze[i][j] == '.':
                rewards[k] = -1
            k += 1

    # PRINT Initial randomized policy of each state
    print(f'\nImmediate Reward of each state:')
    for i, row in enumerate(rewards):
        print(f'R({i}): {row}')
    
    # Return (N*N) array of rewards
    return rewards

#-------------------------------------------------------------------------------------------------#
# Implemmentation of Policy Evaluation
def policy_evaluation(discount_factor, value_fns, rewards, policies, N, indx, iter):
    new_value_fns = np.zeros(N * N)
    s = 0

    # Loop over the states
    for i in range(N):
        for j in range(N):
            x = policies[s] # get the current policy of each state
            if x != ' ':

                # according to the policy, get the oldV(s') and the R(s') of the next state(s')
                if x == 'right' and j + 1 < N:
                    value = value_fns[indx[i][j + 1]]
                    reward = rewards[indx[i][j + 1]]
                elif x == 'down' and i + 1 < N:
                    value = value_fns[indx[i + 1][j]]
                    reward = rewards[indx[i + 1][j]]
                elif x == 'left' and j - 1 >= 0:
                    value = value_fns[indx[i][j - 1]]
                    reward = rewards[indx[i][j - 1]]
                elif x == 'up' and i - 1 >= 0:
                    value = value_fns[indx[i - 1][j]]
                    reward = rewards[indx[i - 1][j]]

                # Apply Bellman equation of value function (assume the policy is determinestic, prob = 1)
                # as the action led to one state then there is no summation
                # bellman equation: V(s) = R + gamma * oldV(s')
                new_value_fns[s] = reward + discount_factor * value
            s += 1
    
    # # PRINT New value functions of each state at each iteration
    # print(f'\nNew value functions of each state at iteration {iter}:')
    # for i, row in enumerate(new_value_fns):
    #     print(f'V({i}): {row}')
    
    # Return (N*N) array of new value functions 
    return new_value_fns

#-------------------------------------------------------------------------------------------------#
# Implemmentation of Policy Improvement
def policy_improvement(discount_factor, value_fns, next_states, rewards, indx, N, iter):
    new_policies = [' ' for _ in range(N * N)]
    s = 0
    for i in range(N):
        for j in range(N):
            
            # get the valid next actions for each state
            valid_actions = [x for x in next_states[s] if x != ' ']
            if valid_actions:
                action_value_fns = np.zeros(len(valid_actions))

                # # PRINT Action value functions of each state at each iteration
                # print(f'\nAction value functions of each state at iteration {iter}:')

                # calculate the avction value function for each action of those actions
                for v, x in enumerate(valid_actions):
                    if x == 'right' and j + 1 < N:
                        reward = rewards[indx[i][j + 1]]
                        value = value_fns[indx[i][j + 1]]
                    elif x == 'down' and i + 1 < N:
                        reward = rewards[indx[i + 1][j]]
                        value = value_fns[indx[i + 1][j]]
                    elif x == 'left' and j - 1 >= 0:
                        reward = rewards[indx[i][j - 1]]
                        value = value_fns[indx[i][j - 1]]
                    elif x == 'up' and i - 1 >= 0:
                        reward = rewards[indx[i - 1][j]]
                        value = value_fns[indx[i - 1][j]]
                    # save them in action value functions array
                    action_value_fns[v] = reward + discount_factor * value

                    # # PRINT
                    # print(f'Q({s},{x}): {action_value_fns[v]}')

                # Choose the action that will give the maximium action value function
                # Choose random action if the acation value functions are equal
                best_action_indices = [i for i, val in enumerate(action_value_fns) if val == max(action_value_fns)]
                best_action_index = random.choice(best_action_indices)

                # Update the policy of each state with the best action
                # bellman equation: Policy(s) = argmax{Q(s,a)}
                new_policies[s] = valid_actions[best_action_index]

                # # PRINT best action of each state at each iteration
                # print(f'Best Action at iteration {iter}: Best_A({s}): {new_policies[s]}')

            s += 1

    # Return (N*N) array of new policies
    return new_policies

#-------------------------------------------------------------------------------------------------#
# Policy Iteration
def policy_iteration(maze, discount_factor, N, convergence_threshold=1e-6, max_iterations=100):
    # Get initial values
    indx = get_indx(N)
    next_states = get_next_states(maze, N)
    policies = get_initial_policies(next_states, N)
    value_fns = np.zeros(N * N)
    rewards = get_rewards(maze, N)

    # set the start time of solving
    start_time = time.time()

    # Loop until value function convergence or till a max iteration 
    for i in range(max_iterations):
        # Policy Evaluation
        new_value_fns = policy_evaluation(discount_factor, value_fns, rewards, policies, N, indx, i)

        # Policy Improvement
        new_policies = policy_improvement(discount_factor, new_value_fns, next_states, rewards, indx, N, i)

        # Check convergence using the value function
        value_function_difference = np.linalg.norm(new_value_fns - value_fns, ord=np.inf)
        # PRINT
        # print(f'Iteration {i} - Value Function Difference: {value_function_difference}')

        if value_function_difference < convergence_threshold or policies == new_policies:
            # PRINT
            print(f'\nConverged after {i} iterations.')
            break

        # Update policies and value functions
        policies = new_policies
        value_fns = new_value_fns
    
    # PRINT
    print(f'\nNumber of iterations: {i + 1}')

    # set the end time of solving
    end_time = time.time()

    # calculate the time of solving
    elapsed_time = end_time - start_time

    # PRINT total taken time of solving
    print(f"\nTotal time taken: {elapsed_time} seconds")

    # Update the maze with the final policies
    s = 0
    for i in range(N):
        for j in range(N):
            if maze[i][j] == '.':
                maze[i][j] = policies[s]
            s += 1

   # Generate a 2d array for the optimal policy of each state
    policy_matrix = np.array(policies).reshape((N, N))

    # PRINT the optimal policy matrix
    print("\nOptimal Policy Matrix:")
    for row in policy_matrix:
        print(row)

    # PRINT the final maze
    print("\nFinal Maze:")
    for row in maze:
        print(row)

    return new_value_fns, new_policies

# Define maze parameters
N=7
gamma=0.99


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

# policy_iteration(grid,gamma, N)
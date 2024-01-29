# Maze-Solver
In the pursuit of efficient maze-solving strategies, this project focuses on leveraging Policy Iteration and Value Iteration, two dynamic programming techniques within the realm of reinforcement learning. These algorithms provide iterative solutions to the maze navigation problem, offering optimal paths while circumventing obstacles.
Here are the assumptions made throughout the code:
User Inputs: 1.
Maze size in terms of N (NXN). a.
Discount factor (gamma). b.
Maze itself. c.
There’s no initial state. 2.
There’s several cells in the maze that has rewards. 3.
The cell with the greatest reward is the terminal state. 4.
Deterministic environment. 5.
Rewards of terminal state is the value in the maze and rewards of empty statesequals -1.
6.
Empty states are represented as “.”. 7.
Barriers are represented as “B”.
8.
The agent will go to the terminal sate but if another cell with reward on its way hewill take it and continue to the terminal state.

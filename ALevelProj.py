"""Changes made:
Made dimension[0][1] = 2 so that it can be stamped green
Changed bounds function
"""

#modules needed for the project, random for random movements, turtle for visualisation, sys to set recursion limit
import random
import tkinter as tk
import turtle
import sys
import time
from collections import deque
sys.setrecursionlimit(10000)

################################################################################################################################################################

root = tk.Tk()
root.title("Maze Solver")
root.geometry("600x600")

entry = tk.Entry(root)
entry.pack()

wn = turtle.Screen()
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.shape("square")

window_height = 600

# global variables for maze and dimensions
maze = None
dimensions = None

def draw_wall(maze, path=None):
    t.clear()
    size = window_height - 40
    maze_size = len(maze)
    cell_size = (size / maze_size)
    t.shapesize(cell_size / 20)
    total_maze_size = maze_size * cell_size
    start_x = -total_maze_size/2
    start_y = total_maze_size/2

    def wall_path(color):
        t.penup()
        x = start_x + (j * cell_size) + (cell_size / 2)
        y = start_y - (i * cell_size) - (cell_size / 2)
        t.goto(x, y)
        t.color(color)
        t.stamp()

    wn.tracer(0)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 1:
                wn.tracer(0)
                wall_path("black")
                
    wn.update()
    wn.tracer(1)
    if path:
        for i, j in path:
            wall_path("green")
            
            wn.update()

    


################################################################################################################################################################

#function to see if the current index is out of bounds
def is_out_of_bounds(maze, new_i, new_j):
    return new_i < 0 or new_i >= len(maze) or new_j < 0 or new_j >= len(maze[0])   

#def generate_maze_AStar(maze):
    #pass

#function to generate maze
def generate_maze_DFS(maze, i , j):
    directions = [(2,0), (-2,0), (0,2), (0,-2)]
    #shuffles list for randomness
    random.shuffle(directions)
    #iterates and unpacks tuple
    for move_i, move_j in directions:
        #new index
        new_i, new_j = i + move_i, j + move_j
        #checks if out of bounds and if new index is not visited
        if not is_out_of_bounds(maze, new_i, new_j) and maze[new_i][new_j] == 1:
            #if condition is true, carve a path
            maze[new_i][new_j] = 0
            maze[(i+new_i)//2][(j+new_j)//2] = 0
            #recursion
            generate_maze_DFS(maze, new_i, new_j)
            
def randomized_prim(maze, i, j, dimensions):
    # Fill maze with walls
    for x in range(dimensions):
        for y in range(dimensions):
            maze[x][y] = 1

    # Set start and end
    maze[0][1] = 0
    maze[dimensions-1][dimensions-2] = 0

    # Frontier list (stores cells as (x, y, parent_x, parent_y))
    frontier = []

    # Helper to add neighbors to frontier
    def add_frontier(x, y):
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < dimensions-1 and 0 < ny < dimensions-1:
                if maze[nx][ny] == 1 and (nx, ny) not in [(f[0], f[1]) for f in frontier]:
                    frontier.append((nx, ny, x, y))

    # Initialize frontier from start
    add_frontier(i, j)

    # Main loop
    while frontier:
        idx = random.randint(0, len(frontier)-1)
        x, y, px, py = frontier.pop(idx)

        if maze[x][y] == 1:
            # Carve path from parent
            maze[x][y] = 0
            maze[(x+px)//2][(y+py)//2] = 0

            # Add neighbors of the new cell to frontier
            add_frontier(x, y)

#BFS traversal
def BFS_traversal(maze, dimensions):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    start = (0, 1)
    end = (dimensions - 1, dimensions - 2)
    queue = deque([start])
    
    parents = {start: None}
    maze[start[0]][start[1]] = 4  # Start position is marked as visited
    
    while len(queue) > 0:
        x, y = queue.popleft()

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if not is_out_of_bounds(maze, new_x, new_y):
                if maze[new_x][new_y] == 0:  # If it's an empty cell
                    maze[new_x][new_y] = 4  # Mark it as visited
                    parents[(new_x, new_y)] = (x, y)
                    queue.append((new_x, new_y))
                    
        if (x, y) == end:
            break

    # Reconstruct the path from end to start
    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = parents[cur]
        
    for x, y in path:
        maze[x][y] = 2  # Mark the path as visited (green)

    return path[::-1]

#function to find path (pathfinder)
def find_path_dfs(maze, i, j, path):
    # check goal
    if i == dimensions - 1 and j == dimensions - 2:
        path.append((i, j))
        return True

    # invalid move
    if is_out_of_bounds(maze, i, j) or maze[i][j] == 1 or maze[i][j] == 2:
        return False

    # mark visited
    maze[i][j] = 2

    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    random.shuffle(directions)

    for move_i, move_j in directions:
        if find_path_dfs(maze, i + move_i, j + move_j, path):
            path.append((i, j))  # add to path while backtracking
            return True

    # backtrack
    maze[i][j] = 0
    return False

#######################################################################

# function to create maze only once
def create_maze_DFS():
    global maze, dimensions
    value = entry.get()
    if not value.isdigit():
        label = tk.Label(root, text="Enter a valid number.")
        label.pack()
        label.after(1000, label.destroy)
        return
    dimension = int(value)
    if dimension < 4 or dimension > 100:
        label = tk.Label(root, text="Dimensions must be between 4 and 100.")
        label.pack()
        label.after(1000, label.destroy)
        return
    
    dimensions = (2*dimension)+1
    maze = [[1 for i in range(dimensions)] for j in range(dimensions)]
    maze[0][1] = 0
    maze[dimensions-1][dimensions-2] = 0

    generate_maze_DFS(maze, 1, 1)
    draw_wall(maze)

def create_maze_prims():
    global maze, dimensions
    value = entry.get()
    if not value.isdigit():
        label = tk.Label(root, text="Enter a valid number.")
        label.pack()
        label.after(1000, label.destroy)
        return
    dimension = int(value)
    if dimension < 4 or dimension > 100:
        label = tk.Label(root, text="Dimensions must be between 4 and 100.")
        label.pack()
        label.after(1000, label.destroy)
        return
    
    dimensions = (2*dimension)+1
    maze = [[1 for i in range(dimensions)] for j in range(dimensions)]
    maze[0][1] = 0
    maze[dimensions-1][dimensions-2] = 0

    randomized_prim(maze, 1, 1, dimensions)
    draw_wall(maze)

#function triggered by BFS button
def run_bfs():
    if maze is None:
        label = tk.Label(root, text="Generate the maze first!")
        label.pack()
        label.after(1000, label.destroy)
        return
    # create a copy so BFS doesn't overwrite original maze

    maze_copy = [row[:] for row in maze]
    path = BFS_traversal(maze_copy, dimensions)
    draw_wall(maze_copy, path)   

#function triggered by DFS button
def run_dfs():
    if maze is None:
        label = tk.Label(root, text="Generate the maze first!")
        label.pack()
        label.after(1000, label.destroy)

        return
    # create a copy so DFS doesn't overwrite original maze
    maze_copy = [row[:] for row in maze]
    path = []
    find_path_dfs(maze_copy, 1, 1, path)
    path=path[::-1]
    draw_wall(maze_copy, path)

def run_prims():
    if maze is None:
        label = tk.Label(root, text="Generate the maze first!")
        label.pack()
        label.after(1000, label.destroy)
        return
    
    maze_copy = [row[:] for row in maze]
    randomized_prim(maze_copy, 1, 1, dimensions)
    draw_wall(maze_copy)
    

# Buttons
button_dfs = tk.Button(root, text="Run DFS maze gen", command=create_maze_DFS)
button_dfs.pack()

button_prim = tk.Button(root, text="Run Prims Algorithm", command=create_maze_prims)
button_prim.pack()

button_bfs = tk.Button(root, text="Run BFS", command=run_bfs)
button_bfs.pack()

button_dfs = tk.Button(root, text="Run DFS", command=run_dfs)
button_dfs.pack()

root.mainloop()

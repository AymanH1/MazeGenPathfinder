import random
import turtle
import sys
sys.setrecursionlimit(10000)

while True:
    if not dimension.isdigit():
        print("Enter a valid positive integer.")
        continue
    dimension = int(dimension)
    if dimension < 4 or dimension < 100:break
    else:print("Dimensions must be between 4 and 100.")
dimensions = (2*dimension)+1
maze = [[1 for i in range(dimensions)] for j in range(dimensions)]
maze[0][1] = 0
maze[dimensions-1][dimensions-2] = 0

def is_out_of_bounds(maze,new_i, new_j):
    return new_i <= 0 or new_i >= (len(maze)-1) or new_j <= 0 or new_j >= (len(maze)-1)


def generate_maze(maze, i , j):
    directions = [(2,0), (-2,0), (0,2), (0,-2)]
    random.shuffle(directions)
    for move_i, move_j in directions:
        new_i, new_j = i + move_i, j + move_j
        if not is_out_of_bounds(maze, new_i, new_j) and maze[new_i][new_j] == 1:
            maze[new_i][new_j] = 0
            maze[(i+new_i)//2][(j+new_j)//2] = 0
            generate_maze(maze, new_i, new_j)

generate_maze(maze, 1,1)

################################################################################################################################################################

maze[dimensions-1][dimensions-2] = 3
def find_path(maze, i, j):
    if i==dimensions-1 and j == dimensions-2:
        maze[i][j] = 2
        return True
    if is_out_of_bounds(maze,i,j) or maze[i][j] == 1 or maze[i][j] == 2:
        return False
    maze[i][j] = 2
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    random.shuffle(directions)
    for move_i, move_j in directions:
        if find_path(maze, i + move_i, j + move_j):
            return True
    maze[i][j] = 0
    return False
find_path(maze, 1, 1)

##################################################################################################################################################################################

wn = turtle.Screen()
window_width = 1800
window_height = 1000
wn.setup(window_width, window_height)
wn.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.shape("square")


def draw_wall(maze, window_height):
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
                wall_path("black")
            elif cell == 2:
                wall_path("green")
    wn.update()

draw_wall(maze, window_height)
wn.mainloop()
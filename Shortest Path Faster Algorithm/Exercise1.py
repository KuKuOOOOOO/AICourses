import os
import sys

#-----------------------------node and cmd color class------------------------------------
# Group of Different functions for different styles
class style():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[34m' + str(x)
    MAGENTA = lambda x: '\033[35m' + str(x)
    CYAN = lambda x: '\033[36m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)
# Define node(parent, posittion, g, h, f)
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

#-----------------------------a* algoirthm------------------------------------
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Define direction and data
    Direction_list = []
    Direction_Data = ["上", "下", "左", "右"]
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                # Find point(x,y) and last point(x,y) and finish direction
                if current.parent is not None:
                    Xr = current.position[1]-current.parent.position[1]
                    Yr = current.position[0]-current.parent.position[0]
                    if Xr == 0 and Yr == -1:
                        Direction_list.append(Direction_Data[0])
                    elif Xr == 0 and Yr == 1:
                        Direction_list.append(Direction_Data[1])
                    elif Xr == -1 and Yr == 0:
                        Direction_list.append(Direction_Data[2])
                    elif Xr == 1 and Yr == 0:
                        Direction_list.append(Direction_Data[3])
                    else:
                        continue
                path.append(current.position[::-1])
                current = current.parent
            return path[::-1], Direction_list[::-1]  # Return reversed path
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            # if want to add slash, please add this in new_position:(-1, -1), (-1, 1), (1, -1), (1, 1)
            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)
        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)

#-----------------------------Main Function------------------------------------
# Cmd color setting
if sys.platform.lower() == "win32":
    os.system('color')
# Read and show maps.txt file
with open(r'test1.txt') as f:
    # Read first line(map's length and width)
    MapRange = f.readline()[0::].strip('\n')
    MapRange = MapRange.split()
    # Read map (010111100000111...)
    maplist = f.readlines()[0:]
    maplist = ''.join(maplist).strip()
    maplist = maplist.split('\n')
# Define map's length, width and internal
Length_Y = int(MapRange[1])
Width_X = int(MapRange[0])
maze = []
# Show map's length, width and internal
print("\n地圖寬度={}, 地圖長度={}".format(Width_X, Length_Y))
print("test1.txt內部地圖畫面:")
for i in range(len(maplist)):
    maze.append(list(maplist[i]))
    for j in range(len(maze[i])):
        maze[i][j] = int(maze[i][j])
        print(maplist[i][j], end="")
        if j == len(maplist[i])-1:
            print("", end="\n")
# Define start and end point
start = ""
end = ""
#Show start and end point, and check vaious errors
while start == "" and end == "":
    try:
        StartPoint_X, StartPoint_Y, EndPoint_X, EndPoint_Y = map(
            int, input("請輸入起點與終點座標(起點X 起點Y 終點X 終點Y):").split())

        start = (StartPoint_Y, StartPoint_X)  # (y,x)
        end = (EndPoint_Y, EndPoint_X)  # (y,x)
        if StartPoint_X >= Width_X or EndPoint_X >= Width_X or StartPoint_Y >= Length_Y or EndPoint_Y >= Length_Y:
            print("座標請輸入在地圖範圍內!!\n地圖寬度={}, 地圖長度={}".format(Width_X, Length_Y))
            start = end = ""
            continue
        if maze[StartPoint_Y][StartPoint_X] == 1 or maze[EndPoint_Y][EndPoint_X] == 1:
            print("請勿輸入在有障礙物之座標!!")
            start = end = ""
            continue
    except ValueError:
        print("請輸入整數並依照(起點X 起點Y 終點X 終點Y)方式輸入!!")
        start = end = ""
        continue
# Define focus point(A,S,E) to change output color
FocusPointX = []
FocusPointY = []
# Start a* algoirthm and define output format
Path, Direction = astar(maze, start, end)
# Setting path into focus point list 
for i in range(len(Path)):
    FocusPointX.append(Path[i][0])
    FocusPointY.append(Path[i][1])
# Change mark on the map
for i in range(len(FocusPointX)):
    maze[FocusPointY[i]][FocusPointX[i]] = 'A'
    if FocusPointX[i] == StartPoint_X and FocusPointY[i] == StartPoint_Y:
        maze[FocusPointY[i]][FocusPointX[i]] = 'S'
    elif FocusPointX[i] == EndPoint_X and FocusPointY[i] == EndPoint_Y:
        maze[FocusPointY[i]][FocusPointX[i]] = 'E'
# Show map on cmd(1110A000011000111000...)
print("\n在地圖內加上路線圖後之畫面:")
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if maze[i][j] == 'A':
            print(style.RED(maze[i][j]), end="")
        elif maze[i][j] == 'S' or maze[i][j] == 'E':
            print(style.YELLOW(maze[i][j]), end="")
        else:
            print(style.RESET(maze[i][j]), end="")
        if j == len(maze[i])-1:
            print("", end="\n")
# Show explanation and count on cmd
print(style.YELLOW('S')+style.RESET("=起點"), end='\n')
print(style.YELLOW('E')+style.RESET("=終點"))
print(style.RED('A')+style.RESET("=路徑標示"))
# Show path and direction on cmd((4, 14) 上 -> (4, 13)...)
for i in range(len(Path)):
    print(Path[i], end=" ")
    if i != len(Direction):
        print(Direction[i], end=" -> ")
print("\n總步數:" + str(len(Path)-1))

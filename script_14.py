from copy import deepcopy
from itertools import count

hiking_map = []

# start_time = perf_counter()

maze = []
moves = []
robot = None

reading_maze = True
while True:
   try:
      if reading_maze:
         line = input().strip()
         # find @ in the line
         try:
            robot = (len(maze), line.index('@'))
         except Exception as e:
            ...
         if not line:
            reading_maze = False
            continue
         maze.append(list(line))
      else:
         moves.extend(list(input().strip()))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

new_maze = []
for row_ in maze:
   new_row = []
   for col_ in row_:
      if col_ == "@":
         robot = (len(new_maze), len(new_row))
         new_row.extend(list("@."))
      elif col_ == "O":
         new_row.extend(list("[]"))
      else:
         new_row.extend(list(col_*2))
   new_maze.append(new_row)

def print_maze(maze):
   for row_ in maze:
      print(''.join(row_))

maze = new_maze

def bfs_obstacle(row_, col_, maze_, moving_dir=1):
   queue = [(row_, col_)]
   visited = set()
   obstacle = set()
   while queue:
      row, col = queue.pop(0)
      if (row, col) in visited:
         continue
      visited.add((row, col))
      if maze_[row][col] == "]":  # add left bracket and above
         obstacle.add((row, col))
         queue.append((row + moving_dir, col))
         queue.append((row, col - 1))
      elif maze_[row][col] == "[": # add right bracket and above
         obstacle.add((row, col))
         queue.append((row + moving_dir, col))
         queue.append((row, col + 1))
      elif maze_[row][col] == "#": # blocked cannot move
         return False, None
   return True, obstacle


while moves:
   move = moves.pop(0)
   next_position = None
   if move == "^":
      next_position = (robot[0] - 1, robot[1])
   elif move == "v":
      next_position = (robot[0] + 1, robot[1])
   elif move == "<":
      next_position = (robot[0], robot[1] - 1)
   elif move == ">":
      next_position = (robot[0], robot[1] + 1)

   if next_position and maze[next_position[0]][next_position[1]] == "#": # can't move continue
      continue
   elif next_position and maze[next_position[0]][next_position[1]] == ".":
      maze[robot[0]][robot[1]] = "."
      robot = next_position
      maze[robot[0]][robot[1]] = "@"
   else:
      direction_func = {
         "^": lambda r, c, i: (r - i, c),  # UP: decrease row
         ">": lambda r, c, i: (r, c + i),  # RIGHT: increase col
         "v": lambda r, c, i: (r + i, c),  # DOWN: increase row
         "<": lambda r, c, i: (r, c - i),  # LEFT: decrease col
      }[move]
      if move in ["<", ">"]: # same as before
         next_empty = None
         for i in count(1):
            next_pos = direction_func(robot[0], robot[1], i)
            if maze[next_pos[0]][next_pos[1]] == "#":
               break
            elif maze[next_pos[0]][next_pos[1]] == ".":
               next_empty = next_pos
               break
         if next_empty: # move all the crates and the robot in the direction of the move
            maze[robot[0]][robot[1]] = "."
            robot = next_position
            maze[robot[0]][robot[1]] = "@"
            # move all in the direction of the move
            obstacles = ["[", "]"]
            idx = 0 if move == ">" else 1
            for i in count(1):
               next_pos = direction_func(robot[0], robot[1], i)
               maze[next_pos[0]][next_pos[1]] = obstacles[idx]
               idx = 1 - idx
               if next_pos == next_empty:
                  break
      else:
         moving_dir = -1 if move == "^" else 1
         can_move, obstacle = bfs_obstacle(*next_position, maze, moving_dir)
         if can_move:
            maze[robot[0]][robot[1]] = "."
            robot = next_position
            orig_maze = deepcopy(maze)
            new_obstacle = set()
            for row, col in obstacle:
               if (row, col) not in new_obstacle:
                  maze[row][col] = "."
               next_position = (row + moving_dir, col)
               new_obstacle.add(next_position)
               maze[next_position[0]][next_position[1]] = orig_maze[row][col]
            maze[robot[0]][robot[1]] = "@"

   # print("Move:", move)
   # print_maze(maze)

sum_coordinates = 0

for row_idx, row in enumerate(maze):
   for col_idx, col in enumerate(row):
      if col == "[":
         sum_coordinates += 100 * row_idx + col_idx

print(sum_coordinates)
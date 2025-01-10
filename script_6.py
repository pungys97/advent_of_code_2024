from itertools import count
from time import perf_counter

obstacles = set()

rows = 0
cols = 0

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

heading = UP
location = None

start_time = perf_counter()

while True:
   try:
      idx = 0
      for idx, grid_item in enumerate(list(input().strip())):
         if grid_item == '#':
            obstacles.add((rows, idx))
         elif grid_item == '^':
            location = (rows, idx)
      rows += 1
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

cols = rows


def walk_direction(location_: tuple[int, int], heading_: int, obstacles_: set[tuple[int, int]]) -> tuple[list[tuple[int, int]], bool]:
   # generate straight path from location in the direction of heading using itertools

   row_, col_ = location_

   direction_func = {
      0: lambda r, c, i: (r - i, c),  # UP: decrease row
      1: lambda r, c, i: (r, c + i),  # RIGHT: increase col
      2: lambda r, c, i: (r + i, c),  # DOWN: increase row
      3: lambda r, c, i: (r, c - i),  # LEFT: decrease col
   }[heading_]

   path = [location_, ]

   for i in count(1):
      next_pos = direction_func(row_, col_, i)
      if next_pos in obstacles_:
         return path, False
      new_row, new_col = next_pos
      if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
         return path, True
      path.append(next_pos)

original_location = location

class CycleFoundException(Exception):
   pass

def solve_maze(location_: tuple[int, int], heading_: int, obstacles_: set[tuple[int, int]]):
   visited_grid_items_with_heading = set()

   while True:
      path, is_end = walk_direction(location_, heading_, obstacles_)
      location_ = path[-1]
      original_walked_distance = len(visited_grid_items_with_heading)
      visited_grid_items_with_heading |= set([(loc, heading_) for loc in path])
      if is_end:
         break
      # if the len of visited_grid_items_with_heading does not increase by len(path), then a cycle is found
      if original_walked_distance + len(path) != len(visited_grid_items_with_heading):
         raise CycleFoundException()
      heading_ = DIRECTIONS[(heading_ + 1) % 4]

   return visited_grid_items_with_heading

res = solve_maze(location, heading, obstacles)

# only unique locations
potential_obstacles = set([loc for loc, _ in res]) - {original_location}

new_obstacles = set()

for potential_obstacle in potential_obstacles:
   try:
      solve_maze(location, heading, obstacles | {potential_obstacle})
   except CycleFoundException:
      new_obstacles.add(potential_obstacle)

print(len(new_obstacles))

print("Time taken: ", perf_counter() - start_time)

# print("maze dimensions: ", rows, cols)
# print(len(visited_grid_items))
# print("intersection: ", visited_grid_items & obstacles)
# # print the maze
# for r in range(rows):
#    line = ""
#    for c in range(cols):
#       if (r, c) == location:
#          # base on heading
#          if heading == UP:
#             line += "^"
#          elif heading == RIGHT:
#             line += ">"
#          elif heading == DOWN:
#             line += "v"
#          elif heading == LEFT:
#             line += "<"
#       elif (r, c) in found_obstacles:
#          line += "O"
#       elif (r, c) in visited_grid_items:
#          line += "X"
#       elif (r, c) in obstacles:
#          line += "#"
#       else:
#          line += "."
#    print(line)


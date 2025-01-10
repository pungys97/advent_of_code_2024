from collections import defaultdict
from functools import lru_cache

n_rows = n_cols = 71
obstacles = []

while True:
   try:
      x, y = list(map(int, input().split(",")))
      obstacles.append((y, x))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

def find_shortest_path(row, col, n_steps):
   queue = [(row, col, 0)]
   visited = set()

   obstacles_ = set(obstacles[:n_steps])

   while queue:
      row, col, steps = queue.pop(0)

      if (row, col) in visited:
         continue

      visited.add((row, col))

      if (row, col) == (n_rows - 1, n_cols - 1):
         return steps

      for drow, dcol in ((0, 1), (0, -1), (1, 0), (-1, 0)):
         new_row, new_col = row + drow, col + dcol
         if 0 <= new_row < n_rows and 0 <= new_col < n_cols and (new_row, new_col) not in visited and (new_row, new_col) not in obstacles_:
            queue.append((new_row, new_col, steps + 1))
   return -1

def print_maze():
   for i in range(n_rows):
      row = ""
      for j in range(n_cols):
         if (i, j) in obstacles:
            row += "X"
         else:
            row += "."
      print(row)


for i in range(1024, 3450, 1):
   if find_shortest_path(0, 0, i + 1) == -1:
      print(obstacles[i])
      break




from collections import defaultdict

maze = []
start_ = None
end_ = None

while True:
   try:
      row = list(input().strip())
      maze.append(row)
      if "S" in row:
         start_ = (len(maze) - 1, row.index("S"))
      if "E" in row:
         end_ = (len(maze) - 1, row.index("E"))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)


def print_maze():
   for row in maze:
      print("".join(row))


def bfs(jump_allowed=False, original=0):
   queue = [(*start_, 0, None)]
   visited = set()
   solutions = dict()
   while queue:
      y, x, length, jump = queue.pop(0)
      print(y, x, length, jump)
      if (y, x, jump) in visited:
         continue
      visited.add((y, x, jump))
      if (y, x) == end_:
         solutions[jump] = length
         print("Found solution", length, jump)
         if original - length - 1 < 100:
            break
      for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
         nx, ny = x + dx, y + dy
         if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#" and (ny, nx, jump) not in visited:
            queue.append((ny, nx, length + 1, jump))
         if not jump_allowed:
            continue
         jump_x, jump_y = x + 2 * dx, y + 2 * dy
         if jump is None and 0 <= jump_y < len(maze) and 0 <= jump_x < len(maze[0]) and maze[jump_y][jump_x] != "#" and (jump_y, jump_x, (ny, nx)) not in visited:
            queue.append((jump_y, jump_x, length + 1, (ny, nx)))
   return solutions


if __name__ == "__main__":
   solutions = bfs()
   original = solutions[None]
   print(original)
   print(bfs(True, original))


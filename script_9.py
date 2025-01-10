hiking_map = []

# start_time = perf_counter()

starts = []
row_idx = 0

while True:
   try:
      hiking_map.append(list(map(int, list(input().strip()))))
      for idx, val in enumerate(hiking_map[-1]):
         if val == 0:
            starts.append((row_idx, idx))
      row_idx += 1
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

def bfs_search_9(start, map_):
   queue = [start]
   cnt = 0
   while queue:
      current = queue.pop()
      row, col = current
      value = map_[row][col]
      if value == 9:
         cnt += 1
      # if neighbor is up, down, left, right and exactly 1 higher than current value
      if row > 0 and map_[row-1][col] == value + 1:
         queue.append((row-1, col))
      if row < len(map_) - 1 and map_[row+1][col] == value + 1:
         queue.append((row+1, col))
      if col > 0 and map_[row][col-1] == value + 1:
         queue.append((row, col-1))
      if col < len(map_[0]) - 1 and map_[row][col+1] == value + 1:
         queue.append((row, col+1))
   return cnt


print(sum(bfs_search_9(start, hiking_map) for start in starts))
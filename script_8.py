from time import perf_counter

start_time = perf_counter()

data = list(map(int, list(input().strip())))
original_data = data.copy()

get_id = lambda x : x // 2

checksum = 0

current_idx = 0

def add_to_checksum(block_id, block_size):
   global checksum
   global current_idx

   for _ in range(block_size):
      # print(f"{current_idx} * {block_id}")
      checksum += current_idx * block_id
      current_idx += 1

for i in range(0, len(data), 2):
   # handle normal case
   add_to_checksum(get_id(i), data[i])

   if i + 1 >= len(data):
      break

   if data[i] == 0:
      add_to_checksum(0, original_data[i])

   # get gap between next block
   gap_size = data[i + 1]
   last_unmoved_idx = len(data) - 1
   while last_unmoved_idx > i:
      moved_block = data[last_unmoved_idx]
      if moved_block > gap_size:
         last_unmoved_idx -= 2
      else:
         data[last_unmoved_idx] = 0
         add_to_checksum(get_id(last_unmoved_idx), moved_block)
         gap_size -= moved_block
         last_unmoved_idx -= 2
   add_to_checksum(0, gap_size)

print(checksum)
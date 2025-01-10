from collections import defaultdict
from functools import lru_cache


options = defaultdict(list)
patterns = []

reading_options = True
while True:
   try:
      if reading_options:
         line = input().strip()
         if not line:
            reading_options = False
            continue
         for option in line.split(", "):
            options[option[0]].append(option)
      else:
         patterns.append(input().strip())
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

# sort all options by length in descending order
for key in options:
   options[key].sort(key=len, reverse=True)

cnt_recursive_calls = 0

@lru_cache(maxsize=None)
def can_be_combined(pattern):
   cnt_combined = 0
   if len(pattern) == 0:
      return 1
   for option in options[pattern[0]]:
      if pattern.startswith(option):
         cnt_combined += can_be_combined(pattern[len(option):])
   return cnt_combined

count_can_be_combined = 0

for pattern in patterns:
   count_can_be_combined += can_be_combined(pattern)

print(count_can_be_combined)
print(cnt_recursive_calls)
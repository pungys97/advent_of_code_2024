import sys

data = True

def is_valid(vals, dampener = 1):
   f, s = vals[:2]
   is_increasing = f < s
   last = vals[0]
   for i, v in enumerate(vals[1:]):
      if (
        (is_increasing and 1 <= (v - last) <= 3)
         or
        (not is_increasing and 1 <= (last - v) <= 3)
      ):
         last = v
      elif dampener:
         # either remove the current element or the previous element, or we guessed the wrong direction
         return is_valid(vals[:i+1] + vals[i+2:], dampener - 1) or is_valid(vals[:i] + vals[i + 1:], dampener - 1) or is_valid(vals[1:], dampener - 1)
      else:
         return 0
   return 1

cnt = 0
cnt_invalid = 0

# parse dampener from args
damp = int(sys.argv[1])

while data:
   try:
      data = list(map(int, input().split()))
      # print("============================")
      if not is_valid(data, damp):
         print(data)
         print("not valid")
         cnt_invalid += 1
      else:
         # print("valid")
         cnt += 1
   except:
      break

print(cnt)
print(cnt_invalid)

import sys
import re

data = True

def mul(a, b):
   return a * b

all_sum = 0

do = True

while data:
   try:
      data = input()
      # regex all mul(1-3 digits number, 1-3 digits number)
      reg = r"don't\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\)"
      # find all matches
      matches = re.findall(reg, data)
      # loop through all matches and eval them
      for match in matches:
         if match == "don't()":
            do = False
         elif match == "do()":
            do = True
         elif do:
            all_sum += eval(match)
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

print(all_sum)

from itertools import zip_longest, product
from time import perf_counter

equations = dict()

start_time = perf_counter()

while True:
   try:
      line = input()
      result, equation = line.strip().split(": ")
      equations[int(result)] = list(map(int, equation.split(" ")))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

result = 0

for res, eq in equations.items():
   for operators in product(["+", "*", "||"], repeat=len(eq) - 1):
      cum_result = eq[0]
      for operand, operator in zip(eq[1:], operators):
         if operator == "+":
            cum_result += operand
         elif operator == "*":
            cum_result *= operand
         else:
            cum_result = int(str(cum_result) + str(operand))
         if cum_result > res:
            break
      if cum_result == res:
         result += res
         break

print(result)
print(f"Execution time: {perf_counter() - start_time}")
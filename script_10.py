import sys
from time import perf_counter
from functools import cache
from collections import defaultdict

data = defaultdict(int)

for input_ in list(map(int, input().strip().split())):
    data[input_] += 1

@cache
def process_data(item):
    if item == 0:
       return (1, )
    elif len(str(item)) % 2 == 0:
       stringified = str(item)
       half_idx = len(stringified) // 2
       return int(stringified[:half_idx]), int(stringified[half_idx:])
    else:
       return (item * 2024, )

def blink():
    new_data = defaultdict(int)
    for item, cnt in data.items():
        for num in process_data(item):
            new_data[num] += cnt
    return new_data


start_time = perf_counter()
blinks = int(sys.argv[1])
for i in range(blinks):
    data = blink()
    # print("idx", i, "Time elapsed: ", perf_counter() - start_time)

# print(data)
print(sum(data.values()))
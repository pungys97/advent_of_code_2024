from twisted.positioning.base import Heading

data = []

while True:
    try:
        line = list(input().strip())
        data.append(line)
    except EOFError:
        break

n_rows = n_cols = len(data)

already_accounted_for = set()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def count_fences_needed(row_idx, col_idx):
    symbol = data[row_idx][col_idx]
    # look up, down, left, right, if out of bounds add to fence count, if different symbol add to fence count
    fences_added = set()
    if row_idx - 1 < 0 or data[row_idx - 1][col_idx] != symbol:
        # print(f"fence needed up {symbol} at {row_idx, col_idx}")
        fences_added.add(((row_idx, col_idx), UP))
    if row_idx + 1 >= n_rows or data[row_idx + 1][col_idx] != symbol:
        # print(f"fence needed down {symbol} at {row_idx, col_idx}")
        fences_added.add(((row_idx, col_idx), DOWN))
    if col_idx - 1 < 0 or data[row_idx][col_idx - 1] != symbol:
        # print(f"fence needed left {symbol} at {row_idx, col_idx}")
        fences_added.add(((row_idx, col_idx), LEFT))
    if col_idx + 1 >= n_cols or data[row_idx][col_idx + 1] != symbol:
        # print(f"fence needed right {symbol} at {row_idx, col_idx}")
        fences_added.add(((row_idx, col_idx), RIGHT))
    return fences_added


def bfs_location(row_idx, col_idx):
    symbol = data[row_idx][col_idx]
    queue = [(row_idx, col_idx)]
    visited_set = set()

    fences_needed = set()

    while queue:
        current_row, current_col = queue.pop(0)
        if (current_row, current_col) in visited_set:
            continue
        visited_set.add((current_row, current_col))
        fences_needed.update(count_fences_needed(current_row, current_col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < n_rows and 0 <= new_col < n_cols and data[new_row][new_col] == symbol and (new_row, new_col) not in visited_set:
                queue.append((new_row, new_col))

    return fences_needed, visited_set


def clean_fences_needed(fences_needed):
    cleaned_fences = set()
    for fence in fences_needed:
        (row_idx, col_idx), heading = fence
        # look left and same heading not in fences_needed then add it
        if (heading == UP or heading == DOWN) and ((row_idx, col_idx - 1), heading) not in fences_needed:
            cleaned_fences.add(fence)
        elif (heading == LEFT or heading == RIGHT) and ((row_idx - 1, col_idx), heading) not in fences_needed:
            cleaned_fences.add(fence)
    return cleaned_fences

total_price = 0

for row_idx in range(n_rows):
    for col_idx in range(n_cols):
        if (row_idx, col_idx) not in already_accounted_for:
            fences_needed, visited_set = bfs_location(row_idx, col_idx)
            cleaned_fences = len(clean_fences_needed(fences_needed))
            # print(f"symbols: {data[row_idx][col_idx]}, cleaned fences: {cleaned_fences}, visited_set: {visited_set}")
            total_price += cleaned_fences * len(visited_set)
            already_accounted_for.update(visited_set)

print(total_price)
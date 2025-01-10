data = []

while True:
   try:
      data.append(list(input().strip()))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

rows_max = len(data) - 1
cols_max = len(data[0]) - 1

found_xmas = 0

# part 1
# for row_i, row in enumerate(data):
#    for col_i, character in enumerate(row):
#       if character not in ['X', 'S']:
#          continue
#       looking_for = 'XMAS' if character == 'X' else 'SAMX'
#       # row
#       if "".join(row[col_i: col_i + 4]) == looking_for:
#          # print(f"found horizontal {looking_for} {row_i=}, {col_i=}")
#          found_xmas += 1
#
#       # column
#       if row_i + 3 <= rows_max:
#          if "".join([data[row_i + i][col_i] for i in range(4)]) == looking_for:
#             # print(f"found vertical {looking_for} {row_i=}, {col_i=}")
#             found_xmas += 1
#
#       # down right
#       if row_i + 3 <= rows_max and col_i + 3 <= cols_max:
#          if "".join([data[row_i + i][col_i + i] for i in range(4)]) == looking_for:
#             # print(f"found down right {looking_for} {row_i=}, {col_i=}")
#             found_xmas += 1
#
#
#       # down left
#       if row_i + 3 <= rows_max and col_i - 3 >= 0:
#          if "".join([data[row_i + i][col_i - i] for i in range(4)]) == looking_for:
#             # print(f"found down left {looking_for} {row_i=}, {col_i=}")
#             found_xmas += 1

# part 2
for row_i, row in enumerate(data):
   for col_i, character in enumerate(row):
      if character != "A" or not (0 < row_i < rows_max and 0 < col_i < cols_max):
         continue
      top_left_character = data[row_i - 1][col_i - 1]
      top_right_character = data[row_i - 1][col_i + 1]
      bottom_left_character = data[row_i + 1][col_i - 1]
      bottom_right_character = data[row_i + 1][col_i + 1]

      diag_words = [top_left_character + character + bottom_right_character,
                    top_right_character + character + bottom_left_character]

      if all(word in ["MAS", "SAM"] for word in diag_words):
         found_xmas += 1

print(found_xmas)
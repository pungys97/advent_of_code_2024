import re

# start_time = perf_counter()

robot_positions = []
robot_velocities = []
rows = 103
cols = 101

def print_maze():
   for r in range(rows):
      row = ""
      for c in range(cols):
         if (r, c) in robot_positions:
            # find all occurrences of the robot in the list
            occurrences = [i for i, x in enumerate(robot_positions) if x == (r, c)]
            row += str(len(occurrences))
         else:
            row += "."
      print(row)

while True:
   try:
      # find all the numbers in the string, can be negative
      x, y, v_x, v_y = re.findall(r'-*\d+', input())
      robot_positions.append((int(y), int(x)))
      robot_velocities.append((int(v_y), int(v_x)))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

def walk_robot(pos, vel):
   return (pos[0] + vel[0]) % rows, (pos[1] + vel[1]) % cols

def quadrants_count(positions):
   q = 4 * [0]
   for pos in positions:
      if pos[0] < rows // 2 and pos[1] < cols // 2:
         q[0] += 1
      elif pos[0] < rows // 2 and pos[1] > cols // 2:
         q[1] += 1
      elif pos[0] > rows // 2 and pos[1] < cols // 2:
         q[2] += 1
      elif pos[0] > rows // 2 and pos[1] > cols // 2:
         q[3] += 1
   return q

n_seconds = 10_000

# print_maze()

for i in range(n_seconds):
   new_positions = []
   for pos, vel in zip(robot_positions, robot_velocities):
      new_positions.append(walk_robot(pos, vel))
   robot_positions = new_positions
   # at least 80% of robots are in the middle 3rd of cols
   if (len([pos for pos in robot_positions if cols // 3 < pos[1] < 2 * cols // 3]) / len(robot_positions)) > 0.7:
      print(f"###############{i+1}###############")
      print_maze()

q1, q2, q3, q4 = quadrants_count(robot_positions)
# print(q1 * q2 * q3 * q4)


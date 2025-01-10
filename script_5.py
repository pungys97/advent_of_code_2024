import networkx as nx
from collections import defaultdict
from networkx.algorithms.dag import topological_sort
from pygments.lexer import default

updates = []

graph = nx.DiGraph()

while True:
   try:
      line = input().strip()
      if "|" in line:
         s, t = list(map(int, line.split("|")))
         graph.add_edge(s, t)
      if "," in line:
         updates.append(list(map(int, line.split(","))))
   except EOFError as e:
      break
   except Exception as e:
      print(e)
      sys.exit(1)

def get_top_sort_idx_of_subgraph(nodes):
   top_sort_idx = defaultdict(lambda: 100)

   idx = 0
   for node in nx.topological_sort(nx.subgraph(graph, nodes)):
      top_sort_idx[node] = idx
      idx += 1

   return top_sort_idx

# part 1
sum_of_middle = 0
sum_of_corrected_middle = 0

for update in updates:
   top_sort_idx = get_top_sort_idx_of_subgraph(update)
   previous_index = top_sort_idx[update[0]]
   is_valid = True
   for page_number in update[1:]:
      current_index = top_sort_idx[page_number]
      if current_index < previous_index:
         is_valid = False
         break
      previous_index = current_index
   # part 1
   if is_valid:
      # add the middle number
      sum_of_middle += update[int(len(update) / 2)]
   # part 2
   else:
      # add the middle number
      sum_of_corrected_middle += list(top_sort_idx.keys())[int(len(update) / 2)]

print(sum_of_middle)
print(sum_of_corrected_middle)
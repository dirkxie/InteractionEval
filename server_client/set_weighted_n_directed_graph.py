#   '1'-5-'2'-2-'3'
#    |     |     |
#    7     3     8
#    |     |     |
#   '4'-1-'5'-6-'6'
#    |     |     |
#    3     1     4  
#    |     |     |
#   '7'-5-'8'-9-'9'

from dijkstar import Graph, find_path

graph = None 
cost_func = None

def directed_and_guided_map_init ():
  graph = None
  cost_func = None
  graph = Graph()
# 4 real beacons
  graph.add_edge(1, 2, {'cost': 3})
  graph.add_edge(2, 1, {'cost': 3})
  graph.add_edge(2, 3, {'cost': 4})
  graph.add_edge(3, 2, {'cost': 4})
  graph.add_edge(1, 7, {'cost': 4})
  graph.add_edge(7, 1, {'cost': 4})
# 3 virtual beacons that does not actually exist
  graph.add_edge(3, 4, {'cost': 5})
  graph.add_edge(4, 3, {'cost': 5})
  graph.add_edge(3, 5, {'cost': 5})
  graph.add_edge(5, 3, {'cost': 5})
  graph.add_edge(2, 5, {'cost': 6})
  graph.add_edge(5, 2, {'cost': 6})
  graph.add_edge(1, 6, {'cost': 7})
  graph.add_edge(6, 1, {'cost': 7})

  cost_func = lambda u, v, e, prev_e: e['cost']

  return graph, cost_func

#def main():
  #directed_and_guided_map_init()
  #a, b, c, d = find_path(graph, 7, 2, cost_func=cost_func)
  #print a

#main()

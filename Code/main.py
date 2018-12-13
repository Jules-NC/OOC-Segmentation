import sys
from Code.Graph import *
from Code.Image import *
from Code.Block import *
from Code.Server2 import *
#   from Code.GraphPrinter import *


sys.setrecursionlimit(15000)

IMAGE.len_x = 6
IMAGE.len_y = 1

boundary_1 = Border(0, 0, 2, 0)
boundary_2 = Border(3, 0, 5, 0)

graph_1 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[3, 7])
graph_2 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[6, 8])

print("TEST")

block_1 = Block(graph_1, boundary_1)
block_2 = Block(graph_2, boundary_2)

print("TEST")
#   print_three_trees([block_1.get_subtree(1), block_2.get_subtree(4)], figsize=(20, 10))

# server = Server(block_1, block_2, (1, 4), 4)
server2 = Server2(3,3)
border = block_1.get_border_tree([1, 2])

server2.merging(block_1, block_2, [(1, 4)], [4])
# server.merging()
pass
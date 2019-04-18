import sys
from Code.Graph import *
from Code.Image import *
from Code.Block import *
from Code.Server import *
#   from Code.GraphPrinter import *


sys.setrecursionlimit(15000)

# set the image size
IMAGE.len_x = 6
IMAGE.len_y = 1

#create borders
boundary_1 = Border(0, 0, 2, 0)
boundary_2 = Border(3, 0, 5, 0)

#create graphs
graph_1 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[3, 7])
graph_2 = Graph(n_vertices=3, edges=[(0, 1), (1, 2)], weights=[6, 8])

print("TEST")

# set blocks
block_1 = Block(graph_1, boundary_1)
block_2 = Block(graph_2, boundary_2)

print("TEST")
#   print_three_trees([block_1.get_subtree(1), block_2.get_subtree(4)], figsize=(20, 10))

# create a server that will merge block 1 and block 2 on the specified border
server = Server(block_1, block_2, (1, 4), 4)

#merge the two blocks
#server.compute()
server.compute()
server.merging()

pass

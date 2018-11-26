import sys
sys.setrecursionlimit(15000)

from Graph import *
from Image import *
from GraphPrinter import *
from Block import *
from Server import *

IMSIZE = ImageSize(6, 1)
boundary_1 = Border(0, 0, 2, 0)
boundary_2 = Border(3, 0, 5, 0)

graph_1 = Graph(n_vertices=3, edges=[(0,1), (1,2)], weights=[3, 7])
graph_2 = Graph(n_vertices=3, edges=[(0,1), (1,2)], weights=[6, 8])

block_1 = Block(graph_1, boundary_1, IMSIZE)
block_2 = Block(graph_2, boundary_2, IMSIZE)

#print_three_trees([block_1.get_subtree(1), block_2.get_subtree(4)], figsize=(20, 10))

server = Server(block_1, block_2, (1, 4), 4)

server.compute()
print(block_1.tree)
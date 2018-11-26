import sys
sys.setrecursionlimit(15000)

from Graph import *
from QBT import *
from Image import *
from GraphPrinter import *
from Block import *
from Server import *

IMSIZE = ImageSize(6, 1)
boundary_1 = Boundary(0,0,2,0)
boundary_2 = Boundary(3,0,5,0)

graph_1 = Graph(n_vertices=3, edges=[(0,1), (1,2)], weights=[3, 7], boundary=boundary_1)
graph_2 = Graph(n_vertices=3, edges=[(0,1), (1,2)], weights=[6, 8], boundary=boundary_2)

block_1 = Block(graph_1, IMSIZE)
block_2 = Block(graph_2, IMSIZE)

#print_three_trees([block_1.get_subtree(1), block_2.get_subtree(4)], figsize=(20, 10))

server = Server(block_1, block_2, (1, 4), 4)

server.compute()

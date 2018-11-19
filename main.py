import sys
sys.setrecursionlimit(15000)

from Graph import *
from QBT import *
from Image import *
from GraphPrinter import *
from Block import *
from Server import *

IMSIZE = ImageSize(4, 2)
boundary_1 = Boundary(0,0,1,1)
boundary_2 = Boundary(2,0,3,1)
boundary_W = Boundary(0,0,3,1)


graph_1 = Graph(n_vertices=4, edges=[(0,1), (1,3), (3,2), (2,0)], weights=[2, 2, 1, 0], boundary=boundary_1)
graph_2 = Graph(n_vertices=4, edges=[(0,1), (1,3), (3,2), (2,0)], weights=[0, 1, 0, 3], boundary=boundary_2)
graph_W = Graph(n_vertices=8, edges=[(0,1), (1,2), (2,3), (7,6), (5,4), (0,4), (1,5), (2,6), (3,7)], weights=[2, 2, 0, 0, 1, 0, 2, 3, 1], boundary=boundary_W)

print_three_trees([do_QBT(graph_1, IMSIZE), do_QBT(graph_2, IMSIZE), do_QBT(graph_W, IMSIZE)], figsize=(20, 10))


block_1 = Block(graph_1, IMSIZE)
block_2 = Block(graph_2, IMSIZE)


server = Server(block_1, block_2, (0, 2), 2)
tree_bloc_1 = server.subtree_1

print_tree(tree_bloc_1, figsize=(10, 5))

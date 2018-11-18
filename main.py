import sys
sys.setrecursionlimit(15000)

from Graph import *
from QBT import *
from Image import *
from GraphPrinter import *

IMSIZE = ImageLen(4,2)
boundary1 = Boundary(0,0,1,1)
boundary2 = Boundary(2,0,3,1)
boundaryW = Boundary(0,0,3,1)

graph1 = Graph(n_vertices=4, edges=[(0,1), (1,3), (3,2), (2,0)], weights=[2, 2, 1, 0], boundary=boundary1)
graph2 = Graph(n_vertices=4, edges=[(0,1), (1,3), (3,2), (2,0)], weights=[0, 1, 0, 3], boundary=boundary2)
graphW = Graph(n_vertices=8, edges=[(0,1), (1,2), (2,3), (7,6), (5,4), (0,4), (1,5), (2,6), (3,7)], weights=[2, 2, 0, 0, 1, 0, 2, 3, 1], boundary=boundaryW)


node1 = do_QBT(graph1, IMSIZE)[0].root()
node2 = do_QBT(graph2, IMSIZE)[0].root()


nodes_1 = do_QBT(graph1, IMSIZE)
nodes_2 = do_QBT(graph2, IMSIZE)
nodes_W = do_QBT(graphW, IMSIZE)


IMSIZE = ImageLen(5,3)
gr = generate_graph(IMSIZE)
nodes_G = do_QBT(gr, IMSIZE)
print(nodes_G[-1])
write_QBT(nodes_G)
print_QBT(nodes_G, figsize=(30, 30))

print(nodes_G[-1].max_height())
print(len(nodes_G))
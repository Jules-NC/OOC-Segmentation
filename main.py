import sys
sys.setrecursionlimit(15000)

from Graph import *
from QBT import *
from Image import *
from GraphPrinter import *

IMSIZE = ImageSize(4, 2)
boundary1 = Boundary(0,0,1,1)


graph1 = Graph(n_vertices=4, edges=[(0,1), (1,3), (3,2), (2,0)], weights=[2, 2, 1, 0], boundary=boundary1)

tree_1 = do_QBT(graph1, IMSIZE)

write_QBT(tree_1)
print_qbt(tree_1, figsize=(30, 30))

print(tree_1.height())

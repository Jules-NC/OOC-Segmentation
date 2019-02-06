import sys
# from Code.Graph import *
# from Code.Image import *
# from Code.Block import *
from Code.Server import *
#   from Code.GraphPrinter import *


sys.setrecursionlimit(15000)

IMAGE.len_x = 4
IMAGE.len_y = 2

server2 = Server(IMAGE.len_x, IMAGE.len_y, 2, 1, "Teste1")

weights = [1, 2, 2, 0, 3, 1, 0, 4, 0, 3]

server2.initiate(weights)
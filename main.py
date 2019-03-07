import sys
from Code.Image import *
from Code.Server import *

sys.setrecursionlimit(15000)

IMAGE.len_x = 4
IMAGE.len_y = 2

server2 = Server(IMAGE.len_x, IMAGE.len_y, 2, 1, "Test_Original")

#weights = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# The weights:
# o--0--o--1--o
# |     |     |
# 2     3     4
# |     |     |
# o--5--o--6--o

# weights = [2, 3, 4, 2, 5, 10, 3, 2, 7, 6, 8, 21, 12, 10, 4, 2, 7, 3, 4, 2, 5, 10, 8, 2]
weights = [4, 1, 7, 5, 8, 3, 6, 9, 2, 10]
#weights = [3, 2, 5, 4, 6, 3, 8, 7, 1, 9]
server2.initiate(weights)
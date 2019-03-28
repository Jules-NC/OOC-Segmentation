from Code.Graph import *
from Code.Merge import *
import random
import os
# New Server


class Server:
    # New definition for the server
    # +image
    def __init__(self, img_x, img_y, x_blocks, y_blocks, file_name):
        # Number of blocks by column and by row
        self.num_x_blocks = x_blocks
        self.num_y_blocks = y_blocks

        # Size of the image x and y
        self.img_x = img_x
        self.img_y = img_y

        # Number of blocks
        self.n_blocks = x_blocks * y_blocks

        # Size x and y of each block
        self.x_length = round(img_x / self.num_x_blocks)
        self.y_length = round(img_y / self.num_y_blocks)

        # Area of the block
        self.block_size = (self.x_length * self.y_length)

        # Initiate all_edges
        self.all_edges = []

        # Beging output file
        self.file_name = file_name
        directory = "Data/"+str(self.file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.f = open(directory+"/"+str(self.file_name)+".txt", "w")

        # Initiate all_blocks
        self.all_blocks = []

    def initiate(self, weights):
        assert len(weights) == (self.img_x*self.img_y*2)-(self.img_x+self.img_y)
        print("Initiating graph...")
        self.generate_all_edges()
        print("Initiating blocks...")
        self.generate_all_blocks(weights)
        print("Merging blocks...")
        merge = Merge(self.all_blocks, weights, self.img_x, self.img_y, self.num_x_blocks, self.num_y_blocks,
                      self.x_length, self.y_length, self.f)
        merge.merge_all()
        self.refactor()
        self.print_all()
        self.f.close()

    def refactor(self):
        wrong_nodes = []
        copy_wrong_nodes = []
        for a in self.all_blocks:
            for node in a.tree.nodes:
                n = node.name
                if n not in wrong_nodes:
                    if node.left is None or node.right is None:
                        wrong_nodes.append(n)
                        copy_wrong_nodes.append(node.copy_all())

        for a in self.all_blocks:
            for node in a.tree.nodes:
                n = node.name
                copy_n = node.copy_all()
                if n in wrong_nodes:
                    same = wrong_nodes.index(n)
                    # left child
                    if copy_n[3] != copy_wrong_nodes[same][3]:
                        if copy_wrong_nodes[same][4] is None:
                            copy_wrong_nodes[same][4] = copy_n[3]
                    elif copy_n[3] != copy_wrong_nodes[same][4]:
                        if copy_wrong_nodes[same][3] is None:
                            copy_wrong_nodes[same][3] = copy_n[3]

                    if copy_n[4] != copy_wrong_nodes[same][3]:
                        if copy_wrong_nodes[same][4] is None:
                            copy_wrong_nodes[same][4] = copy_n[4]
                    elif copy_n[4] != copy_wrong_nodes[same][4]:
                        if copy_wrong_nodes[same][3] is None:
                            copy_wrong_nodes[same][3] = copy_n[4]

        w1 = []
        for w in copy_wrong_nodes:
            if w[3] is None and w[4] is None:
                w1.append(w)
            if w[3] != w[4] and w[3] is not None and w[4] is not None:
                w1.append(w)
        for w in w1:
            wrong_nodes.remove(w[1])
            copy_wrong_nodes.remove(w)

        for w in wrong_nodes:
            print(w)

        for a in self.all_blocks:
            a.remove_node(wrong_nodes)


    def print_all(self):
        for b in self.all_blocks:
            b.block_print_tree()

    def generate_all_edges(self):
        # 4-connected edges
        for i in range(self.block_size - 1):
            if i % self.x_length < self.x_length - 1:
                self.all_edges.append((i, i + 1))
            if i + self.x_length < self.block_size:
                self.all_edges.append((i, i + self.x_length))

    def generate_block(self, x, y, weights):
        self.f.write("Block %d," % x)
        self.f.write("%d (Original)\n" % y)
        block = self.define_block(x, y, weights)
        self.all_blocks.append(block)

        self.f.write("All altitudes and nodes: \n")
        for node in block.tree.nodes:
            self.f.write("{0} ".format(node.altitude))
            self.f.write("{0}\n".format(node.name))

    def generate_all_blocks(self, weights):
        for y in range(self.num_y_blocks):
            for x in range(self.num_x_blocks):
                print(" Block ("+str(x)+","+str(y)+")")
                weights_of_block = []
                # Where the block begins
                initial = (x * self.x_length) + (y * self.y_length) * self.img_x
                print("Initial node: " + str(initial))
                for j in range(self.y_length):
                    # first indexes on the horizontal
                    i = 0
                    w = initial + (2*self.img_x-1)*j + y*(self.img_x-1)
                    while i < self.x_length-1:
                        weights_of_block.append(weights[w])
                        i = i + 1
                        w = w + 1
                    # then indexes on the vertical
                    w = w + self.img_x-self.x_length
                    i = 0
                    if j < self.y_length-1:
                        while i < self.x_length:
                            weights_of_block.append(weights[w])
                            i = i + 1
                            w = w + 1

                print(" Weights", weights_of_block)
                self.generate_block(x, y, weights_of_block)

    def define_border(self, index_x, index_y):
        start_x = index_x*self.x_length
        start_y = index_y*self.y_length
        end_x = ((index_x+1) * self.x_length) - 1
        end_y = ((index_y+1) * self.y_length) - 1
        return Border(start_x, start_y, end_x, end_y)

    def define_graph(self, index_x, index_y, weights=[]):
        if weights is None:
            for i in range(self.block_size - 1):
                if i % self.x_length < self.x_length - 1:
                    shift = index_x * self.x_length
                    # pixel position in the image
                    # 0 - 1 - 2 - 3
                    # |   | | |   |
                    # 4 - 5 - 6 - 7
                    # if x_lenght = 2 then block 1
                    # 0 - 1                         0 - 1
                    # |   |  - but in the block ->  |   |
                    # 4 - 5                         2 - 3
                    # and block 2:
                    # 2 - 3                         0 - 1
                    # |   |  - but in the block ->  |   |
                    # 6 - 7                         2 - 3
                    # to find the real weights on the image we need the real values
                    # THESE ARE NOT REAL NUMBERS!
                    # random weights
                    weights.append(random.randint(0, 255))
                if i + self.x_length < self.block_size:
                    weights.append(random.randint(0, 255))
        return Graph(n_vertices=self.block_size, edges=self.all_edges, weights=weights)

    def define_block(self, index_x, index_y, weight=[]):
        # define the edges of each block depending on its index
        # the blocks are defined by their position (x,y) in the image
        #
        border = self.define_border(index_x, index_y)
        graph = self.define_graph(index_x, index_y, weight)
        return Block(graph, border, (index_y*self.num_x_blocks+index_x), self.file_name)


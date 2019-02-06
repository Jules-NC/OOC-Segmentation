from Code.Block import *
from Code.Graph import *

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

        # Nodes that are being merged
        self.current_merge_name_1 = None
        self.current_merge_name_2 = None

        # Initiate all_edges
        self.all_edges = []

        # Beging output file
        self.f = open(str(file_name), "w")

        # Initiate all_blocks
        self.all_blocks = []

    def initiate(self, weights=[]):
        print("Initiating graphs...")
        self.generate_all_edges()
        print("Initiating blocks...")
        self.generate_all_blocks(weights)
        print("Merging blocks...")
        self.merge_all(weights)

    def generate_all_edges(self):
        # 4-connected edges
        for i in range(self.block_size - 1):
            if i % self.x_length < self.x_length - 1:
                self.all_edges.append((i, i + 1))
            if i + self.x_length < self.block_size:
                self.all_edges.append((i, i + self.x_length))

    def generate_block(self, x, y, weight=[]):
        self.f.write("Block %d," % x)
        self.f.write("%d (Original)\n" % y)
        block = self.define_block(x, y, weight)
        self.all_blocks.append(block)

        self.f.write("All altitudes and nodes: \n")
        for node in block.tree.nodes:
            self.f.write("{0} ".format(node.altitude))
            self.f.write("{0}\n".format(node.name))

    def generate_all_blocks(self, weights=[]):

        for y in range(self.num_y_blocks):
            for x in range(self.num_x_blocks):
                print(" Block ("+str(x)+","+str(y)+")")
                weights_of_block = []
                # In which block we are
                index = (y + 1) * x

                for j in range(self.y_length):
                    w = index * self.x_length + (j*(self.img_x*2-1))
                    for i in range(self.x_length-1):
                        weights_of_block.append(weights[w])
                        if j < self.y_length-1:
                            w = w + self.img_x - 1
                            weights_of_block.append(weights[w])
                            w = w+1
                            weights_of_block.append(weights[w])


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
                    weights.append(i + shift + i + shift + 1)
                if i + self.x_length < self.block_size:
                    weights.append(i + shift + i + shift + self.x_length)
        return Graph(n_vertices=self.block_size, edges=self.all_edges, weights=weights)

    def define_block(self, index_x, index_y, weight=[]):
        # define the edges of each block depending on its index
        # the blocks are defined by their position (x,y) in the image
        #
        border = self.define_border(index_x, index_y)
        graph = self.define_graph(index_x, index_y, weight)
        return Block(graph, border, (index_y*self.num_x_blocks+index_x))

    def merge_all(self, weights=[]):
        self.f.write("\n-------------------------------------------")
        for y in range(self.num_y_blocks):
            for x in range(self.num_x_blocks):

                self.f.write("\nBlock %d," % x)
                self.f.write("%d (Final)\n" % y)

                index = y * self.num_x_blocks + x
                block_1 = self.all_blocks[index]

                # First merge horizontally
                if x+1 < self.num_x_blocks:
                    block_2 = self.all_blocks[index+1]
                    print(" Block " + str(index) + " and Block " + str(index+1))
                    # define border
                    edges = []
                    for i in range(self.num_y_blocks+1):
                        left = (y * self.num_y_blocks + i) * self.img_x + ((x + 1) * self.num_x_blocks - 1)
                        w = left + (i*(self.img_x-1))
                        right = left + 1
                        # NOT REAL VALUES
                        if weights is None:
                            edges.append((left, right, left+right))
                        else:
                            edges.append((left, right, weights[w]))

                    self.merging(block_1, block_2, edges)

                # Second merge vertically
                if y+1 < self.num_y_blocks:
                    block_2 = self.all_blocks[index + self.num_x_blocks]
                    print(" Block " + str(index) + " and Block " + str(index + self.num_x_blocks))
                    # define border
                    edges = []
                    for i in range(self.num_x_blocks+1):
                        above = x * self.num_x_blocks + (((y + 1) * self.num_y_blocks - 1) * self.img_x) + i
                        below = above + self.img_x
                        w = above + self.img_x - 1

                        # NOT REAL VALUES
                        if weights is None:
                            edges.append((above, below, above + below))
                        else:
                            edges.append((above, below, weights[w]))

                    self.merging(block_1, block_2, edges)

                self.f.write("Nodes: \n")
                self.f.write("Altitude Nodes Parent Left Right: \n")
                for node in block_1.tree.nodes:
                    self.f.write("{0}\n".format(node))

        self.f.close()

    def merging(self, block_1, block_2, edges):
        edges.sort(key=lambda edges: edges[2])

        nodes_1 = [edge[0] for edge in edges]
        nodes_2 = [edge[1] for edge in edges]
        altitudes = [edge[2] for edge in edges]

        # edges belonging to block 1
        subtree_1 = block_1.get_border_tree(nodes_1)
        # edges belonging to block 2
        subtree_2 = block_2.get_border_tree(nodes_2)

        for i, edge in enumerate(edges):
            # names of the merging nodes in order to create the name of the new node
            self.current_merge_name_1 = str(edge[0])
            self.current_merge_name_2 = str(edge[1])

            print("  Node " + str(self.current_merge_name_1) + " and Node " + str(self.current_merge_name_2))
            print("   At altitude " + str(altitudes[i]))

            # Initiating selectors up and down
            selector_1_down = subtree_1.find_leaf(edge[0])
            selector_2_down = subtree_2.find_leaf(edge[1])

            selector_1_up = selector_1_down.parent
            selector_2_up = selector_2_down.parent

            # Computing the border tree
            new_tree_nodes = self.compute(altitudes[i], selector_1_down, selector_2_down, selector_1_up, selector_2_up)

            # Updating blocks with their respective boundary trees
            update_block_1 = new_tree_nodes.leaves_subtree(nodes_1)
            block_1.update_tree(update_block_1, nodes_1)

            update_block_2 = new_tree_nodes.leaves_subtree(nodes_2)
            block_2.update_tree(update_block_2, nodes_2)

    def compute(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        # Initializing variables
        new_tree_nodes = []
        node_created = False
        current_node = None
        # do the merging while both selectors are not the same (the root)
        while selector_1_up is not selector_2_up:
            #  If the node is not created yet we go up in both trees until we find an altitude that is higher then what
            # we are merging
            if node_created is False:
                new_tree_nodes.append(selector_1_down)
                new_tree_nodes.append(selector_2_down)
                #  If both selectors up are roots of they respective trees, we create the node
                if selector_1_up.is_root() and selector_2_up.is_root():
                    [current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up] = self.create_node(
                                                                                        altitude, selector_1_down,
                                                                                        selector_2_down, selector_1_up,
                                                                                        selector_2_up)
                    new_tree_nodes.append(current_node)
                    current_node = current_node.parent
                    node_created = True
                    # STEP 3) Update the good selector
                    if selector_1_up is current_node:
                        [selector_1_down, selector_1_up] = self.update_selector(node_created,
                                                                                selector_1_down, selector_1_up,
                                                                                altitude)
                    elif selector_2_up is current_node:
                        [selector_2_down, selector_2_up] = self.update_selector(node_created,
                                                                                selector_2_down, selector_2_up,
                                                                                altitude)

                #  If the altitude of both selectors up are higher than the altitude of the edge to merge
                elif selector_1_up.altitude >= altitude and selector_2_up.altitude >= altitude:
                    [current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up] = self.create_node(
                                                                                        altitude, selector_1_down,
                                                                                        selector_2_down, selector_1_up,
                                                                                        selector_2_up)
                    new_tree_nodes.append(current_node)
                    current_node = current_node.parent
                    node_created = True
                    # Update the good selector
                    if selector_1_up is current_node:
                        [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                                selector_1_up,
                                                                                altitude)
                    elif selector_2_up is current_node:
                        [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down,
                                                                                selector_2_up,
                                                                                altitude)
                else:
                    [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                            selector_1_up, altitude)
                    [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down,
                                                                            selector_2_up, altitude)

            #  When the node was created but is not the root
            if selector_1_up is not selector_2_up:
                if node_created is True:
                    current_node.unbind_parent()
                    current_node.bind_parent(self.min_selectors_up(node_created, selector_1_up, selector_2_up,
                                                                   selector_1_down, selector_2_down, current_node))

                    new_tree_nodes.append(current_node)

                    [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                            selector_1_up, altitude)
                    [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down,
                                                                            selector_2_up, altitude)

                    if current_node.is_root() is False:
                        current_node = current_node.parent
        return Tree(new_tree_nodes)

    def create_node(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        # Define the parent of the new node by choosing the one with the lower altitude
        parent = self.min_selectors_up(False, selector_1_up, selector_2_up, selector_1_down, selector_2_down, None)

        # If the minimum selector has an altitude less than what we are looking for, this new node is a root, and the
        # parent is None
        if parent.altitude < altitude:
            parent = None
            selector_1_down = selector_1_up
            selector_2_down = selector_2_up

        # Create the node and link the node to his parent and to his childs
        if not selector_1_down.is_root():
            selector_1_down.unbind_parent()
        if not selector_2_down.is_root():
            selector_2_down.unbind_parent()

        # Create the new Node
        current_node = Node(name="("+self.current_merge_name_1+","+self.current_merge_name_2+")*",
                                 altitude=altitude,
                                 parent=parent,
                                 left=selector_1_down,
                                 right=selector_2_down)

        if parent is None:
            selector_1_up = selector_2_up = current_node

        return list((current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up))

    def min_selectors_up(self, node_created, selector_1_up, selector_2_up, selector_1_down, selector_2_down, current_node):
        if node_created is False:
            #  If both are root => root is the next selector
            if selector_1_up.altitude == selector_2_up.altitude:
                if selector_1_up.altitude > selector_1_down.altitude:
                    return selector_1_up
                else:
                    return selector_2_up
            elif selector_1_up.altitude > selector_2_up.altitude:
                return selector_2_up
            else:
                return selector_1_up
        else:
            if current_node.is_root() and current_node is selector_1_up:
                return selector_2_up

            if current_node.is_root() and current_node is selector_2_up:
                return selector_1_up

            if selector_1_up.altitude > selector_2_up.altitude:
                return selector_2_up
            else:
                return selector_1_up

    def update_selector(self, node_created, selector_down, selector_up, altitude):
        # If the altitude of the selector up is lower than the altitude of the edge, we increment the selector
        if node_created is False:
            if selector_up.altitude < altitude:
                selector_down = selector_up
                if selector_up.parent is not None:
                    selector_up = selector_up.parent
        else:
            selector_down = selector_up
            if selector_up.parent is not None:
                selector_up = selector_up.parent
        return selector_down, selector_up


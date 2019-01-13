from Code.Node import *
from Code.Tree import *
from Code.Block import *
from Code.Border import *
from Code.Graph import *

# It probqbly zorks


class Server2:
    # New definition for the server
    # +image
    def __init__(self, img_x, img_y, x_blocks, y_blocks):
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        self.img_x = img_x
        self.img_y = img_y
        self.n_blocks = x_blocks * y_blocks
        self.x_length = round(img_x / self.x_blocks)
        self.y_length = round(img_y / self.y_blocks)
        self.block_size = (self.x_length * self.y_length)

        self.current_merge_name_1 = None
        self.current_merge_name_2 = None

        self.all_edges = []
        for i in range(self.block_size-1):
            if i % self.x_length < self.x_length-1:
                self.all_edges.append((i, i+1))
            if i+self.x_length < self.block_size:
                self.all_edges.append((i, i+self.x_length))
        self.f = open("all_blocks.txt", "w+")
        self.all_blocks = []
        for y in range(self.y_blocks):
            for x in range(self.x_blocks):
                self.f.write("Block %d," % x)
                self.f.write("%d (Original)\n" % y)
                block = self.define_block(x, y)
                self.all_blocks.append(block)

                self.f.write("All altitudes and nodes: \n")
                for node in block.tree.nodes:
                    self.f.write("{0} ".format(node.altitude))
                    self.f.write("{0}\n".format(node.name))


    # TO-DO
    def define_border(self, index_x, index_y):
        start_x = index_x*self.x_length
        start_y = index_y*self.y_length
        end_x = ((index_x+1) * self.x_length) - 1
        end_y = ((index_y+1) * self.y_length) - 1
        return Border(start_x, start_y, end_x, end_y)

    def define_graph(self, index_x, index_y):
        weights = []
        for i in range(self.block_size-1):
            if i % self.x_length < self.x_length - 1:
                shift = index_x*self.x_length
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
                ## THESE ARE NOT REAL NUMBERS!
                weights.append(i+shift + i+shift+1)
            if i + self.x_length < self.block_size:
                weights.append(i+shift + i+shift+self.x_length)

        return Graph(n_vertices=self.block_size, edges=self.all_edges, weights=weights)

    def define_block(self, index_x, index_y):
        # define the edges of each block depending on its index
        # the blocks are defined by their position (x,y) in the image
        #
        border = self.define_border(index_x, index_y)
        graph = self.define_graph(index_x, index_y)

        return Block(graph, border)


    def merge_all(self):
        self.f.write("\n-------------------------------------------")
        for y in range(self.y_blocks):
            for x in range(self.x_blocks):
                self.f.write("Block %d," % x)
                self.f.write("%d (Final)\n" % y)

                index = y * self.x_blocks + x
                block_1 = self.all_blocks[index]

                # First merge horizontally
                if x+1 < self.x_blocks:
                    block_2 = self.all_blocks[index+1]

                    # define border
                    edges = []
                    altitudes = []
                    for i in range(self.y_blocks):
                        left = (y*self.y_blocks+i)*self.img_x + ((x+1)*self.x_blocks - 1)
                        right = left + 1
                        edges.append((left, right))
                        # NOT REAL VALUES
                        altitudes.append(left+right)

                    self.merging(block_1, block_2, edges, altitudes)

                # Second merge vertically
                if y+1 < self.y_blocks:
                    block_2 = self.all_blocks[index + self.x_blocks]

                    # define border
                    edges = []
                    altitudes = []
                    for i in range(self.x_blocks):
                        above = x*self.x_blocks + (((y+1) * self.y_blocks - 1) * self.img_x) + i
                        below = above + self.img_x
                        edges.append((above, below))
                        # NOT REAL VALUES
                        altitudes.append(above + below)
                    self.merging(block_1, block_2, edges, altitudes)

                self.f.write("Nodes: \n")
                self.f.write("Altitude Nodes Parent Left Right: \n")
                for node in block_1.tree.nodes:
                    self.f.write("{0}\n".format(node))

        self.f.close()

    def merging(self, block_1, block_2, edges, altitudes):
        # edges belonging to block 1
        nodes_1 = [edge[0] for edge in edges]
        nodes_2 = [edge[1] for edge in edges]
        subtree_1 = block_1.get_border_tree(nodes_1)
        # edges belonging to block 2
        subtree_2 = block_2.get_border_tree(nodes_2)

        for i, edge in enumerate(edges):

            self.current_merge_name_1 = str(edge[0])
            self.current_merge_name_2 = str(edge[1])
            selector_1_down = subtree_1.find_leaf(edge[0])
            selector_2_down = subtree_2.find_leaf(edge[1])

            selector_1_up = selector_1_down.parent
            selector_2_up = selector_2_down.parent

            new_tree_nodes = self.compute(altitudes[i], selector_1_down, selector_2_down, selector_1_up, selector_2_up)

            new_tree = Tree(new_tree_nodes)

            update_block_1 = new_tree.leaves_subtree(nodes_1)
            block_1.update_tree(update_block_1, nodes_1)

            update_block_2 = new_tree.leaves_subtree(nodes_2)
            block_2.update_tree(update_block_2, nodes_2)

    def compute(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        new_tree_nodes = []
        node_created = False
        current_node = None
        # do the old merging
        while selector_1_up is not selector_2_up:
            #  If the node is not created
            if node_created is False:
                new_tree_nodes.append(selector_1_down)
                new_tree_nodes.append(selector_2_down)
                #  If both selectors are roots of they respective trees, we create the node
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

                #  If the altitude of both selector_up are higher than the altitude of the edge to merge
                elif selector_1_up.altitude > altitude and selector_2_up.altitude > altitude:
                    [current_node, selector_1_down, selector_2_down, selector_1_up, selector_2_up] = self.create_node(
                                                                                        altitude, selector_1_down,
                                                                                        selector_2_down, selector_1_up,
                                                                                        selector_2_up)
                    new_tree_nodes.append(current_node)
                    current_node = current_node.parent
                    node_created = True
                    # STEP 3) Update the good selector
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

            #  When the node was created
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
        return new_tree_nodes

    def create_node(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):

        parent = self.min_selectors_up(False, selector_1_up, selector_2_up, selector_1_down, selector_2_down, None)

        if parent.altitude < altitude:
            parent = None
            selector_1_down = selector_1_up
            selector_2_down = selector_2_up

        # STEP 1) Create the node and link the node to his parent and to his childs
        if not selector_1_down.is_root():
            selector_1_down.unbind_parent()
        if not selector_2_down.is_root():
            selector_2_down.unbind_parent()

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


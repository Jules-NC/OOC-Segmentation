from Code.Node import *
from Code.Tree import *
from Code.Block import *

# It probqbly zorks
class Server2:
    # New definition for the server
    # +image
    def __init__(self, x_blocks, y_blocks):
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        self.n_blocs = x_blocks * y_blocks

    # TO-DO
    def define_block(self, index):
        # define the edges of each block depending on its index
        graph = None
        border = None
        return Block(graph, border)

    def merging(self, block_1, block_2, edges, altitudes):
        # edges belonging to block 1
        nodes_1 = [edge[0] for edge in edges]
        nodes_2 = [edge[1] for edge in edges]
        subtree_1 = block_1.get_border_tree(nodes_1)
        # edges belonging to block 2
        subtree_2 = block_2.get_border_tree(nodes_2)

        for i, edge in enumerate(edges):

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
                    [current_node, selector_1_down, selector_2_down] = self.create_node(altitude, selector_1_down,
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
                        [selector_1_down, selector_1_up] = self.update_selector(node_created,
                                                                                selector_1_down, selector_1_up,
                                                                                altitude)

                #  If the altitude of both selector_up are higher than the altitude of the edge to merge
                elif selector_1_up.altitude > altitude and selector_2_up.altitude > altitude:
                    [current_node, selector_1_down, selector_2_down] = self.create_node(altitude, selector_1_down,
                                                                                        selector_2_down, selector_1_up,
                                                                                        selector_2_up)
                    new_tree_nodes.append(current_node)
                    current_node = current_node.parent
                    node_created = True
                    # STEP 3) Update the good selector
                    if selector_1_up is current_node:
                        [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down, selector_1_up,
                                                                                altitude)
                    elif selector_2_up is current_node:
                        [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down,
                                                                                selector_1_up,
                                                                                altitude)
                else:
                    [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down, selector_1_up, altitude)
                    [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down, selector_2_up, altitude)

            #  When the node was created
            if node_created is True:
                current_node.unbind_parent()
                current_node.bind_parent(self.min_selectors_up(node_created, selector_1_up, selector_2_up, current_node))

                new_tree_nodes.append(current_node)

                [selector_1_down, selector_1_up] = self.update_selector(node_created, selector_1_down, selector_1_up, altitude)
                [selector_2_down, selector_2_up] = self.update_selector(node_created, selector_2_down, selector_2_up, altitude)

                if current_node.is_root() is False:
                    current_node = current_node.parent
        return new_tree_nodes

    def create_node(self, altitude, selector_1_down, selector_2_down, selector_1_up, selector_2_up):
        # STEP 1) Create the node and link the node to his parent and to his childs
        selector_1_down.unbind_parent()
        selector_2_down.unbind_parent()
        current_node = Node(name="NewNode",
                                 altitude=altitude,
                                 parent=self.min_selectors_up(False, selector_1_up, selector_2_up, None),
                                 left=selector_1_down,
                                 right=selector_2_down)
        return list((current_node, selector_1_down, selector_2_down))

    def min_selectors_up(self, node_created, selector_1_up, selector_2_up, current_node):
        if node_created is False:
            #  If both are root => root is the next selector
            if selector_1_up.altitude > selector_2_up.altitude:
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


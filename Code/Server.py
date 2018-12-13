from Code.Node import *
from Code.Tree import *
from Code.Block import *

class Server:

    def __init__(self, bloc_1, bloc_2, edge, edge_altitude):

        self.edge = edge
        self.edge_altitude = edge_altitude

        self.bloc_1 = bloc_1
        self.bloc_2 = bloc_2

        self.subtree_1 = bloc_1.get_subtree(edge[0])
        self.subtree_2 = bloc_2.get_subtree(edge[1])

        self.selector_1_down = self.subtree_1.nodes[0]
        self.selector_2_down = self.subtree_2.nodes[0]

        self.selector_1_up = self.selector_1_down.parent
        self.selector_2_up = self.selector_2_down.parent

        self.current_node = None
        self.node_created = False
        self.new_tree = None
        self.new_tree_nodes = []

    def merging(self):
        self.compute()
        self.new_tree = Tree(self.new_tree_nodes)

        update_bloc1 = self.new_tree.leaf_subtree(self.edge[0])
        self.bloc_1.update_tree(update_bloc1, [self.edge[0]])

        update_bloc2 = self.new_tree.leaf_subtree(self.edge[1])
        self.bloc_2.update_tree(update_bloc2, [self.edge[1]])

    def compute(self):
        while self.selector_1_up is not self.selector_2_up:
            #  If the node is not created
            if self.node_created is False:
                self.new_tree_nodes.append(self.selector_1_down)
                self.new_tree_nodes.append(self.selector_2_down)

                #  If both selectors are roots of they respective trees, we create the node
                if self.selector_1_up.is_root() and self.selector_2_up.is_root():
                    self.create_node()
                #  If the altitude of both selectorcurrent_nodes up are higher than the altitude of the edge to merge
                if self.selector_1_up.altitude > self.edge_altitude and self.selector_2_up.altitude > self.edge_altitude:
                    self.create_node()
                self.update_selector_1()
                self.update_selector_2()

            #  When the node was created
            if self.node_created is True:
                self.current_node.unbind_parent()
                self.current_node.bind_parent(self.second_min_selectors_up())

                self.new_tree_nodes.append(self.current_node)
                self.second_update_selector_1()
                self.second_update_selector_2()

                if self.current_node.is_root() is False:
                    self.current_node = self.current_node.parent
        print(self.current_node)

    def update_selector_1(self):
        # If the altitude of the selector up is lower than the altitude of the edge, we increment the selector
        if self.selector_1_up.altitude < self.edge_altitude:
            self.selector_1_down = self.selector_1_up
            if self.selector_1_up.parent is not None:
                self.selector_1_up = self.selector_1_up.parent

    def second_update_selector_1(self):
        self.selector_1_down = self.selector_1_up
        if self.selector_1_up.parent is not None:
            self.selector_1_up = self.selector_1_up.parent

    def update_selector_2(self):
        if self.selector_2_up.altitude < self.edge_altitude:
            self.selector_2_down = self.selector_2_up
            if self.selector_2_up.parent is not None:
                self.selector_2_up = self.selector_2_up.parent

    def second_update_selector_2(self):
        self.selector_2_down = self.selector_2_up
        if self.selector_2_up.parent is not None:
            self.selector_2_up = self.selector_2_up.parent

    def create_node(self):
        # STEP 1) Create the node and link the node to his parent and to his childs
        self.selector_1_down.unbind_parent()
        self.selector_2_down.unbind_parent()
        self.current_node = Node(name="NewNode",
                                 altitude=self.edge_altitude,
                                 parent=self.min_selectors_up(),
                                 left=self.selector_1_down,
                                 right=self.selector_2_down)

        self.node_created = True
        self.new_tree_nodes.append(self.current_node)
        self.current_node = self.current_node.parent

        # STEP 3) Update the good selector
        if self.selector_1_up is self.current_node:
            self.second_update_selector_1()
        elif self.selector_2_up is self.current_node:
            self.second_update_selector_2()

    def update_machins(self):
        # STEP 2) Delete the remainings links from the selectors
        self.selector_1_down.parent = self.current_node
        self.selector_2_down.parent = self.current_node

        self.selector_1_up.delete_child(self.selector_1_down)
        self.selector_2_up.delete_child(self.selector_2_down)

        self.current_node = self.current_node.parent

        if self.selector_1_up is self.current_node:
            self.second_update_selector_1()
        elif self.selector_2_up is self.current_node:
            self.second_update_selector_2()

    def min_selectors_up(self):
        #  If both are root => root is the next selector
        if self.selector_1_up.altitude > self.selector_2_up.altitude:
            return self.selector_2_up
        else:
            return self.selector_1_up

    def second_min_selectors_up(self):
        if self.current_node.is_root() and self.current_node is self.selector_1_up:
            return self.selector_2_up

        if self.current_node.is_root() and self.current_node is self.selector_2_up:
            return self.selector_1_up

        if self.selector_1_up.altitude > self.selector_2_up.altitude:
            return self.selector_2_up
        else:
            return self.selector_1_up

    def max_selectors_up(self):
        #  If both are root => root is the next selector
        if self.selector_1_up.altitude > self.selector_2_up.altitude:
            return self.selector_1_up
        else:
            return self.selector_2_up

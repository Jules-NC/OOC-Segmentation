from Code.Tree import *


class Server:
    def __init__(self, bloc_1, bloc_2, edge, edge_altitude):

        self.edge = edge
        self.edge_altitude = edge_altitude

        self.subtree_1 = bloc_1.get_subtree(edge[0])
        self.subtree_2 = bloc_2.get_subtree(edge[1])

        self.selector_1_down = self.subtree_1.nodes[0]
        self.selector_2_down = self.subtree_2.nodes[0]

        self.selector_1_up = self.selector_1_down.parent
        self.selector_2_up = self.selector_2_down.parent

        self.current_node = None
        self.node_created = False

    def compute(self):
        while self.selector_1_up is not self.selector_2_up:
            #  If the node is not created
            if self.node_created is False:
                self.update_selector_1()
                self.update_selector_2()
                #  If both selectors are roots of they respective trees, we create the node
                if self.selector_1_up.parent is None and self.selector_2_up is None:
                    self.create_node()
                #  If the altitude of both selectors up are higher than the altitude of the edge to merge
                if self.selector_1_up.altitude > self.edge_altitude and self.selector_2_up.altitude > self.edge_altitude:
                    self.create_node()

            #  When the node was created
            if self.node_created is True:
                self.current_node.parent = self.second_min_selectors_up()
                self.second_min_selectors_up().add_child(self.current_node)
                self.max_selectors_up().delete_child(self.current_node)

                self.second_update_selector_1()
                self.second_update_selector_2()

                if not self.current_node.is_root():
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
        self.current_node = Node(name="NewNode",
                                 altitude=self.edge_altitude,
                                 parent=self.min_selectors_up(),
                                 childs=(self.selector_1_down, self.selector_2_down))
        # STEPS 1) Change the links on the NewNode
        self.current_node.parent.delete_child(self.current_node.parent.childs[1])
        self.current_node.parent.add_child(self.current_node)

        # STEP 2) Delete the remainings links from the selectors
        self.selector_1_down.parent = self.current_node
        self.selector_2_down.parent = self.current_node

        self.selector_1_up.delete_child(self.selector_1_down)
        self.selector_2_up.delete_child(self.selector_2_down)

        self.node_created = True
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

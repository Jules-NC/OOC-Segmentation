from Tree import *


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
            # If the node is not created
            if self.node_created is False:
                self.update_selector_1()
                self.update_selector_2()
                # If both selectors are roots of they respective trees, we create the node
                if self.selector_1_up.parent is None and self.selector_2_up is None:
                    self.create_node()
                # If the altitude of both selectors up are higher than the altitude of the edge to merge
                if self.selector_1_up.altitude > self.edge_altitude and self.selector_2_up > self.edge_altitude:
                    self.create_node()

            # When the node was created
            if self.node_created is True:
                self.current_node.parent = self.max_selectors_up()
                self.current_node = self.max_selectors_up()
                self.update_selector_1()
                self.update_selector_2()
                self.update_machins()

    def update_selector_1(self):
        # If the altitude of the selector up is higher than the altitude of the edge, we increment the selector
        if self.selector_1_up.altitude > self.edge_altitude:
            self.selector_1_down = self.selector_1_up
            if self.selector_1_up.parent is not None:
                self.selector_1_up = self.selector_1_up.parent

    def update_selector_2(self):
        if self.selector_2_up.altitude > self.edge_altitude:
            self.selector_2_down = self.selector_2_up
            if self.selector_2_up.parent is not None:
                self.selector_2_up = self.selector_2_up.parent

    def create_node(self):
        # STEP 1) Create the node and link the node to his parent and to his childs
        self.current_node = Node(name="LOLOLOLOL",
                                 altitude=self.edge_altitude,
                                 parent=self.max_selectors_up(),
                                 childs=(self.selector_1_down,self.selector_2_down))
        self.update_machins()

    def update_machins(self):
        # STEP 2) Delete the remainings links from the selectors
        self.selector_1_down.parent = self.current_node
        self.selector_2_down.parent = self.current_node

        self.selector_1_up.delete_child(self.selector_1_down)
        self.selector_2_up.delete_child(self.selector_2_down)

        self.node_created = True
        self.current_node = self.current_node.parent

        if self.selector_1_up is self.current_node:
            self.update_selector_1()
        elif self.selector_2_up is self.current_node:
            self.update_selector_2()
        else:
            print("GROSSE ERREUR CA VA PAS IT S DOESN'T GOOD AT ALL")

    def max_selectors_up(self):
        # If both are root => root is the next selector
        if self.selector_1_up.is_root() and self.selector_2_up.is_root():
            return None

        if self.selector_1_up.altitude > self.selector_2_up.altitude:
            return self.selector_2_up
        else:
            return self.selector_1_up


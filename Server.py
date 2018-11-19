from Tree import *

class Server:
    def __init__(self, bloc_1, bloc_2, edge, edge_altitude):
        self.bloc_1 = bloc_1
        self.bloc_2 = bloc_2

        self.edge = edge
        self.edge_altitude = edge_altitude

        self.subtree_1 = self.bloc_1.get_subtree(edge[0])
        self.subtree_2 = self.bloc_2.get_subtree(edge[1])
        
        self.tree = self.subtree_1.nodes.append(self.subtree_2.nodes)

        self.selector_node_b1 = self.subtree_1.nodes[0].parent
        self.selector_node_b2 = self.subtree_2.nodes[0].parent

        self.selector_name_b1 = self.selector_node_b1.name
        self.selector_name_b2 = self.selector_node_b2.name

        self.selector_alt_b1 = self.selector_node_b1.altitude
        self.selector_alt_b2 = self.selector_node_b2.altitude

        self.current_node = None
        self.can_continue = True
        

    def compute(self):
        print("Selectors :", self.selector_name_b1, self.selector_name_b2)
        print("Alts sels :", self.selector_alt_b1, self.selector_alt_b2)

        while self.can_continue:
            if self.current_node is not None:
                if self.current_node.parent is None:
                    self.can_continue = False
                    print("COND1")
                    continue

            if self.can_create_new_node():
                print("CREATION D'UNE NODE")
                self.current_node = self.new_node()
                print("ST-1")
                print(self.subtree_1)
                print("ST-2")
                print(self.subtree_2)

            if self.current_node is None:
                print("PAS DE NODE CREE, ON ITERE")
                print("ST-1")
                print(self.subtree_1)
                print("ST-2")
                print(self.subtree_2)
                pass

            if self.current_node is not None:
                print("ON LINK LA NODE")
                self.relink()
                print("ST-1")
                print(self.subtree_1)
                print("ST-2")
                print(self.subtree_2)
            print("========================")
            self.increase_selectors()

    def can_create_new_node(self):
        return self.selector_alt_b1 == self.edge_altitude or self.selector_alt_b2 == self.edge_altitude and self.current_node is None

    def new_node(self):
        new_node = Node(name=(self.selector_name_b1, self.selector_name_b2),
                        altitude=self.edge_altitude,
                        childs=(self.selector_node_b1, self.selector_node_b2))
        if self.selector_node_b1 is not None:
            self.selector_node_b1.parent = new_node
        if self.selector_node_b2 is not None:
            self.selector_node_b2.parent = new_node
        self.node_not_created = False
        return new_node

    def relink(self):
        self.current_node.father = self.max_fathers()
        self.current_node = self.max_fathers()

    def increase_selectors(self):
        if self.selector_node_b1.parent is not None:
            self.selector_node_b1 = self.selector_node_b1.parent
            self.selector_name_b1 = self.selector_node_b1.name
            self.selector_alt_b1 = self.selector_node_b1.altitude
        else:
            self.selector_node_b1 = None
            self.selector_name_b1 = None
            self.selector_alt_b1 = None


        if self.selector_node_b2.parent is not None:
            self.selector_node_b2 = self.selector_node_b2.parent
            self.selector_name_b2 = self.selector_node_b2.name
            self.selector_alt_b2 = self.selector_node_b2.altitude
        else:
            self.selector_node_b2 = None
            self.selector_name_b2 = None
            self.selector_alt_b2 = None

    def max_fathers(self):
        if self.selector_node_b1 is None and self.selector_node_b2 is not None:
            return self.selector_node_b2
        elif self.selector_node_b1 is not None and self.selector_node_b2 is None:
            return self.selector_node_b1
        elif self.selector_node_b2 is None and self.selector_node_b1 is None:
            return None
        elif self.selector_alt_b1 > self.selector_alt_b2:
            return self.selector_node_b1
        return self.selector_node_b2
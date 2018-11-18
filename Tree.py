class Tree:
    def __init__(self, list_of_nodes):
        self.nodes = list_of_nodes
        self.root = self.nodes[-1]

    def height(self):
        return self.root.rec_height(0)


class Node:
    def __init__(self, name="!", altitude=-1, parent=None, childs=(None, None)):
        self.parent = parent
        self.childs = childs
        self.name = name
        self.altitude = altitude

    def left(self):
        return self.childs[0]

    def right(self):
        return self.childs[1]

    def leaf(self):
        return self.childs[0] is None and self.childs[1] is None

    def rec_height(self, i):
        if self.leaf():
            return i
        ch1 = None
        ch2 = None
        if self.left() is not None:
            ch1 = self.left().rec_height(i)
        if self.right() is not None:
            ch2 = self.right().rec_height(i)

        return max(ch1, ch2) + 1

    def set_childs(self, child1=None, child2=None):
        self.childs = list(self.childs)
        self.childs[0] = child1
        self.childs[1] = child2
        self.childs = tuple(self.childs)

    def add_child(self, node):
        self.childs = list(self.childs)
        if self.childs[0] is None:
            self.childs[0] = node
        elif self.childs[1] is None:
            self.childs[1] = node
        self.childs = tuple(self.childs)

    def root(self):
        if self.parent is None:
            return self
        return self.parent.root()

    def __eq__(self, other):
        # return self.name == other.name
        return self == other

    def is_(self, other):
        return self.name == other.name

    def __str__(self):
        res = ""
        if self.parent is not None:
            res += str(self.parent.name) + ", "
        else:
            res += "None, "
        res += '"' + str(self.name) + '"' + ", "
        res += "[" + str(self.altitude) + "], "
        if self.childs[0] is not None: res += "{" + str(self.childs[0].name) + ", "
        if self.childs[1] is not None:
            res += str(self.childs[1].name) + "}"
        elif self.childs[0] is None and self.childs[1] is None:
            res += "{,}"
        return res

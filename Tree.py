class Node:
    def __init__(self, name="!", altitude=-1, parent=None, childs=(None, None)):
        self.parent = parent
        self.childs = childs
        self.name = name
        self.altitude = altitude

    def leaf(self):
        return self.childs[0] is None and self.childs[1] is None

    def height(self):
        return self.root().rec_root(0)

    def rec_root(self, i):
        if self.parent is None:
            return i
        return self.parent.rec_root(i + 1)

    def max_height(self):
        if self.leaf():
            return 1
        return max(self.childs[0].max_height(), self.childs[1].max_height()) + 1

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

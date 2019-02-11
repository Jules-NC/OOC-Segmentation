class Node:
    """
    A Node object represent a QBT node.
    :param name: Name of the node
    :type name: str
    
    :param altitude: Represent the QBT altitude (see QBT)
    :type altitude: int
    
    :param parent: The parent of the current Node
    :type parent: Node

    :param left: The left child of the current Node
    :type left: Node

    :param right: The right child of the current Node
    :type right: Node
    """
    def __init__(self, name=None, altitude=None, parent=None, left=None, right=None):
        """
        During the initialisation of a Node, if parent, left or right is not None, then
        the current node is binded with them. If parent is not none, bind_parent(parent)
        is used. Otherwise, bind_child(child) is used for both of the parents
        """
        self.name = name
        self.altitude = altitude

        self.parent = None
        if parent is not None:
            self.bind_parent(parent)

        self.left = None
        if left is not None:
            self.bind_child(left)

        self.right = None
        if right is not None:
            self.bind_child(right)

    def is_leaf(self):
        """True if the Node is a is_leaf => childs are None"""
        return self.left is None and self.right is None

    def rec_height(self, i):
        assert i >= 0, "Rec_height canno be below zero"
        """Recursively get the height from the node to the childs"""
        if self.is_leaf():
            return i
        #   To avoid None comparisons, -1 better than None
        left = -1
        right = -1
        if self.left is not None:
            left = self.left.rec_height(i)
        if self.right is not None:
            right = self.right.rec_height(i)
        return max(left, right) + 1

    def add_child(self, node):
        """Add the Node node as a child of self if one of the childs of self is
        None. It will assign the left child first, and the right child if the
        left child already exists"""
        assert self.can_add_child() is True, "The parent must have one child 'left'..."

        if self.left is None:
            self.left = node
        elif self.right is None:
            self.right = node

    def child_exist(self, other):
        if self.left == other or self.right == other:
            return True
        else:
            return False

    def delete_child(self, node):
        if self.left == node:
            self.left = None
        elif self.right == node:
            self.right = None

    def can_add_child(self):
        if self.left is None or self.right is None:
            return True
        else:
            return False

    def bind_parent(self, node):
        assert self.parent is None, "The parent must exist"
        assert node != self, "The parent must not be the current node"
        self.parent = node
        self.parent.add_child(self)

    def unbind_parent(self):
        #assert self.parent is not None, "parent must not be None"
        if self.is_root():
            return
        assert self.parent.child_exist(self)
        self.parent.delete_child(self)
        self.parent = None

    def bind_child(self, node):
        assert node != self, "The child must not be the current node"
        node.bind_parent(self)

    def unbind_child(self, child):
        assert child is not None, "Cannot unbind a unbinded link"
        assert self.child_exist(child) is True, "The child to delete must exist"
        assert child.parent is self, "The child must be linked to the parent"

        self.delete_child(child)
        child.parent = None

    def root(self):
        """Recursively return the root of the Node self"""
        if self.is_root():
            return self
        else:
            return self.parent.root()

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def subtree(self, list_):
        """Recursively add the parent of self to a list_ list_ => subtree"""
        if self.parent is None:
            return list_
        list_.append(self)
        return self.parent.subtree(list_)

    def __eq__(self, other):
        if other is None:
            return False
        if self.name == other.name and self.altitude == other.altitude:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.altitude < other.altitude:
            return True
        else:
            return False

    def is_(self, other):
        return self.name == other.name

    def __str__(self):
        """
        Print a Node with the following template:
            parent name, "name", [altitude], {child 1 name, child 2 name}
        """
        res = "["
        res += str(self.altitude) + ", "

        res += "'" + str(self.name) + "'" + ", "
        if self.parent is not None:
            res += "[" + str(self.parent.name) + "], "
        else:
            res += "[None], "

        # A and not B
        if self.left is not None and self.right is None:
            res += "{" + str(self.left.name) + ", None}"
        # A and B
        elif self.left is not None and self.right is not None:
            res += "{" + str(self.left.name) + ", " + str(self.right.name) + "}"
        # not A and B
        elif self.left is None and self.right is not None:
            res += "{None, " + str(self.right.name) + "}"
        # not A and not B
        else:
            res += "{None, None}"
        res += "]"
        return res
        
    def copy(self): 
        return Node(name=self.name, altitude=self.altitude)
    
     def set_Surface(self):
        if self.left != None:
            if self.right != None:
                self.aire = self.left.set_Surface()+self.right.set_Surface()
            else:
                self.aire = self.left.set_Surface()
        else:
            if self.right != None:
                self.aire = self.right.set_Surface()
            else:
                self.aire = 1
        return self.aire

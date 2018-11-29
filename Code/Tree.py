class Tree:
    """
    Tree object. A tree object is composed by a list of nodes and a root node
    :param list_of_nodes: The list of Nodes of the tree
    """
    def __init__(self, list_of_nodes):
        self.nodes = list_of_nodes
        self.root = self.nodes[-1]

    def height(self):
        """
        Return the height of the graph from the root node
        """
        return self.root.rec_height(0)

    def subtree(self, leaf_name):
        """
        If leaf_name is a leaf, then subtree(self, leaf_name) will return a new
        Tree composed by the parents of the leaf only
        
        If the Tree is:
            a
           / \
          b   c
         /
        d
        
        then subtree(d) will return:
            a
           / 
          b
         /
        d
        """
        res = None
        for node in self.nodes:  # TODO: actually O(n). Want O(1) for the search part
            if node.name == leaf_name:
                res = node.subtree([])
        assert res is not None, "leaf not found"
        return Tree(res)

    def __str__(self):
        """
        Print the Tree in the form:
            Leaf 1
            Leaf 2
            ...
            Leaf n-1
            Leaf n
            <BLANKLINE>
        """
        res = ""
        for node in self.nodes:
            res += str(node) + "\n"
        return res


class Node:
    """
    A Node object represent a QBT node.
    :param name: Name of the node. Can be any type
    :param altitude: int wich represent the QBT altitude (see QBT)
    """
    def __init__(self, name=None, altitude=None, parent=None, left=None, right=None):
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

    def leaf(self):
        """True if the Node is a leaf => childs are None"""
        return self.left is None and self.right is None

    def rec_height(self, i):
        """Recursively get the height from the node to the childs"""
        if self.leaf():
            return i
        left = None
        right = None
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
        assert self.parent is None, "The parent must not exist"
        self.parent = node
        self.parent.add_child(self)

    def unbind_parent(self, parent):
        assert parent is not None, "parent must not be None"
        assert self.parent is parent, "The parent of the node must be the good parent"
        assert parent.child_exist(self)
        self.parent = None
        parent.delete_child(self)

    def bind_child(self, node):
        node.bind_parent(self)

    def unbind_child(self, child):
        assert child is not None, "Cannot unbind a unbinded link"
        assert self.child_exist(child) is True, "The child to delete must exist"
        assert child.parent is self, "The child must be linked to the parent"

        self.delete_child(child)
        child.parent = None

    def root(self):
        """Recursively return the root of the Node self"""
        if self.parent is None:
            return self
        return self.parent.root()

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def subtree(self, list):
        """Recursively add the parent of self to a list list_ => subtree"""
        if self.parent is None:
            return list
        list.append(self)
        return self.parent.subtree(list)

    def __eq__(self, other):
        if other is None:
            return False
        if self.name == other.name and self.altitude == other.altitude:
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
        res +="]"
        return res

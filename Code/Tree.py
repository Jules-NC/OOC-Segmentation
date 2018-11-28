class Tree:
    """
    Tree object. A tree object is composed by a list of nodes and a root node
    :param nodes: The list of Nodes of the tree
    :param root: The root Node of the tree, wich is contained in self.nodes
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
        self.parent = parent
        self.left = left
        self.right = right

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
            left = self.left().rec_height(i)
        if self.right is not None:
            right = self.right.rec_height(i)
        return max(left, right) + 1

    def set_childs(self, child1=None, child2=None):
        """...set the childs of the Node..."""
        self.childs = list(self.childs)
        self.childs[0] = child1
        self.childs[1] = child2
        self.childs = tuple(self.childs)

    def add_child(self, node):
        """Add the Node node as a child of self if one of the childs of self is
        None. It will assign the left child first, and the right child if the
        left child already exists"""
        self.childs = list(self.childs)
        if self.childs[0] is None:
            self.childs[0] = node
        elif self.childs[1] is None:
            self.childs[1] = node
        self.childs = tuple(self.childs)

    def delete_child(self, node):
        self.childs = list(self.childs)
        if self.childs[0] is node:
            self.childs[0] = None
        elif self.childs[1] is node:
            self.childs[1] = None
        self.childs = tuple(self.childs)

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
        res = False
        if self.name is other.name and \
        self.altitude is other.altitude and \
        self.parent is other.parent and \
        self.left is other.left and \
        self.right is other.right:
            res = True
        return res

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

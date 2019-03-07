from Code.Tree import *

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

    def find_node(self, leaf_name):
        for node in self.nodes:
            if node.name == leaf_name:
                return node
        return None

    def leaf_subtree(self, leaf_name):
        ref = self.find_node(leaf_name)
        # Create the sublist
        boundary = []
        while ref is not None:
            boundary.append(ref.copy())
            ref = ref.parent
        for i in range(len(boundary)-1):
            boundary[i].bind_parent(boundary[i+1])
        return Tree(boundary)

    def leaves_subtree(self, leaves_name):
        boundary = []
        for l in leaves_name:
            ref = self.find_node(l)
            # Create the sublist
            while ref is not None and ref not in boundary:
                boundary.append(ref.copy())
                ref = ref.parent
            ref = self.find_node(l)
            while ref is not None:
                if not ref.is_root():
                    n = boundary.index(ref.copy())
                    n_parent = boundary.index(ref.parent.copy())
                    if n_parent is not None and boundary[n].parent is None:
                        boundary[n].bind_parent(boundary[n_parent])
                ref = ref.parent
        boundary.sort()
        return Tree(boundary)

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
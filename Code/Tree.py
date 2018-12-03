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
        If leaf_name is a is_leaf, then subtree(self, leaf_name) will return a new
        Tree composed by the parents of the is_leaf only
        
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
        assert res is not None, "is_leaf not found"
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

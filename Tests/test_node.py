from Code.Tree import *


def test_init():
    node_1 = Node()
    assert node_1.name is None
    assert node_1.altitude is None
    assert node_1.parent is None
    assert node_1.left is None
    assert node_1.right is None
    assert str(node_1) == "[None, 'None', [None], {None, None}]"
    
    node_2 = Node(name="NomTest")
    assert node_2.name is "NomTest"
    assert node_2.altitude is None
    assert node_2.parent is None
    assert node_2.left is None
    assert node_2.right is None
    assert str(node_2) == "[None, 'NomTest', [None], {None, None}]"

    node_3 = Node(name="NodeTrois", left=node_2)
    assert node_3.name is "NodeTrois"
    assert node_3.left is node_2
    assert node_3.left == node_2
    assert node_3.left.name is "NomTest"
    assert str(node_3) == "[None, 'NodeTrois', [None], {NomTest, None}]"

    node_4 = Node(name="Node4", altitude=42100, parent=node_1, right=node_2)
    assert node_4.parent is node_1
    assert node_4.parent == node_1
    assert str(node_4) == "[42100, 'Node4', [None], {None, NomTest}]"
    
    node_5 = Node(name="Node5", altitude=300, parent=None, left=None, right=None)
    node_6 = Node(name="NodeSix", altitude=120, parent=None, left=None, right=None)
    node_7 = Node(name="Node7ven", altitude=10, parent=None, left=None, right=None)
    node_8 = Node(name="Node8", altitude=42, parent=node_5, left=node_6, right=node_7)
    assert str(node_8) == "[42, 'Node8', [Node5], {NodeSix, Node7ven}]"


def test_egality():
    a = Node()
    b = Node()
    assert a is not b
    assert a == b
    
    c = Node(name="lol", parent=a)
    d = Node(name="lol", parent=b)
    assert c is not d
    assert c != d


def test_fonctions():
    node_5 = Node(name="Node5", altitude=300, parent=None, left=None, right=None)
    node_6 = Node(name="NodeSix", altitude=120, parent=None, left=None, right=None)
    node_7 = Node(name="Node7ven", altitude=10, parent=None, left=None, right=None)
    node_8 = Node(name="Node8", altitude=42, parent=node_5, left=node_6, right=node_7)
    
    root = node_8.root()
    print(root)
    assert root is node_5
    assert root == node_5
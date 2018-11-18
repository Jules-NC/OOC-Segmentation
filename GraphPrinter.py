import matplotlib.pyplot as plt
import networkx as nx
import math
import csv


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5,
                  pos=None, parent=None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    if parent != None:  # this should be removed for directed graphs.
        neighbors.remove(parent)  # if directed, then parent not in neighbors.
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                parent=root)
    return pos


def write_QBT(node_list, figsize=(10, 5)):
    listofedges = [(node.name, node.parent.name) for node in node_list if node.parent is not None]
    lignes = [[node[0], node[1]] for i, node in enumerate(listofedges)]

    with open('graphe.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Source", "Target"])

        for ligne in lignes:
            writer.writerow(ligne)


def print_QBT(node_list, figsize=(10, 5)):
    G = nx.Graph()
    listofedges = [(node.name, node.parent.name) for node in node_list if node.parent is not None]
    G.add_edges_from(listofedges)
    pos = hierarchy_pos(G, listofedges[-1][1])
    plt.figure(1, figsize=figsize)
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()


def print_QBT2(node_list, figsize=(10, 5)):
    G = nx.Graph()
    listofedges = [(node.name, node.parent.name) for node in node_list if node.parent is not None]
    G.add_edges_from(listofedges)
    pos = hierarchy_pos(G, listofedges[-1][1], width=2 * math.pi, xcenter=0)
    new_pos = {u: (r * math.cos(theta), r * math.sin(theta)) for u, (theta, r) in pos.items()}
    plt.figure(1, figsize=figsize)
    nx.draw(G, pos=new_pos, node_size=50, with_labels=True)
    nx.draw_networkx_nodes(G, pos=new_pos, nodelist=[listofedges[-1][1]], node_color='blue', node_size=200)
    plt.show()


def print_QBTN(node_list, figsize=(10, 5)):
    G = nx.Graph()
    listofedges = [(node.name, node.parent.name) for node in node_list if node.parent is not None]
    G.add_edges_from(listofedges)
    plt.figure(1, figsize=figsize)
    nx.draw(G, with_labels=True)
    plt.show()
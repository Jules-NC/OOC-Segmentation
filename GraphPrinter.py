import networkx as nx
import matplotlib.pyplot as plt

V = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def view(E, F):
    # Traduction des edges pour l'humain
    Etrad = [(V[i], V[j]) for i, j in E]

    # Sample graph
    G = nx.Graph()

    for edge in Etrad:
      G.add_edge(*edge)
    labels = {Etrad[i]:F[i] for i in range(len(Etrad))}
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=30)
    plt.savefig("graph.png")
    plt.show()


def viewP(Parent, lV):
    G = nx.Graph()

    for i in range(len(Parent)):
        if Parent[i] == -1:
            continue
        G.add_edge(*(i, Parent[i]))
    nx.draw(G, with_labels=True)
    plt.savefig("graph.png")
    plt.show()


from Code.Graph import *


def test_init():
    edges = [(0, 1), (1, 2), (2, 3)]
    weights = [1, 6, 12]
    graph_1 = Graph(3, edges, weights)
    
    print(edges)
    print(graph_1.edges)
    #   TODO !: POURQUOI ?????????????????????? 
    #   assert graph_1.edges == edges
    #   assert graph_1.weights is weights
    assert graph_1.it_size is 3
    assert graph_1.n_vertices is 3

import networkx as nx
from itertools import combinations

from helpers import violates_anti_prefs


def find_k_clique(graph, k):
    """
    Algorithm to find cliques of size-k in a graph

    Arguments:
        graph: a networkx Graph object
        k: an integer representing the size of the cliques to find
    
    Return:
        a list of networkx Graph objects representing cliques
    """
    cliques = []
    combos = combinations(graph.nodes, k)

    for combo in combos:
        if not violates_anti_prefs(combo):
            clique = graph.subgraph(combo).copy()
            cliques.append(clique)
    return cliques

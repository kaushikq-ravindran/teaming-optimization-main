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
    # can't have a k-clique in a k-1 graph
    if k > graph.number_of_nodes():
        return []

    # this might technically be correct but is it useful? only for error handling
    if k == 1:
        return list(graph.nodes)

    # if we've gotten to this point we have k >= 2
    two_cliques = [graph.subgraph(edge) for edge in graph.edges]

    if k == 2:
        return two_cliques

    count = 2
    cliques = two_cliques
    next_k_cliques = []
    clique_nodes = set()

    while count < k:
        # enumerate all the possible edge combinations
        for graph1, graph2 in combinations(cliques, 2):

            # find our candidate edge
            candidate_edge = (graph1.nodes | graph2.nodes) - (graph1.nodes & graph2.nodes)

            if len(candidate_edge) == 2 and graph.has_edge(*candidate_edge) and candidate_edge not in next_k_cliques:
                nodes = tuple(graph1.nodes | graph2.nodes)

                if nodes not in clique_nodes:
                    # pull out the subgraph containing all the nodes in this clique and add it to the list of cliques
                    clique = graph.subgraph(nodes).copy()
                    next_k_cliques.append(clique)
                    # add the nodes to the set of clique nodes so we can easily eliminate duplicates
                    clique_nodes.add(nodes)
        count += 1
        cliques = next_k_cliques
        next_k_cliques = []

    return cliques


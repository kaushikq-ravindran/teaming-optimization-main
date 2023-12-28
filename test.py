"""
Code to test helper functions. Currently just tests `overlaps`, but additional
tests should go here.
"""
from helpers import overlaps
import networkx as nx

graph1 = nx.Graph()
graph1.add_node("a")
graph1.add_node("b")
graph1.add_node("c")

graph2 = nx.Graph()
graph2.add_node("e")
graph2.add_node("f")
graph2.add_node("g")

does_overlap = overlaps(graph1.nodes(),graph2.nodes())

print("overlaps:")
print(does_overlap)

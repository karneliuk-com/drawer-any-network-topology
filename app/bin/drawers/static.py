"""
This module creates static pictures using Graphviz/Pygraphviz.
"""
# Modules
import networkx as nx


# Functions
def draw(input_graph, output_path: str) -> None:
    """
    This function creates PNG image from NetworkX graph.
    """
    gv_graph = nx.drawing.nx_agraph.to_agraph(input_graph)
    gv_graph.layout("dot")
    gv_graph.draw(output_path + ".png")

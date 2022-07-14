"""
This module creates dynamic topology using VisJS.
"""
# Modules
from pyvis.network import Network


# Functions
def draw(input_graph, output_path: str) -> None:
    """
    This function creates HTML dynamic page from NetworkX graph.
    """
    pyvis_net = Network(height="600px",
                        width="100%",
                        font_color="#FFFFFF",
                        heading=f"{input_graph.graph['label']}, (c)2022, Karneliuk.com")
    pyvis_net.from_nx(input_graph)
    pyvis_net.toggle_physics(False)
    pyvis_net.set_edge_smooth("starightCross")

    pyvis_net.show(output_path + ".html")

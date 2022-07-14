"""
This module container piece to build network topology
"""
# Modules
import os
from importlib import import_module
import networkx as nx


# Classes
class Topographer:
    """
    This class is used to create objecgt, which visualises network topology
    """
    def __init__(self,
                 data: dict,
                 topology: str,
                 path: str = "./output",
                 output_format: str = "static"):
        self.__data = data
        self.__topology = topology
        self.__graph = None
        self.__path = path
        self.__output_format = output_format

    def build_graph(self):
        """
        This method creates a graph (networkx object) relying the provided data and topoligy type
        """
        subgraphs = list(map(self.__node_subgraph, self.__data.items()))
        self.__graph = nx.compose_all(subgraphs)
        self.__graph.graph["label"] = f"{self.__topology.upper()} Network Topology"

        self.__interconnect_subgraphs()

    def save(self):
        """
        This method saves to a disk the created graph in a DOT language as text file
        """
        if not os.path.exists(path=self.__path):
            os.mkdir(self.__path)

        nx.drawing.nx_agraph.write_dot(self.__graph, f"{self.__path}/{self.__topology}.dot")

    def draw(self):
        """
        This method saves to a disk the created graph as a PNG drawing
        """
        package_name = "bin.drawers"
        module_name = f".{self.__output_format}"

        drawer = import_module(name=module_name, package=package_name)
        drawer.draw(input_graph=self.__graph,
                    output_path=f"{self.__path}/{self.__topology}")

    def __node_subgraph(self, node_detail):
        """
        This is helper method which dynamically import graph based on topology and vendor name.
        """
        vendor = node_detail[1]["platform"]
        package_name = f"bin.{vendor}"
        module_name = f".graph_{self.__topology}"

        subgraph_module = import_module(name=module_name, package=package_name)
        subgraph = subgraph_module.build_one_node(node_detail, extra_data=self.__data)

        return subgraph

    def __interconnect_subgraphs(self):
        """
        This helper method is used to interconnect disjoint nodes, where applicable
        """
        for node in self.__graph.nodes.data():
            if "connect_to" in node[1]:
                if isinstance(node[1]["connect_to"], dict):
                    if node[1]["connect_to"]["type"] == "node":
                        # Add edge
                        self.__graph.add_edge(node[0], node[1]["connect_to"]["value"])

                        # Remove connector metadata
                        if "connect_to" in self.__graph.nodes[node[1]["connect_to"]]:
                            del self.__graph.nodes[node[1]["connect_to"]["value"]]["connect_to"]

                        del self.__graph.nodes[node[0]]["connect_to"]

                    else:
                        for node2 in self.__graph.nodes.data():
                            print("--------------")
                            print(node)
                            print(node2)
                            print("--------------")
                            if node[1]["connect_to"]["type"] in node2[1] and\
                                    node2[1][node[1]["connect_to"]["type"]] == node[1]["connect_to"]["value"]:
                                # Add edge
                                self.__graph.add_edge(node[0], node2[0])

                                # Remove connector metadata
                                del self.__graph.nodes[node[0]]["connect_to"]
                                del self.__graph.nodes[node2[0]]["connect_to"]

                                # Terminate iteration
                                break

                else:
                    raise Exception("The key node['connect_to'] shall be a dictionary.",
                                    f"Obtained: {type(node[1]['connect_to'])}")

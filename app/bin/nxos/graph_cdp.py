"""
This module contains function, which builds CDP subgraphs for Cisco NX-OS based network devices.
"""
# Modules
from typing import Any
import networkx as nx


# Functions
def build_one_node(node_data: tuple, **kwargs) -> Any:
    """
    This method constructs subgraph representing network device and its interfaces
    as well as metadata for interconnection with othet sugraphs.
    """
    graph = nx.Graph()

    graph.add_node(node_data[0],
                   label=node_data[0],
                   color="#104E8B",
                   fontcolor="#FFFFFF",
                   shape="oval",
                   style="filled",
                   node_type="device")

    try:
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["System"]["cdp-items"]\
            ["inst-items"]["if-items"]["If-list"]
        for interface in iter_data:
            if "adj-items" in interface and not interface["id"].startswith("mgmt"):
                if_normalized = interface["id"].replace("eth", "Ethernet")
                if_id = node_data[0] + "_" + if_normalized
                graph.add_node(if_id,
                               label=if_normalized,
                               color="#009ACD",
                               fontcolor="#000000",
                               shape="box",
                               style="filled",
                               node_type="interface")
                graph.add_edge(node_data[0], if_id,
                               penwidth=3.0)

                adj_host = interface["adj-items"]["AdjEp-list"]["devId"].split(".")[0]
                adj_if_name = interface["adj-items"]["AdjEp-list"]["portId"]
                adj_if = adj_host + "_" + adj_if_name
                graph.nodes[if_id]["connect_to"] = adj_if

    except KeyError as err:
        print(f"Skipping node {node_data[0]} as it doesn't have CDP inforamtion: {err}.")

    return graph

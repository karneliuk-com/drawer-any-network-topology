"""
This module contains function, which builds LLDP subgraphs for Cisco IOS XR based network devices.
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

    # Add ISIS meta data
    try:
        general_info = node_data[1]["collected"]["rpc-reply"]["data"]["lldp"]["global-lldp"]

        title = ""
        if "system-name" in general_info["lldp-info"]:
            title += f"system-name: {general_info['lldp-info']['system-name']}\n"

        if "chassis-id" in general_info["lldp-info"]:
            title += f"chassis-id: {general_info['lldp-info']['chassis-id']}\n"

        graph.nodes[node_data[0]]["title"] = title

    except KeyError as err:
        print(f"There is no host-data for LLDP: {node_data[0]}, {err}")

    # Add Interfaces
    try:
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["lldp"]["nodes"]["node"]\
            ["interfaces"]["interface"]
        for interface in iter_data:
            if_id = node_data[0] + "_" + interface["interface-name"]
            if_label = f"{interface['interface-name']}"

            graph.add_node(if_id,
                           label=if_label,
                           color="#000000",
                           fontcolor="#FFFFFF",
                           title=if_label,
                           shape="box",
                           style="filled",
                           node_type="interface")
            graph.add_edge(node_data[0], if_id,
                           penwidth=3.0)

    except KeyError as err:
        print(f"Skipping node {node_data[0]} as it doesn't have LLDP inforamtion: {err}.")

    # Find neighbors
    iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["lldp"]["nodes"]["node"]\
        ["neighbors"]["details"]["detail"]

    for adjacency in iter_data:
        node_a_id = node_data[0] + "_" + adjacency["interface-name"]

        if "lldp-neighbor" in adjacency and adjacency["lldp-neighbor"] and\
                isinstance(adjacency["lldp-neighbor"], dict):
            neighbor = adjacency["lldp-neighbor"]["device-id"] + "_" +\
                adjacency["lldp-neighbor"]["port-id-detail"]
            graph.nodes[node_a_id]["connect_to"] = {
                                                        "type": "node",
                                                        "value": neighbor
                                                    }
            graph.nodes[node_a_id]["color"] = "#009ACD"

    return graph

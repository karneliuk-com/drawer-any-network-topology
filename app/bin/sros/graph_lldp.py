"""
This module contains function, which builds LLDP subgraphs for Nokia SR OS based network devices.
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
    title = f"system-name: {node_data[0]}"
    graph.nodes[node_data[0]]["title"] = title

    # Add Interfaces
    try:
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["state"]["port"]
        for interface in iter_data:
            if interface["oper-state"] != "down":
                if_id = node_data[0] + "_" + interface["port-id"]
                if_label = f"{interface['port-id']}"

                if "ethernet" in interface and "lldp" in interface["ethernet"]:
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
        print(f"Skipping node {node_data[0]} as it doesn't have ISIS inforamtion: {err}.")

    # Find neighbors
    iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["state"]["port"]
    for interface in iter_data:
        if_id = node_data[0] + "_" + interface["port-id"]

        if "ethernet" in interface and "lldp" in interface["ethernet"] and\
                "dest-mac" in interface["ethernet"]["lldp"]:
            for entry in interface["ethernet"]["lldp"]["dest-mac"]:
                if "remote-system" in entry and isinstance(entry["remote-system"], dict):
                    peer = entry["remote-system"]["system-name"] + "_" + entry["remote-system"]["remote-port-id"]
                    graph.nodes[if_id]["connect_to"] = {
                                                            "type": "node",
                                                            "value": peer
                                                        }
                    graph.nodes[if_id]["color"] = "#009ACD"

    return graph

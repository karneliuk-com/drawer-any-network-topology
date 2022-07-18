"""
This module contains function, which builds ISIS subgraphs for Cisco IOS XR based network devices.
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
        nodes = node_data[1]["collected"]["rpc-reply"]["data"]["isis"]["instances"]\
            ["instance"]["host-names"]["host-name"]

        for isis_node in nodes:
            title = ""
            if "system-id" in isis_node:
                title += f"system-id: {isis_node['system-id']}\n"

            if "host-levels" in isis_node:
                title += f"host-levels: {isis_node['host-levels']}\n"

        graph.nodes[node_data[0]]["title"] = title

    except KeyError as err:
        print(f"There is no host-data for ISIS: {err}")

    # Add Interfaces
    try:
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["isis"]["instances"]\
            ["instance"]["interfaces"]["interface"]
        for interface in iter_data:
            # Find connectivity data
            snpa = None
            if "clns-data" in interface["interface-status-and-data"]["enabled"]:
                if "snpa-state" in interface["interface-status-and-data"]["enabled"]["clns-data"]:
                    snpa = interface["interface-status-and-data"]["enabled"]["clns-data"]\
                        ["snpa-state"]["known"]["snpa"]

            # Find ISIS information
            det_info = interface["interface-status-and-data"]["enabled"]["per-topology-data"][0]["status"]

            if_id = node_data[0] + "_" + interface["interface-name"]
            if_label = f"{interface['interface-name']}\ntype: {interface['is-type']}"

            if 'level1-metric' in det_info['enabled']:
                if_label += f"\nL1 cost: {det_info['enabled']['level1-metric']}"

            if 'level2-metric' in det_info['enabled']:
                if_label += f"\nL2 cost: {det_info['enabled']['level2-metric']}"

            if snpa:
                if_label += f"\nSNPA: {snpa}"

            graph.add_node(if_id,
                           label=if_label,
                           color="#000000",
                           fontcolor="#FFFFFF",
                           title=if_label,
                           shape="box",
                           style="filled",
                           node_type="interface",
                           snpa=snpa)
            graph.add_edge(node_data[0], if_id,
                           penwidth=3.0)

    except KeyError as err:
        print(f"Skipping node {node_data[0]} as it doesn't have ISIS inforamtion: {err}.")

    # Find neighbors
    iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["isis"]["instances"]\
        ["instance"]["levels"]["level"]["adjacencies"]["adjacency"]

    for adjacency in iter_data:
        node_a_id = node_data[0] + "_" + adjacency["interface-name"]

        if "adjacency-snpa" in adjacency and adjacency["adjacency-snpa"]:
            graph.nodes[node_a_id]["connect_to"] = {
                                                        "type": "snpa",
                                                        "value": adjacency["adjacency-snpa"]
                                                    }
            graph.nodes[node_a_id]["color"] = "#009ACD"

    return graph

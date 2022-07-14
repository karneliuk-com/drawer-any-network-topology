"""
This module contains function, which builds ISIS subgraphs for Nokia SR OS based network devices.
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
        nodes = node_data[1]["collected"]["rpc-reply"]["data"]["state"]["router"]["isis"]

        title = ""
        if "isis-instance" in nodes:
            title += f"isis-instance: {nodes['isis-instance']}\n"

        if "oper-system-id" in nodes:
            title += f"system-id: {nodes['oper-system-id']}\n"

        if "l1-state" in nodes:
            title += f"l1-state: {nodes['l1-state']}\n"

        if "l2-state" in nodes:
            title += f"l2-state: {nodes['l2-state']}\n"

        graph.nodes[node_data[0]]["title"] = title

    except KeyError as err:
        print(f"There is no host-data for ISIS: {err}")

    # Add Interfaces
    try:
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["state"]["router"]["isis"]\
            ["interface"]
        for interface in iter_data:
            if_id = node_data[0] + "_" + interface["interface-name"]
            if_label = f"{interface['interface-name']}"

            if "level" in interface:
                for level in interface["level"]:
                    if_label += f"\nL{level['level-number']} cost: {level['oper-metric']['ipv4-unicast']}"

            # Find connectivity data
            snpa = None

            if interface['interface-name'].startswith("int"):
                port_id = interface['interface-name'].replace("int", "")

                for port in node_data[1]["collected"]["rpc-reply"]["data"]["state"]["port"]:
                    if port["port-id"] == port_id:
                        snpa = ".".join(["".join(port["hardware-mac-address"].split(":")[:2]),
                                         "".join(port["hardware-mac-address"].split(":")[2:4]),
                                         "".join(port["hardware-mac-address"].split(":")[4:])])

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
    iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["state"]["router"]["isis"]\
            ["interface"]
    for interface in iter_data:
        if_id = node_data[0] + "_" + interface["interface-name"]

        if "adjacency" in interface:
            peer_snpa = interface["adjacency"]["neighbor"]["snpa-address"].replace("0x", "")
            peer_snpa = "0" * (12 - len(peer_snpa)) + peer_snpa
            peer_snpa = peer_snpa[:4] + "." + peer_snpa[4:8] + "." + peer_snpa[8:]

            graph.nodes[if_id]["connect_to"] = {
                                                    "type": "snpa",
                                                    "value": peer_snpa
                                                }
            graph.nodes[if_id]["color"] = "#009ACD"

    return graph

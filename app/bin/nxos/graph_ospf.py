"""
This module contains function, which builds OSPF subgraphs for Cisco NX-OS based network devices.
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
        iter_data = node_data[1]["collected"]["rpc-reply"]["data"]["System"]["ospf-items"]\
            ["inst-items"]["Inst-list"]["dom-items"]["Dom-list"]["if-items"]["If-list"]
        for interface in iter_data:
            if_id = node_data[0] + "_" + interface["id"]
            if_label = f"{interface['id']}\nIP: {interface['addr']}\narea: {interface['area']}"
            graph.add_node(if_id,
                           label=if_label,
                           color="#009ACD",
                           fontcolor="#000000",
                           shape="box",
                           style="filled",
                           node_type="interface")
            graph.add_edge(node_data[0], if_id,
                           penwidth=3.0)

            if "adj-items" in interface:
                peer_ip = interface["adj-items"]["AdjEp-list"]["peerIp"]
                graph.nodes[if_id]["connect_to"] = __get_peer_node(peer_ip=peer_ip,
                                                                   all_data=kwargs["extra_data"])

            if "connect_to" not in graph.nodes[if_id] or not graph.nodes[if_id]["connect_to"]:
                graph.nodes[if_id]["fillcolor"] = "#000000"
                graph.nodes[if_id]["fontcolor"] = "#FFFFFF"

    except KeyError as err:
        print(f"Skipping node {node_data[0]} as it doesn't have OSPF inforamtion: {err}.")

    return graph


def __get_peer_node(peer_ip: str, all_data: dict) -> str:
    """
    This is a helper method to map peerIP of OSPF neighbor to node
    """
    result = None
    for host_name, host_var in all_data.items():
        try:
            iter_data = host_var["collected"]["rpc-reply"]["data"]["System"]["ospf-items"]\
                ["inst-items"]["Inst-list"]["dom-items"]["Dom-list"]["if-items"]["If-list"]
            for interface in iter_data:
                if interface["addr"].startswith(peer_ip):
                    result = host_name + "_" + interface["id"]
                    break

        except KeyError as err:
            print(f"Skipping node {host_name} as it doesn't have OSPF inforamtion: {err}.")

        if result:
            break

    return result

"""
This module builds a rich data structure out of multiple Nornir objects
"""
# Modules
import xmltodict
import xml


# Functions
def prepare_data_for_graph(inventory, results) -> dict:
    """
    This function composes Norninr inventory and Results into a simple dictionary
    """
    result = {}
    inv_dict = inventory.dict()

    for host_name, host_var in inv_dict["hosts"].items():
        result[host_name] = {}

        if host_var["platform"]:
            result[host_name]["platform"] = host_var["platform"]

        else:
            if host_var["groups"]:
                for group_name in host_var["groups"]:
                    if "platform" not in result[host_name] and\
                            inv_dict["groups"][group_name]["platform"]:
                        result[host_name]["platform"] = inv_dict["groups"][group_name]["platform"]

            if "platform" not in result[host_name]:
                result[host_name]["platform"] = inv_dict["defaults"]["platform"]

        try:
            result[host_name]["collected"] = xmltodict.parse(results[host_name][0].result)

        except (ValueError, KeyError, xml.parsers.expat.ExpatError) as err:
            print(f"{host_name}: Error with results: {err}")

    return result

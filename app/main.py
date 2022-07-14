"""
This script contains the tool to interact with Cisco fabric via NAPALM
"""

# Modules
import json
import os
import datetime
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result


# Local modules
import bin.topograph as bt
import bin.structurer as bs
import bin.argparser as ba
import bin.extra_tasks as be


# Statics
CONFIG_FILE = "./config.yaml"
FILTER_FILE = "./bin/filters/netconf_filters.json"


# Body
if __name__ == "__main__":
    time_start = datetime.datetime.now()

    # Get args
    args = ba.get_args()

    # Production mode (work with real data collection)
    if not args.local:
        # Create Nornir object
        nr_obj = InitNornir(config_file=CONFIG_FILE)

        # Set credentials
        nr_obj.inventory.defaults.username = os.getenv("AUTOMATION_USERNMAE")
        nr_obj.inventory.defaults.password = os.getenv("AUTOMATION_PASSWORD")

        # Get NETCONF filter
        with open(file=FILTER_FILE, mode="rt", encoding="utf-8") as filter_file:
            netconf_filters = json.load(filter_file)

        # Select only Nexus from Inventory
        only_nexus = nr_obj.filter(platform="sros")

        # Collect operational information
        task_result = nr_obj.run(task=be.augmented_netconf_get,
                                 netconf_filters=netconf_filters,
                                 topology=args.topology)

        time_finish = datetime.datetime.now()

        # Pring results to STDOUT
        print_result(task_result)
        print(f"Completed in {time_finish - time_start}")

        # Build graph and visualise topology
        augmented = bs.prepare_data_for_graph(inventory=nr_obj.inventory, results=task_result)

        # Store locally NETCONF response
        if args.development:
            open("temp.json", "wt").write(json.dumps(augmented, sort_keys=True, indent=4))

    # Use locally stored NETCONF response
    else:
        augmented = json.loads(open("temp.json", "rt").read())

    # Draw topology
    topo = bt.Topographer(data=augmented, topology=args.topology, output_format=args.format)
    topo.build_graph()
    topo.save()
    topo.draw()

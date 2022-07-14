"""
This module contains extra NORNIR tasks, which perform augmentation of data on per-host basis
"""
# Modules
from nornir.core.task import Task, Result
from nornir_scrapli.tasks import netconf_get


# Tasks
def augmented_netconf_get(task: Task, netconf_filters: dict, topology: str) -> Result:
    """This is a helper tsask to chose proper NETCONF YANG filter based on the NOS"""
    filter_ = netconf_filters[task.host.platform]["state"][topology]

    result = task.run(task=netconf_get, filter_=filter_)

    return Result(host=task.host, result=result[0].result, changed=False)

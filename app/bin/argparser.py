"""
This module contains the det
"""
# Modules
from typing import Any
import argparse


# Functions
def get_args() -> Any:
    """
    The helper function to control which toplogy is to be visualised
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--format",
        type=str,
        required=True,
        choices=[
            "static", "dynamic"
        ],
        default="static",
        help="Select output format",
    )

    parser.add_argument(
        "-l", "--local",
        action="store_true",
        default=False,
        help="Use local copy of NETCONF response",
    )

    parser.add_argument(
        "-t", "--topology",
        type=str,
        required=True,
        choices=[
            "cdp", "ospf", "isis", "lldp", "test"
        ],
        default="cdp",
        help="Select network topology type",
    )

    parser.add_argument(
        "-d", "--development",
        action="store_true",
        default=False,
        help="Save NETCONF response locally",
    )

    result = parser.parse_args()

    return result

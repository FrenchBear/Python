"""
VERY simple port TCP port check
https://docs.python.org/3/library/socket.html
https://www.redhat.com/sysadmin/test-tcp-python-scapy?utm_source=pocket_saves
"""

# 2023-04-20    PV

import socket
from pathlib import Path
from typing import Dict, List
from argparse import ArgumentParser


def load_machines_port(the_data_file: Path) -> Dict[str, List[int]]:
    port_data = {}
    with open(the_data_file, 'r') as d_scan:
        for line in d_scan:
            host, ports = line.split()
            port_data[host] = [int(p) for p in ports.split(',')]
    return port_data


def test_port(address: str, dest_port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((address, dest_port)) == 0:
                return True
        return False
    except (OSError, ValueError):
        return False


if __name__ == "__main__":
    PARSER = ArgumentParser(description=__doc__)
    PARSER.add_argument("scan_file", type=Path, help="Scan file with list of hosts and ports")
    ARGS = PARSER.parse_args()
    data = load_machines_port(ARGS.scan_file)
    for machine in data:
        for port in data[machine]:
            try:
                results = test_port(machine, port)
            except (OSError, ValueError):
                results = False
            if results:
                print(f"{machine}:{port}: OK")
            else:
                print(f"{machine}:{port}: ERROR")
#!/usr/bin/env python3.9

"""
Sever driver, this should be run first
"""

from SockMonkey.Domain.Client.cli import main as cli_main
from SockMonkey.Domain.Server.server import main as server_main


# cli_main()
server_main()

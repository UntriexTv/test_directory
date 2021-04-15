#! /usr/bin/python3
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from main import app

import socket


def get_my_ip_address(remote_server="google.com"):
    """
    Return the/a network-facing IP number for this system.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((remote_server, 80))
        return s.getsockname()[0]


config = Config()
config.bind = [f"""{get_my_ip_address(remote_server="192.168.1.1")}:8000"""]
config.use_reloader = True
asyncio.run(serve(app, config))

#! /usr/bin/python3
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from main import app

config = Config()
config.bind = ["0.0.0.0:8000"]
config.use_reloader = True
asyncio.run(serve(app, config))

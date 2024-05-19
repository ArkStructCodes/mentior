from contextlib import asynccontextmanager
from typing import Optional

import websockets

from .client import UnauthenticatedClient


@asynccontextmanager
async def authenticate(host="127.0.0.1", port="8001", *, token: Optional[str] = None):
    ws = await websockets.connect(f"ws://{host}:{port}")
    try:
        yield await UnauthenticatedClient(ws).authenticate(token)
    finally:
        await ws.close()


@asynccontextmanager
async def connect(host="127.0.0.1", port="8001"):
    ws = await websockets.connect(f"ws://{host}:{port}")
    try:
        yield UnauthenticatedClient(ws)
    finally:
        await ws.close()

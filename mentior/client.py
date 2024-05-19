from typing import Any, Dict, Optional

from websockets import WebSocketClientProtocol

from .errors import AuthenticationError
from .models.base import Request
from .models.data import Status, Statistics
from .types import (
    AuthResponse,
    AuthTokenResponse,
    RequestType,
    StatusResponse,
    StatisticsResponse,
)


class Client:
    """Base class for implementing API endpoints."""

    def __init__(self, ws: WebSocketClientProtocol) -> None:
        self._ws = ws

    async def _request(
        self,
        message_type: RequestType,
        data: Optional[Dict[str, Any]] = None,
    ) -> str | bytes:
        """Send a request to the API. May optionally contain data."""
        req = Request[RequestType](message_type=message_type, data=data)
        # Enabling `exclude_none` omits the `data` field when empty.
        payload = req.model_dump_json(by_alias=True, exclude_none=True)
        await self._ws.send(payload)
        return await self._ws.recv()

    async def status(self) -> Status:
        """Check the API connection status."""
        res = await self._request("APIStateRequest")
        return StatusResponse.parse(res)


class UnauthenticatedClient(Client):
    """Implements API endpoints that can be called without authenticating."""

    async def request_auth_token(self) -> str:
        res = await self._request(
            "AuthenticationTokenRequest",
            {
                "pluginName": "Mentior",
                "pluginDeveloper": "ArkStruct",
                "pluginIcon": None,
            },
        )
        data = AuthTokenResponse.parse(res)
        return data.authentication_token

    async def authenticate(self, token: Optional[str] = None) -> "AuthenticatedClient":
        if token is None:
            token = await self.request_auth_token()
        res = await self._request(
            "AuthenticationRequest",
            {
                "pluginName": "Mentior",
                "pluginDeveloper": "ArkStruct",
                "authenticationToken": token,
            },
        )
        data = AuthResponse.parse(res)
        if not data.authenticated:
            raise AuthenticationError(data.reason)
        return AuthenticatedClient(self._ws)


class AuthenticatedClient(Client):
    """Implements API endpoints that can be called when authenticated."""

    async def statistics(self) -> Statistics:
        res = await self._request("StatisticsRequest")
        return StatisticsResponse.parse(res)

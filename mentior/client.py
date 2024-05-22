from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from websockets import WebSocketClientProtocol

from .errors import AuthenticationError
from .models.base import Request
from .models.data import (
    ArtMeshMatcher,
    ArtMeshes,
    ArtmeshTint,
    AvailableModels,
    ColorTint,
    CurrentModel,
    ExpressionState,
    Hotkeys,
    MoveModel,
    Status,
    Statistics,
    VTSFolderInfo,
)
from .types import (
    ArtMeshListResponse,
    AuthResponse,
    AuthTokenResponse,
    AvailableModelsResponse,
    ColorTintResponse,
    CurrentModelResponse,
    ExpressionActivationResponse,
    ExpressionStateResponse,
    HotkeyTriggerResponse,
    HotkeysInModelResponse,
    ModelLoadResponse,
    MoveModelResponse,
    RequestType,
    StatusResponse,
    StatisticsResponse,
    VTSFolderInfoResponse,
)


class Client:
    """Base class for implementing API endpoints."""

    def __init__(self, ws: WebSocketClientProtocol) -> None:
        self._ws = ws

    async def _request(
        self,
        message_type: RequestType,
        data: Optional[Union[BaseModel, Dict[str, Any]]] = None,
    ) -> str | bytes:
        """Send a request to the API. May optionally contain data."""
        req = Request(message_type=message_type, data=data)
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

    async def vts_folder_info(self) -> VTSFolderInfo:
        res = await self._request("VTSFolderInfoRequest")
        return VTSFolderInfoResponse.parse(res)

    async def current_model(self) -> CurrentModel:
        res = await self._request("CurrentModelRequest")
        return CurrentModelResponse.parse(res)

    async def available_models(self) -> AvailableModels:
        res = await self._request("AvailableModelsRequest")
        return AvailableModelsResponse.parse(res)

    async def load_model(self, model_id: str) -> None:
        res = await self._request("ModelLoadRequest", {"modelID": model_id})
        assert model_id == ModelLoadResponse.parse(res).model_id

    async def move_model(
        self,
        time_in_seconds: float,
        *,
        values_are_relative_to_model: bool = False,
        position_x: Optional[float] = None,
        position_y: Optional[float] = None,
        position_z: Optional[float] = None,
        rotation: Optional[float] = None,
        size: Optional[float] = None,
    ) -> None:
        res = await self._request(
            "MoveModelRequest",
            MoveModel(
                time_in_seconds=time_in_seconds,
                values_are_relative_to_model=values_are_relative_to_model,
                position_x=position_x,
                position_y=position_y,
                position_z=position_z,
                rotation=rotation,
                size=size,
            ),
        )
        MoveModelResponse.parse(res)

    async def model_hotkeys(
        self,
        model_id: Optional[str] = None,
        live2d_item_file_name: Optional[str] = None,
    ) -> Hotkeys:
        res = await self._request(
            "HotkeysInCurrentModelRequest",
            {"modelID": model_id, "live2DItemFileName": live2d_item_file_name},
        )
        return HotkeysInModelResponse.parse(res)

    async def trigger_hotkey(
        self,
        hotkey_id: Optional[str] = None,
        item_instance_id: Optional[str] = None,
    ) -> None:
        res = await self._request(
            "HotkeyTriggerRequest",
            {"hotkeyID": hotkey_id, "itemInstanceID": item_instance_id},
        )
        assert hotkey_id == HotkeyTriggerResponse.parse(res).hotkey_id

    async def expression_state(
        self,
        details: bool = True,
        expression_file: Optional[str] = None,
    ) -> ExpressionState:
        if expression_file is not None:
            if not expression_file.endswith(".exp3.json"):
                raise ValueError("file name must end with .exp3.json")
        res = await self._request(
            "ExpressionStateRequest",
            {"details": details, "expressionFile": expression_file},
        )
        return ExpressionStateResponse.parse(res)

    async def activate_expression(
        self,
        expression_file: Optional[str] = None,
        active: bool = True,
    ) -> None:
        if expression_file is not None:
            if not expression_file.endswith(".exp3.json"):
                raise ValueError("file name must end with .exp3.json")
        res = await self._request(
            "ExpressionActivationRequest",
            {"expressionFile": expression_file, "active": active},
        )
        ExpressionActivationResponse.parse(res)

    async def art_meshes(self) -> ArtMeshes:
        res = await self._request("ArtMeshListRequest")
        return ArtMeshListResponse.parse(res)

    async def tint_art_meshes(
        self,
        color_tint: Optional[ColorTint] = None,
        art_mesh_matcher: Optional[ArtMeshMatcher] = None,
    ) -> int:
        res = await self._request(
            "ColorTintRequest",
            ArtmeshTint(
                color_tint=color_tint or ColorTint(),
                art_mesh_matcher=art_mesh_matcher or ArtMeshMatcher(),
            ),
        )
        return ColorTintResponse.parse(res).matched_art_meshes

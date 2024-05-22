from typing import Literal

from .models.base import Response
from .models.data import (
    AuthStatus,
    AuthToken,
    AvailableModels,
    CurrentModel,
    Empty,
    HotkeyID,
    Hotkeys,
    ModelID,
    Statistics,
    Status,
    VTSFolderInfo,
)

RequestType = Literal[
    "APIStateRequest",
    "AuthenticationRequest",
    "AvailableModelsRequest",
    "AuthenticationTokenRequest",
    "CurrentModelRequest",
    "HotkeysInCurrentModelRequest",
    "HotkeyTriggerRequest",
    "ModelLoadRequest",
    "MoveModelRequest",
    "StatisticsRequest",
    "VTSFolderInfoRequest",
]

AuthResponse = Response[Literal["AuthenticationResponse"], AuthStatus]
AuthTokenResponse = Response[Literal["AuthenticationTokenResponse"], AuthToken]
AvailableModelsResponse = Response[Literal["AvailableModelsResponse"], AvailableModels]
CurrentModelResponse = Response[Literal["CurrentModelResponse"], CurrentModel]
HotkeysInModelResponse = Response[Literal["HotkeysInCurrentModelResponse"], Hotkeys]
HotkeyTriggerResponse = Response[Literal["HotkeyTriggerResponse"], HotkeyID]
ModelLoadResponse = Response[Literal["ModelLoadResponse"], ModelID]
MoveModelResponse = Response[Literal["MoveModelResponse"], Empty]
StatisticsResponse = Response[Literal["StatisticsResponse"], Statistics]
StatusResponse = Response[Literal["APIStateResponse"], Status]
VTSFolderInfoResponse = Response[Literal["VTSFolderInfoResponse"], VTSFolderInfo]

from typing import Literal

from .models.base import Response
from .models.data import (
    ArtMeshes,
    AuthStatus,
    AuthToken,
    AvailableModels,
    CurrentModel,
    Empty,
    ExpressionState,
    HotkeyID,
    Hotkeys,
    ModelID,
    Statistics,
    Status,
    TintedArtMeshes,
    VTSFolderInfo,
)

RequestType = Literal[
    "APIStateRequest",
    "AuthenticationRequest",
    "AuthenticationTokenRequest",
    "StatisticsRequest",
    "VTSFolderInfoRequest",
    "CurrentModelRequest",
    "AvailableModelsRequest",
    "ModelLoadRequest",
    "MoveModelRequest",
    "HotkeysInCurrentModelRequest",
    "HotkeyTriggerRequest",
    "ExpressionStateRequest",
    "ExpressionActivationRequest",
    "ArtMeshListRequest",
    "ColorTintRequest",
]

StatusResponse = Response[Literal["APIStateResponse"], Status]
AuthResponse = Response[Literal["AuthenticationResponse"], AuthStatus]
AuthTokenResponse = Response[Literal["AuthenticationTokenResponse"], AuthToken]
StatisticsResponse = Response[Literal["StatisticsResponse"], Statistics]
VTSFolderInfoResponse = Response[Literal["VTSFolderInfoResponse"], VTSFolderInfo]
CurrentModelResponse = Response[Literal["CurrentModelResponse"], CurrentModel]
ModelLoadResponse = Response[Literal["ModelLoadResponse"], ModelID]
MoveModelResponse = Response[Literal["MoveModelResponse"], Empty]
AvailableModelsResponse = Response[Literal["AvailableModelsResponse"], AvailableModels]
HotkeysInModelResponse = Response[Literal["HotkeysInCurrentModelResponse"], Hotkeys]
HotkeyTriggerResponse = Response[Literal["HotkeyTriggerResponse"], HotkeyID]
ExpressionStateResponse = Response[Literal["ExpressionStateResponse"], ExpressionState]
ExpressionActivationResponse = Response[Literal["ExpressionActivationResponse"], Empty]
ArtMeshListResponse = Response[Literal["ArtMeshListResponse"], ArtMeshes]
ColorTintResponse = Response[Literal["ColorTintResponse"], TintedArtMeshes]

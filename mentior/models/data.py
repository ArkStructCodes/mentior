from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from .base import FromCamel


class Empty(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Status(FromCamel):
    active: bool
    vtube_studio_version: str = Field(validation_alias="vTubeStudioVersion")
    current_session_authenticated: bool


class AuthToken(FromCamel):
    authentication_token: str


class AuthStatus(BaseModel):
    authenticated: bool
    reason: str


class Statistics(FromCamel):
    uptime: int
    framerate: int
    vtube_studio_version: str = Field(validation_alias="vTubeStudioVersion")
    allowed_plugins: int
    connected_plugins: int
    started_with_steam: bool
    window_width: int
    window_height: int
    window_is_fullscreen: bool


class VTSFolderInfo(BaseModel):
    models: str
    backgrounds: str
    items: str
    config: str
    logs: str
    backup: str


class ModelID(FromCamel):
    model_id: str = Field(validation_alias="modelID")


class VTSModel(ModelID):
    model_loaded: bool
    model_name: str
    vts_model_name: str
    vts_model_icon_name: str


class AvailableModels(FromCamel):
    number_of_models: int
    available_models: Optional[List[VTSModel]]


class Position(FromCamel):
    position_x: Optional[float] = Field(default=None, ge=-1, le=1)
    position_y: Optional[float] = Field(default=None, ge=-1, le=1)
    rotation: Optional[float] = Field(default=None, ge=-360, le=360)
    size: Optional[float] = Field(default=-80, ge=-100, le=100)


class CurrentModel(VTSModel):
    live2d_model_name: str = Field(validation_alias="live2DModelName")
    model_load_time: int
    time_since_model_loaded: int
    number_of_live2d_parameters: int = Field(
        validation_alias="numberOfLive2DParameters"
    )
    number_of_live2d_artmeshes: int = Field(validation_alias="numberOfLive2DArtmeshes")
    has_physics_file: bool
    number_of_textures: int
    texture_resolution: int
    model_position: Position


class MoveModel(Position):
    position_z: Optional[float] = Field(default=None, ge=-1, le=1)
    time_in_seconds: float = Field(ge=0, le=2)
    values_are_relative_to_model: bool


class HotkeyID(FromCamel):
    hotkey_id: str = Field(validation_alias="HotkeyID")


class Hotkey(HotkeyID):
    name: str
    type_: str = Field(validation_alias="type")
    description: str
    file: str
    key_combination: List  # empty for the near future, kept for compatibility
    on_screen_button_id: int = Field(validation_alias="onScreenButtonID")


class Hotkeys(ModelID):
    model_loaded: bool
    model_name: str
    available_hotkeys: List[Hotkey]

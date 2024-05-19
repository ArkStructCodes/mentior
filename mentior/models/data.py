from pydantic import BaseModel

from .base import FromCamel


class AuthToken(FromCamel):
    authentication_token: str


class AuthStatus(BaseModel):
    authenticated: bool
    reason: str


class Statistics(FromCamel):
    uptime: int
    framerate: int
    v_tube_studio_version: str
    allowed_plugins: int
    connected_plugins: int
    started_with_steam: bool
    window_width: int
    window_height: int
    window_is_fullscreen: bool


class Status(FromCamel):
    active: bool
    v_tube_studio_version: str
    current_session_authenticated: bool

from typing import Literal

from .models.base import Response
from .models.data import AuthStatus, AuthToken, Statistics, Status

RequestType = Literal[
    "APIStateRequest",
    "AuthenticationRequest",
    "AuthenticationTokenRequest",
    "StatisticsRequest",
]

AuthResponse = Response[Literal["AuthenticationResponse"], AuthStatus]
AuthTokenResponse = Response[Literal["AuthenticationTokenResponse"], AuthToken]
StatisticsResponse = Response[Literal["StatisticsResponse"], Statistics]
StatusResponse = Response[Literal["APIStateResponse"], Status]

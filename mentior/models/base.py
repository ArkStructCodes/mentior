"""Declares the classes necessary for interacting with the API."""

from typing import (
    Any,
    Dict,
    Generic,
    Literal,
    Optional,
    TypeVar,
    Union,
)
from uuid import UUID, uuid4

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .failure import ErrorInfo
from ..errors import APIError


MessageT = TypeVar("MessageT")
DataT = TypeVar("DataT", bound=BaseModel)


class ToCamel(BaseModel):
    """Utility class for serializing field names into camelcase."""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel),
        protected_namespaces=(),
    )


class FromCamel(BaseModel):
    """Utility class for deserializing camelcase field names."""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel),
        protected_namespaces=(),
    )


class Metadata(BaseModel):
    """Metadata included in every message."""

    api_name: str = "VTubeStudioPublicAPI"
    api_version: str = "1.0"
    request_id: UUID = uuid4()

    model_config = ConfigDict(frozen=True)


class Request(Metadata, ToCamel, Generic[MessageT, DataT]):
    """Base class for all request models.

    Generic parameter `MessageT` Must be a supported literal.
    Data validation can be skipped by passing in a dict.
    """

    message_type: MessageT
    data: Optional[Union[Dict[str, Any], DataT]]


class Response(Metadata, FromCamel, Generic[MessageT, DataT]):
    """Base class for all response models.

    Accepts generic parameters `MessageT` and `DataT`.
    The expected `MessageT` Must be a supported literal.
    When `message_type` is `"APIError"`, `data` will contain `ErrorInfo`.
    """

    message_type: Union[MessageT, Literal["APIError"]]
    data: Union[DataT, ErrorInfo]

    def unwrap(self) -> DataT:
        """Returns the response data. Raises `APIError` on failure."""
        if not isinstance(self.data, ErrorInfo):
            return self.data
        else:
            assert self.message_type == "APIError"
            raise APIError(self.data)

    @classmethod
    def parse(cls, src: Union[str, bytes]) -> DataT:
        return cls.model_validate_json(src).unwrap()

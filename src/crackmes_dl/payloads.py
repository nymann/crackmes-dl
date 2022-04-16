from typing import Any, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic import root_validator


class Payload(BaseModel):
    def payload(self, token: str) -> dict[str, Union[str, int]]:
        payload_data = self.dict(by_alias=True, exclude_none=True)
        payload_data.update(token=token)
        return payload_data


class SearchPayload(Payload):
    name: str = ""
    author: str = ""
    difficulty_min: int = Field(default=1, ge=1, le=6, alias="difficulty-min")
    difficulty_max: int = Field(default=6, ge=1, le=6, alias="difficulty-max")
    quality_min: int = Field(default=1, ge=1, le=6, alias="quality-min")
    quality_max: int = Field(default=6, ge=1, le=6, alias="quality-max")
    lang: Optional[str] = None
    arch: Optional[str] = None
    platform: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

    @root_validator
    def min_is_less_than_max(cls, values: dict) -> dict[str, Any]:  # noqa: WPS110
        min_difficulty: int = values["difficulty_min"]
        max_difficulty: int = values["difficulty_max"]
        if min_difficulty >= max_difficulty:
            raise ValueError("difficulty_min should be minimum be 1 less than difficulty_max")
        return values


class AuthPayload(Payload):
    username: str = Field(..., alias="name")
    password: str

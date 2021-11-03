from typing import Optional
from pydantic import BaseModel, HttpUrl, ValidationError, validator


class ShortURLType(BaseModel):
    key: str
    url: HttpUrl
    view_count: int


class ShortenAPIRequest(BaseModel):
    url: HttpUrl
    key: Optional[str] = None

    @validator("key")
    def key_must_use_ascii_alphabet(cls, value):
        if not re.fullmatch(r"[a-zA-Z0-9]+", value):
            raise ValidationError(
                "Short key can only contain letters and digits of the english alphabet!"
            )

        return value


class ShortenAPIResponse(BaseModel):
    url: HttpUrl


class StatisticsAPIResponse(BaseModel):
    url: HttpUrl
    views: int

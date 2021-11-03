from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from .models import ShortURL
from .settings import SHORT_URL_BASE
from .helpers import generate_random_key


class ShortenAPIRequest(BaseModel):
    url: HttpUrl
    key: Optional[str] = None

class ShortenAPIResponse(BaseModel):
    url: HttpUrl


app = FastAPI()

@app.post("/shorten")
def shorten_url(data: ShortenAPIRequest) -> ShortenAPIResponse:
    """
    Generates a short URL, optionally key can be supplied,
    otherwise it will be an 8 character randomly generated one
    """
    if not data.key:
        data.key = generate_random_key()

    short_url = ShortenAPIResponse(url=SHORT_URL_BASE)
    return short_url
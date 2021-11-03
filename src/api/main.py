from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from .models import ShortURL
from .settings import SHORT_URL_BASE
from .helpers import generate_random_key, get_short_url_or_404
from .types import ShortenAPIRequest, ShortenAPIResponse, StatisticsAPIResponse


app = FastAPI()


@app.post("/shorten")
def shorten_url(data: ShortenAPIRequest) -> ShortenAPIResponse:
    """
    Generates a short URL, optionally key can be supplied,
    otherwise it will be an 8 character randomly generated one
    """
    is_generated_key = False

    if not data.key:
        data.key = generate_random_key()
        is_generated_key = True

    try:
        short_url_object = ShortURL(key=data.key, url=data.url)
        short_url_object.save()
    except ValueError:
        # In case the generated key happened to collide retry generation
        # with an empty key, so a new key will be generated
        if is_generated_key:
            data.key = None
            return shorten_url(data)

        raise HTTPException(status_code=400, detail="Short key has to be unique!")

    short_url_response = ShortenAPIResponse(url=SHORT_URL_BASE + short_url_object.key)
    return short_url_response


@app.get("/statistics/{short_key}")
def statistics(short_key: str) -> StatisticsAPIResponse:
    """Returns view statistics for a shortened URL"""
    short_url_object = get_short_url_or_404(short_key)
    short_url_response = StatisticsAPIResponse(
        url=short_url_object.url, views=short_url_object.view_count
    )
    return short_url_response


@app.get("/{short_key}")
def redirect_to_url(short_key: str):
    """Resolves a short key url and redirects to the URL
    Increases the view count by one in case the url can be resolved
    """
    short_url_object = get_short_url_or_404(short_key)
    ShortURL.increment_view_count(short_url_object)

    return RedirectResponse(short_url_object.url)

import string
import random

from .models import ShortURL
from .types import ShortURLType


def generate_random_key(length: int = 8) -> str:
    """ Generates a random key using uppercase, lowercase ascii letters and digits """
    random_characters = (random.choice(string.ascii_letters + string.digits) for i in range(length))
    return ''.join(random_characters)


def get_short_url_or_404(short_key: str) -> ShortURLType:
    try:
        short_url_object = next(ShortURL.query(short_key))
    except StopIteration:
        return HTTPException(status_code=404, detail=f"URL for short key {short_key} not found!")

    return short_url_object
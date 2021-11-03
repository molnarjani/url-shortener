from .settings import DYNAMO_DB_ENDPOINT_URL

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class ShortURL(Model):
    """
    Database representation of short urls
    """
    class Meta:
        table_name = 'short_urls'
        region = 'us-west-1'
        host = DYNAMO_DB_ENDPOINT_URL
    key = UnicodeAttribute(hash_key=True)
    url = UnicodeAttribute()
    view_count = NumberAttribute(default=0)
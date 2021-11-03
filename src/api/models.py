from .settings import DYNAMO_DB_ENDPOINT_URL

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class ShortURL(Model):
    """
    Database representation of short urls
    """

    class Meta:
        table_name = "short_urls"
        region = "us-west-1"
        host = DYNAMO_DB_ENDPOINT_URL

    key = UnicodeAttribute(hash_key=True)
    url = UnicodeAttribute()
    view_count = NumberAttribute(default=0)

    def validate_key_uniqueness(self, value: str) -> None:
        """Check if key is unique by querying from dynamoDB"""
        try:
            item = next(self.query(value))
            if item:
                raise ValueError("Key has to be unique!")
        except StopIteration:
            return

    def save(self, *args, **kwargs):
        self.validate_key_uniqueness(self.key)
        super().save(*args, **kwargs)

    @classmethod
    def increment_view_count(cls, instance) -> None:
        instance.update(actions=[cls.view_count.set(instance.view_count + 1)])

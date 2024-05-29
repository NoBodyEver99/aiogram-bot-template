from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class Channel(Model, BaseHelper):
    id = fields.IntField(pk=True)
    # Main Info
    chat_id = fields.BigIntField(null=False, unique=True)
    title = fields.CharField(null=False, max_length=64)
    url = fields.CharField(null=False, max_length=64)
    # Created At
    created_at = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = "channels"

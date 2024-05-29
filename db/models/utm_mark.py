from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class UtmMark(Model, BaseHelper):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, unique=True)
    transitions = fields.IntField(default=0)

    class Meta:
        table = "utm_marks"

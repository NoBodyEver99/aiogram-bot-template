from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class Newsletter(Model, BaseHelper):
    id = fields.IntField(pk=True)
    # Main Info
    owner = fields.ForeignKeyField("models.User", related_name="owned_newsletters")
    status = fields.CharField(8, default="stopped")
    # Newsletter Info
    text = fields.TextField(null=True)
    media = fields.CharField(128, null=True)
    media_type = fields.CharField(8, null=True)
    keyboard = fields.TextField(null=True)
    # Users
    users = fields.ManyToManyField("models.User", related_name="newsletters", through="models.NewsletterUser")
    # Created At
    created_at = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = "newsletter"

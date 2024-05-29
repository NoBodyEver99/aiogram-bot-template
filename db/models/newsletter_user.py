from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class NewsletterUser(Model, BaseHelper):
    user = fields.ForeignKeyField("models.User", related_name="newsletter_users")
    newsletter = fields.ForeignKeyField("models.Newsletter", related_name="newsletter_users")
    success = fields.BooleanField(default=False)

    user: fields.ReverseRelation["User"]
    newsletter: fields.ReverseRelation["Newsletter"]

    class Meta:
        table = "newsletter_users"
        unique_together = ("newsletter", "user")

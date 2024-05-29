from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class Referral(Model, BaseHelper):
    id = fields.IntField(pk=True)
    # Main Info
    inviter = fields.ForeignKeyField("models.User", related_name="referrals")
    invited = fields.ForeignKeyField("models.User", related_name="invited_as_referral")
    # Created At
    created_at = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = "referrals"

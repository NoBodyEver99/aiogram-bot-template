from tortoise.models import Model
from tortoise import fields

from db.helpers import BaseHelper


class User(Model, BaseHelper):
    id = fields.IntField(pk=True)
    # Main Info
    user_id = fields.BigIntField(null=False, unique=True)
    first_name = fields.CharField(max_length=128, null=False)
    last_name = fields.CharField(max_length=128, null=True)
    username = fields.CharField(max_length=64, null=True)
    # Referral
    referrals: fields.ReverseRelation["Referral"]
    invited_as_referral: fields.ReverseRelation["Referral"]
    # Created At && Updated At
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

    class Meta:
        table = "users"

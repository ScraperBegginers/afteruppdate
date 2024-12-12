from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(pk=True, unique=True)
    username = fields.CharField(max_length=255, null=True)
    registration = fields.BooleanField(default=False)

    class Meta:
        table = "users"

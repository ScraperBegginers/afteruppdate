from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(pk=True, unique=True)
    username = fields.CharField(max_length=255, null=True)
    registration = fields.BooleanField(default=False)

    class Meta:
        table = "users"

class ReferralLinks(Model):
    link_id = fields.BigIntField(pk=True, unique=True)
    link = fields.CharField(max_length=255, null=True)
    
    class Meta:
        table = "referral_links"
        
class HistoryReferralLinks(Model):
    link_id = fields.BigIntField(pk=True, unique=True)
    link = fields.CharField(max_length=255, null=True)
    user_id = fields.BigIntField()
    
    class Meta:
        table = "history_referral_links"
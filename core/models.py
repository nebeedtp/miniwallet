import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    customer_xid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)


class MyWallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField(User,  null=True, blank= True, db_column='user_id', related_name="user_id", on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    status = models.CharField(max_length=10, default='disabled')
    enabled_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)

class WalletTransactions(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User,  null=True, blank= True, db_column='user_id', related_name="customer_id", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_added = models.DateTimeField(null=True)
    reference_id = models.CharField(max_length=100, blank=True, default=uuid.uuid4)
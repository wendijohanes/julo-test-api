import datetime
import uuid
import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

from datetime import datetime

# Create your models here.
class ProfileUser(models.Model):
	class Meta:
		db_table = 'profile_user'

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	uuid_user = models.CharField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100,default="")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		ProfileUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profileuser.save()

class Wallet(models.Model):
	class Meta:
		db_table = 'wallet'

	id_wallet = models.BigAutoField(primary_key=True)
	owner = models.OneToOneField(User, on_delete=models.CASCADE)
	uuid_wallet = models.CharField(default=uuid.uuid4, editable=False,max_length=50)
	balance = models.IntegerField(default=0)
	enable = models.BooleanField(default=False)
	time_enabled = models.DateTimeField(blank=True,null=True)

class Deposit(models.Model):
	class Meta:
		db_table = 'deposit'

	id_deposit = models.BigAutoField(primary_key=True)
	uuid_deposit = models.CharField(default=uuid.uuid4, editable=False,max_length=50)
	time_deposit = models.DateTimeField(default=datetime.now)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.IntegerField()
	reference_id = models.CharField(blank=True,max_length=100)

class Withdrawal(models.Model):
	class Meta:
		db_table = 'withdrawal'

	id_withdrawal = models.BigAutoField(primary_key=True)
	uuid_withdrawal = models.CharField(default=uuid.uuid4, editable=False,max_length=50)
	time_withdrawal = models.DateTimeField(default=datetime.now)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.IntegerField()
	reference_id = models.CharField(blank=True,max_length=100)

class FundStatement(models.Model):
	class Meta:
		db_table = 'fund_statement'

	id_statement = models.BigAutoField(primary_key=True)
	uuid_statement = models.CharField(default=uuid.uuid4, editable=False,max_length=50)
	time_statement = models.DateTimeField(default=datetime.now)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.IntegerField()
	type_fund = models.CharField(max_length=15) #DEPOSIT,WITHDRAWAL


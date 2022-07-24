from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

import locale
import datetime
from django.db.models import Q
from django.db.models import F, FloatField,IntegerField
from django.db.models import Sum
from django.db.models.functions import Cast, Coalesce

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions, serializers
#from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from django.contrib.auth.models import User
from .models import ProfileUser, Wallet
from .models import Deposit, Withdrawal, FundStatement
from rest_framework.authtoken.models import Token

#testing
class HelloView(APIView):
	permission_classes = [IsAuthenticated,]

	def get(self, request):
		ID_USER = request.user.id
		USERNAME_USER = request.user.username
		FULL_NAME_USER = request.user.profileuser.full_name
		txtHello = "Hello, " + str(NAMA_USER)
		#txtHello = "Hello, It's Julo API TEST!"

		content = {'message': txtHello, 'nama_user': NAMA_USER}
		content = {'message': txtHello}
		return Response(content)

class InitView(APIView):

	def post(self,request):
		#form body request
		customer_xid = request.POST['customer_xid']
		newUsername = "julo" + customer_xid[0:5]

		#validate user by xid
		pu = ProfileUser.objects.filter(uuid_user=customer_xid)
		if pu.count() > 0:
			content = {'data': 'This XID Customer already registered.', 'status': 'fail'}
			return Response(content)
		
		#new user
		newUser = User.objects.create_user(username=newUsername)
		newUser.profileuser.uuid_user=customer_xid
		newUser.profileuser.full_name = newUsername.upper()
		newUser.save()

		#new wallet
		newWallet = Wallet(owner=newUser)
		newWallet.save()

		token = Token.objects.create(user=newUser)
		print(token.key)

		content = {'data': {'token': str(token.key) }, 'status': 'success'}
		return Response(content)

class WalletView(APIView):
	permission_classes = [IsAuthenticated,]

	def get(self, request):
		#user
		ID_USER = request.user.id

		#check wallet
		wallet = Wallet.objects.get(owner_id=ID_USER)
		if wallet.enable == False:
			content = {'data': 'This wallet is disabled. Please enable your wallet first.' , 'status': 'fail'}
			return Response(content)

		content = {'data': {'wallet': {'id_wallet': wallet.uuid_wallet, 'owned_by': wallet.owner.profileuser.uuid_user, 'balance': wallet.balance, 'enabled_at': wallet.time_enabled, 'status': 'enabled'}}, 'status': 'success'}
		return Response(content)

	def post(self,request):
		#user
		ID_USER = request.user.id

		#check wallet
		wallet = Wallet.objects.get(owner_id=ID_USER)
		if wallet.enable == True:
			content = {'data': 'Wallet already enabled' , 'status': 'fail'}
			return Response(content)

		#enable wallet
		wallet.enable = True
		current_datetime = datetime.datetime.now() 
		wallet.time_enabled = current_datetime
		wallet.save()

		content = {'data': {'wallet': {'id_wallet': wallet.uuid_wallet, 'owned_by': wallet.owner.profileuser.uuid_user, 'balance': wallet.balance, 'enabled_at': current_datetime, 'status': 'enabled'}}, 'status': 'success'}
		return Response(content)

	def patch(self,request):
		#user
		ID_USER = request.user.id
		IS_DISABLED = request.POST['is_disabled']

		wallet = Wallet.objects.get(owner_id=ID_USER)

		#disable wallet
		if IS_DISABLED.lower() == "true":
			wallet.enable = False
		elif IS_DISABLED.lower() == "false":
			wallet.enable = True
		else:
			content = {'data': 'Is Disabled value must be either true or false' , 'status': 'fail'}
			return Response(content)

		current_datetime = datetime.datetime.now() 
		wallet.save()

		content = {'data': {'wallet': {'id_wallet': wallet.uuid_wallet, 'owned_by': wallet.owner.profileuser.uuid_user, 'balance': wallet.balance, 'disabled_at': current_datetime, 'status': IS_DISABLED }}, 'status': 'success'}
		return Response(content)

class DepositView(APIView):
	permission_classes = [IsAuthenticated,]

	def post(self,request):
		#user
		ID_USER = request.user.id
		reference_id = request.POST['reference_id']
		amount = abs(int(request.POST['amount']))

		#check wallet
		wallet = Wallet.objects.get(owner_id=ID_USER)
		if wallet.enable == False:
			content = {'data': 'Wallet is disabled. Please enable it first.' , 'status': 'fail'}
			return Response(content)

		#deposit process
		dp = Deposit(wallet_id=wallet.pk,amount=amount,reference_id=reference_id)
		dp.save()

		#update wallet balance
		Wallet.objects.filter(pk=wallet.id_wallet).update(balance=F("balance") + amount)

		#create new fund statement
		st = FundStatement(wallet_id=wallet.pk,amount=amount,type_fund="DEPOSIT")
		st.save()

		content = { 'status': 'success' , 'data': {'deposit':{'id': dp.id_deposit, 'status': 'success', 'amount': amount ,'reference_id': reference_id, 'deposit_at': dp.time_deposit, 'deposit_by': dp.wallet.owner.profileuser.uuid_user }}}
		return Response(content)

class WithdrawalView(APIView):
	permission_classes = [IsAuthenticated,]

	def post(self,request):
		#user
		ID_USER = request.user.id
		reference_id = request.POST['reference_id']
		amount = abs(int(request.POST['amount']))

		#check wallet
		wallet = Wallet.objects.get(owner_id=ID_USER)
		if wallet.enable == False:
			content = {'data': 'Wallet is disabled. Please enable it first.' , 'status': 'fail'}
			return Response(content)

		#check balance
		if amount > wallet.balance:
			content = {'data': 'Not Enought balance' , 'status': 'fail'}
			return Response(content)

		#withdrawal process
		wd = Withdrawal(wallet_id=wallet.pk,amount=amount,reference_id=reference_id)
		wd.save()

		#update wallet balance
		Wallet.objects.filter(pk=wallet.id_wallet).update(balance=F("balance") - amount)

		#create new fund statement
		st = FundStatement(wallet_id=wallet.pk,amount=-(amount),type_fund="WITHDRAWAL")
		st.save()

		content = { 'status': 'success' , 'data': {'withdrawal': {'id': wd.id_withdrawal, 'status': 'success', 'amount': amount ,'reference_id': reference_id, 'withdraw_at': wd.time_withdrawal, 'withdrawal_by': wd.wallet.owner.profileuser.uuid_user }}}
		return Response(content)

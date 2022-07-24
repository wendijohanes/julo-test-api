from django.urls import path
from django.conf import settings
from django.urls import include, re_path

from . import backend_hello

app_name = 'julo_api'

urlpatterns = [
	path('hello', backend_hello.HelloView.as_view(), name='hello'),
	path('init', backend_hello.InitView.as_view(), name='init'),
	path('wallet', backend_hello.WalletView.as_view(), name='wallet'),

	path('wallet/deposits', backend_hello.DepositView.as_view(), name='deposit'),
	path('wallet/withdrawals', backend_hello.WithdrawalView.as_view(), name='withdrawal'),

]

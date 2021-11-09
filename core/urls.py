

from django.urls import path
from . import views


urlpatterns = [
    path('init', views.TokenView.as_view(), name='init'),
    path('wallet', views.WalletView.as_view(), name='enable'),
    path('wallet/deposits', views.DepositView.as_view(), name='deposit'),
    path('wallet/withdrawals', views.WithdrawalView.as_view(), name='withdrawals'),
]

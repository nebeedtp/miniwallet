from django.db.models import fields
from rest_framework import serializers
from .models import User,MyWallet,WalletTransactions

class TokenSerializer(serializers.Serializer):

    customer_xid = serializers.CharField()

    def validate(self, data):
        customer_id_exists = User.objects.filter(customer_xid = data['customer_xid']).count()
        if not customer_id_exists:
            raise serializers.ValidationError("Invalid Customer XID")
        return data

class EnableWalletSerilizer(serializers.Serializer):

    def validate(self, data):
        user =  self.context['request'].user
        wallet_already_enabled = MyWallet.objects.filter(user_id = user, status = "enabled").count()
        if wallet_already_enabled:
            raise serializers.ValidationError("Wallet Alreaady Enabled")
        return data

class WalletSerilizer(serializers.Serializer):

    def validate(self, data):
        user =  self.context['request'].user
        wallet_exists = MyWallet.objects.filter(user_id = user).count()
        if not wallet_exists:
            raise serializers.ValidationError("Wallet not exists for this user")
        return data

class ViewWalletSerilizer(serializers.Serializer):

    def validate(self, data):
        user =  self.context['request'].user
        wallet_enabled = MyWallet.objects.filter(user_id = user, status = "enabled").count()
        if not wallet_enabled:
            raise serializers.ValidationError("Wallet is not enabled")
        return data


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransactions
        fields = ['amount', 'reference_id']
        extra_kwargs = {'amount': {'required': True}, 'reference_id': {'required': True}}

    def validate(self, data):
        if data['amount'] < 1:
            raise serializers.ValidationError("Please enter an amount greater than zero")
        
        user =  self.context['request'].user
        wallet_enabled = MyWallet.objects.filter(user_id = user, status = "enabled").count()
        if not wallet_enabled:
            raise serializers.ValidationError("Wallet is not enabled")
        
        return data

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransactions
        fields = ['amount', 'reference_id']
        extra_kwargs = {'amount': {'required': True}, 'reference_id': {'required': True}}

    def validate(self, data):
        if data['amount'] < 1:
            raise serializers.ValidationError("Please enter an amount greater than zero")
        
        user =  self.context['request'].user

        wallet_enabled = MyWallet.objects.filter(user_id = user, status = "enabled").count()
        if not wallet_enabled:
            raise serializers.ValidationError("Wallet is not enabled")

        wallet_balance = MyWallet.objects.values_list('balance', flat=True).get(user_id = user)
        if data['amount'] > wallet_balance:
            raise serializers.ValidationError("Insufficient balance")
        
        return data 



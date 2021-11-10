from django.db.models import fields

from .models import User,MyWallet,WalletTransactions

from rest_framework import serializers

class TokenSerializer(serializers.Serializer):

    customer_xid = serializers.CharField()

    def validate(self, data):
        customer_id_exists = User.objects.filter(customer_xid = data['customer_xid']).count()
        if not customer_id_exists:
            raise serializers.ValidationError("Invalid Customer XID")
        return data


class WalletSerializer(serializers.Serializer):

    def validate(self, data):
        user =  self.context['request'].user
        wallet_exists = MyWallet.objects.filter(user_id = user).count()
        if not wallet_exists:
            raise serializers.ValidationError("Wallet not exists for this user")

        wallet_enabled = MyWallet.objects.filter(user_id = user, status = 'enabled').count()
        if wallet_enabled:
            raise serializers.ValidationError("Your wallet is already enabled")

        return data

class DisableWalletSerializer(serializers.Serializer):

    def validate(self, data):
        user =  self.context['request'].user
        wallet_exists = MyWallet.objects.filter(user_id = user).count()
        if not wallet_exists:
            raise serializers.ValidationError("Wallet not exists for this user")

        wallet_enabled = MyWallet.objects.filter(user_id = user, status = 'disabled').count()
        if wallet_enabled:
            raise serializers.ValidationError("Your wallet is already disabled")

        return data

class ViewWalletSerializer(serializers.Serializer):

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
        
        reference_id_existis = WalletTransactions.objects.filter(reference_id = data['reference_id'], type = 'credit').exists()
        if reference_id_existis:
            raise serializers.ValidationError("Reference ID already exists")
        
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

        reference_id_existis = WalletTransactions.objects.filter(reference_id = data['reference_id'], type = 'debit').exists()
        if reference_id_existis:
            raise serializers.ValidationError("Reference ID already exists")
        
        return data 



import datetime


from django.db import transaction
from django.db.models import F



from .models import User,MyWallet
from .serializers import TokenSerializer,WalletSerilizer,ViewWalletSerilizer,DepositSerializer,WithdrawalSerializer


from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class TokenView(APIView):

    def post(self, request):

        serializer = TokenSerializer(data = request.data)
        if serializer.is_valid():
            customer_xid = request.data['customer_xid']
            user = User.objects.get(customer_xid = customer_xid)
            token, _ = Token.objects.get_or_create(user = user)
            wallet_created = MyWallet.objects.filter(user_id = user).count()
            if not wallet_created:
                MyWallet.objects.create(user_id = user)
            data = {
                'token': (token.key),
            }
            content = {'data': data, 'status' : "success"}
            return Response(content)

        return Response(serializer.errors)


class WalletView(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        context = {'request': self.request}
        serializer = ViewWalletSerilizer(data = request.data, context = context)
        if serializer.is_valid():
            user = request.user
            wallet_data = MyWallet.objects.get(user_id = user)
            data = {
                "wallet" : {
                    "id" : wallet_data.id,
                    "owned_by" : wallet_data.user_id.customer_xid,
                    "status": wallet_data.status,
                    "enabled_at": wallet_data.enabled_at,
                    "balance" : wallet_data.balance,
                }
            }
            content = {'message': 'success', 'data' : data}
            return Response(content)

        return Response(serializer.errors)

    def post(self, request):
        current_time = datetime.datetime.now()
        context = {'request': self.request}
        serializer = WalletSerilizer(data = request.data, context = context)
        if serializer.is_valid():
            user = request.user
            wallet_data = MyWallet.objects.get(user_id = user)
            if wallet_data.status == "enabled":
                wallet_data.status = "disabled"
                wallet_data.disabled_at = current_time
                wallet_data.save()
                data = {
                    "wallet" : {
                        "id" : wallet_data.id,
                        "owned_by" : wallet_data.user_id.customer_xid, 
                        "status": "disabled",
                        "disabled_at": current_time,
                        "balance" : wallet_data.balance,
                    }
                }
            else:
                wallet_data.status = "enabled"
                wallet_data.enabled_at = current_time
                wallet_data.save()
                data = {
                    "wallet" : {
                        "id" : wallet_data.id,
                        "owned_by" : wallet_data.user_id.customer_xid,
                        "status": "enabled",
                        "enabled_at": current_time,
                        "balance" : wallet_data.balance,
                    }
                }

            content = {'message': 'success', 'data' : data}
            return Response(content)

        return Response(serializer.errors)


class DepositView(APIView):

    def post(self, request):
        current_time = datetime.datetime.now()
        context = {'request': self.request}
        serializer = DepositSerializer(data = request.data, context = context)
        if serializer.is_valid():
            with transaction.atomic():
                user = request.user
                amount = request.data['amount']
                reference_id = request.data['reference_id']
                MyWallet.objects.filter(user_id=user).update(balance=F('balance') + amount)
                deposit = serializer.save(user_id = user, amount = amount, status='success', type = 'credit', date_added = current_time, reference_id = reference_id)
                data = {
                    "deposit" : {
                        "id" : deposit.id,
                        "deposited_by" : deposit.user_id.customer_xid,
                        "status": deposit.status,
                        "deposited_at": deposit.date_added,
                        "amount" : deposit.amount,
                        "reference_id" : deposit.reference_id,
                    }
                }
                content = {'status' : "success", 'data': data}
                return Response(content)

        return Response(serializer.errors)

class WithdrawalView(APIView):

    def post(self, request):
        current_time = datetime.datetime.now()
        context = {'request': self.request}
        serializer = WithdrawalSerializer(data = request.data, context = context)
        if serializer.is_valid():
            with transaction.atomic():
                user = request.user
                amount = request.data['amount']
                reference_id = request.data['reference_id']
                MyWallet.objects.filter(user_id=user).update(balance=F('balance')  - amount)
                deposit = serializer.save(user_id = user, amount = amount, status='success', type = 'debit', date_added = current_time, reference_id = reference_id)
                data = {
                    "withdrawal" : {
                        "id" : deposit.id,
                        "withdrawn_by" : deposit.user_id.customer_xid,
                        "status": deposit.status,
                        "withdrawn_at": deposit.date_added,
                        "amount" : deposit.amount,
                        "reference_id" : deposit.reference_id,
                    }
                }
                content = {'status' : "success", 'data': data}
                return Response(content)

        return Response(serializer.errors)
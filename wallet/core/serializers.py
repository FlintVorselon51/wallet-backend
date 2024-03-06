from rest_framework import serializers

from core.models import Currency, Wallet, TransactionCategory, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name', 'code', 'symbol')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'currency', 'name', 'balance')


class WalletSerializerWithoutBalance(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'currency', 'name')


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ('id', 'name', 'is_expense')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'category', 'executed_at', 'value', 'title', 'description', 'is_expense')

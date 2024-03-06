from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Currency(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=8)


class Wallet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    class Meta:
        unique_together = (('creator', 'name'),)


class TransactionCategory(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    is_expense = models.BooleanField()

    class Meta:
        unique_together = (('creator', 'name'),)


class Transaction(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True)
    executed_at = models.DateTimeField()
    value = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    title = models.CharField(max_length=32, blank=True)
    description = models.TextField(blank=True)
    is_expense = models.BooleanField()

import decimal
from abc import ABC, abstractmethod
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework.serializers import Serializer

from tools.exceptions import UnprocessableEntity
from core.models import Wallet, TransactionCategory, Transaction


User = get_user_model()


class TransactionQuerySetService:

    def __init__(self, user: User, query_params) -> None:
        self.user: User = user
        self.query_params = query_params

    def execute(self) -> QuerySet:
        queryset = Transaction.objects.filter(creator=self.user)

        executed_at = self.query_params.get('executed_at')
        wallet_id = self.query_params.get('wallet_id')
        category_id = self.query_params.get('category_id')

        if executed_at:
            queryset = queryset.filter(executed_at__date=datetime.strptime(executed_at, '%Y-%m-%d'))

        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


class AbstractTransactionPerformService(ABC):
    wallet: Wallet | None
    category: TransactionCategory | None
    value: decimal.Decimal
    is_expense: bool | None

    def __init__(self, user: User, serializer: Serializer) -> None:
        self.user: User = user
        self.serializer: Serializer = serializer

    def _check_is_expense_fields_are_same(self):
        if self.is_expense is not None and self.category is not None:
            if self.is_expense != self.category.is_expense:
                raise UnprocessableEntity('Transaction and category "is_expense" fields cannot be different.')

    def _check_wallet_belongs_to_user(self):
        try:
            Wallet.objects.get(creator=self.user, id=self.wallet.id)
        except Wallet.DoesNotExist:
            raise UnprocessableEntity('Provided wallet does not exist.')

    def _check_category_belongs_to_user(self):
        if not self.category:
            return
        try:
            TransactionCategory.objects.get(creator=self.user, id=self.category.id)
        except TransactionCategory.DoesNotExist:
            raise UnprocessableEntity('Provided category does not exist.')

    @abstractmethod
    def execute(self) -> None:
        self.wallet = self.serializer.validated_data.get('wallet')
        self.category = self.serializer.validated_data.get('category')
        self.value = self.serializer.validated_data.get('value')
        self.is_expense = self.serializer.validated_data.get('is_expense')


class TransactionCreateService(AbstractTransactionPerformService):

    def execute(self) -> None:
        super(TransactionCreateService, self).execute()

        self._check_is_expense_fields_are_same()
        self._check_wallet_belongs_to_user()
        self._check_category_belongs_to_user()
        self._calculate_and_set_new_balance_to_wallet()

        with atomic():
            self._save_wallet()
            self.serializer.save(creator=self.user)

    def _calculate_and_set_new_balance_to_wallet(self):
        if self.is_expense:
            self.wallet.balance -= self.value
        else:
            self.wallet.balance += self.value

    def _save_wallet(self):
        try:
            self.wallet.save()
        except decimal.InvalidOperation:
            raise UnprocessableEntity('The balance of your wallet will be to big after the provided transaction.')


class TransactionUpdateService(AbstractTransactionPerformService):

    def execute(self) -> None:
        super(TransactionUpdateService, self).execute()

        if self.wallet is None:
            self.wallet = self.serializer.instance.wallet
        if self.value is None:
            self.value = self.serializer.instance.value

        self._check_is_expense_fields_are_same()
        self._check_wallet_belongs_to_user()
        self._check_category_belongs_to_user()
        self._change_wallet_balances()

        with atomic():
            self._save_wallets()
            self.serializer.save(creator=self.user)

    def _change_wallet_balances(self):
        if self.serializer.instance.is_expense:
            self.serializer.instance.wallet.balance += self.serializer.instance.value
        else:
            self.serializer.instance.wallet.balance -= self.serializer.instance.value

        if self.is_expense:
            self.wallet.balance -= self.value
        else:
            self.wallet.balance += self.value

    def _save_wallets(self):
        try:
            self.serializer.instance.wallet.save()
            self.wallet.save()
        except decimal.InvalidOperation:
            raise UnprocessableEntity('The balance of your wallet will be to big after the provided transaction.')


class TransactionDestroyService:
    user: User
    transaction: Transaction

    wallet: Wallet

    def __init__(self, user: User, transaction: Transaction):
        self.user = user
        self.transaction = transaction

    def execute(self):
        self.wallet = self.transaction.wallet
        self._calculate_and_set_new_balance_to_wallet()

        with atomic():
            self._save_wallet()
            self.transaction.delete()

    def _calculate_and_set_new_balance_to_wallet(self):
        if self.transaction.is_expense:
            self.wallet.balance += self.transaction.value
        else:
            self.wallet.balance -= self.transaction.value

    def _save_wallet(self):
        try:
            self.wallet.save()
        except decimal.InvalidOperation:
            raise UnprocessableEntity('The balance of your wallet will be to big after the provided transaction.')

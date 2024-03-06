from abc import ABC, abstractmethod
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from tools.exceptions import Conflict, UnprocessableEntity
from core.models import Currency, Wallet


User = get_user_model()


class WalletQuerySetService:

    def __init__(self, user: User) -> None:
        self.user: User = user

    def execute(self) -> QuerySet:
        return Wallet.objects.filter(creator=self.user)


class AbstractWalletPerformService(ABC):
    currency: Currency
    name: str
    balance: Decimal | None

    def __init__(self, user: User, serializer: Serializer) -> None:
        self.user: User = user
        self.serializer: Serializer = serializer

    def _check_user_does_not_have_wallet_with_same_name(self) -> None:
        try:
            wallet = Wallet.objects.get(creator=self.user, name=self.name)
        except Wallet.DoesNotExist:
            return
        if wallet != self.serializer.instance:
            raise Conflict('The user already has a wallet with provided name.')

    @abstractmethod
    def execute(self) -> None:
        pass


class WalletCreateService(AbstractWalletPerformService):

    def execute(self) -> None:
        self.name = self.serializer.validated_data.get('name')
        self.balance = self.serializer.validated_data.get('balance')

        self._check_user_does_not_have_wallet_with_same_name()

        self.serializer.save(creator=self.user)


class WalletUpdateService(AbstractWalletPerformService):

    def execute(self) -> None:
        self.currency = self.serializer.validated_data.get('currency')
        self.name = self.serializer.validated_data.get('name')

        self._check_user_does_not_have_wallet_with_same_name()
        self._check_user_is_not_trying_to_change_currency()

        self.serializer.save(creator=self.user)

    def _check_user_is_not_trying_to_change_currency(self) -> None:
        if self.currency and self.currency != self.serializer.instance.currency:
            raise UnprocessableEntity('Currency of the wallet cannot be edited.')

from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from tools.exceptions import Conflict, UnprocessableEntity
from core.models import TransactionCategory


User = get_user_model()


class TransactionCategoryQuerySetService:

    def __init__(self, user: User) -> None:
        self.user: User = user

    def execute(self) -> QuerySet:
        return TransactionCategory.objects.filter(creator=self.user)


class AbstractTransactionCategoryPerformService(ABC):
    name: str
    is_expense: bool

    def __init__(self, user: User, serializer: Serializer) -> None:
        self.user: User = user
        self.serializer: Serializer = serializer

    def _check_user_does_not_have_transaction_category_with_same_name(self) -> None:
        try:
            transaction_category = TransactionCategory.objects.get(creator=self.user, name=self.name)
        except TransactionCategory.DoesNotExist:
            return
        if transaction_category != self.serializer.instance:
            raise Conflict('The user already has a wallet with provided name.')

    @abstractmethod
    def execute(self) -> None:
        pass


class TransactionCategoryCreateService(AbstractTransactionCategoryPerformService):

    def execute(self) -> None:
        self.name = self.serializer.validated_data.get('name')

        self._check_user_does_not_have_transaction_category_with_same_name()

        self.serializer.save(creator=self.user)


class TransactionCategoryUpdateService(AbstractTransactionCategoryPerformService):

    def execute(self) -> None:
        self.name = self.serializer.validated_data.get('name')
        self.is_expense = self.serializer.validated_data.get('is_expense')

        self._check_user_does_not_have_transaction_category_with_same_name()
        self._check_user_is_not_trying_to_change_is_expense()

        self.serializer.save(creator=self.user)

    def _check_user_is_not_trying_to_change_is_expense(self) -> None:
        if self.is_expense is not None and self.is_expense != self.serializer.instance.is_expense:
            raise UnprocessableEntity('"is_expense" field of the category cannot be edited.')

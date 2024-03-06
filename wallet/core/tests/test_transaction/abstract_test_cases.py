from abc import ABC
from typing import Any, Iterable

from django.urls import reverse

from tools.test import AuthenticatedAPITestCase
from core.models import Wallet, TransactionCategory, Transaction
from core.tests.factories import WalletFactory, TransactionCategoryFactory, TransactionFactory


class AbstractTransactionTestCase(AuthenticatedAPITestCase, ABC):

    def setUp(self) -> None:
        super(AbstractTransactionTestCase, self).setUp()
        self.existing_transaction = TransactionFactory(creator=self.user)

    def _assert_transaction_fields_in_container(self, container) -> None:
        self.assertEqual(len(container), 8)
        self.assertIn('id', container)
        self.assertIn('wallet', container)
        self.assertIn('category', container)
        self.assertIn('executed_at', container)
        self.assertIn('value', container)
        self.assertIn('title', container)
        self.assertIn('description', container)
        self.assertIn('is_expense', container)

    @staticmethod
    def _create_transaction_for_user(user, **kwargs) -> Transaction:
        return TransactionFactory(creator=user, **kwargs)

    @staticmethod
    def _create_wallet_for_user(user, **kwargs) -> Wallet:
        return WalletFactory(creator=user, **kwargs)

    @staticmethod
    def _create_category_for_user(user, **kwargs) -> TransactionCategory:
        return TransactionCategoryFactory(creator=user, **kwargs)

    @staticmethod
    def _get_id_of_non_existing_wallet() -> int:
        return Wallet.objects.count() + 1

    @staticmethod
    def _get_id_of_non_existing_category() -> int:
        return TransactionCategory.objects.count() + 1

    @staticmethod
    def _form_transaction_payload_for_user(
            user,
            excluded_fields: Iterable[str] | None = None,
            **kwargs
    ) -> dict[str, Any]:

        if excluded_fields is None:
            excluded_fields = tuple()

        instance = TransactionFactory.create(creator=user, **kwargs)

        if 'is_expense' in kwargs:
            instance.category.is_expense = kwargs.get('is_expense')
            instance.category.save()

        payload = {
            'wallet': instance.wallet.id,
            'category': instance.category.id,
            'executed_at': instance.executed_at,
            'value': instance.value,
            'title': instance.title,
            'description': instance.description,
            'is_expense': instance.is_expense
        }

        for excluded_field in excluded_fields:
            payload.pop(excluded_field)

        return payload


class AbstractTransactionListTestCase(AbstractTransactionTestCase, ABC):
    url = reverse('core:transaction-list')


class AbstractTransactionDetailTestCase(AbstractTransactionTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractTransactionDetailTestCase, self).setUp()
        self.url = reverse('core:transaction-detail', args=(self.existing_transaction.id,))

    @staticmethod
    def _generate_url_for_transaction(transaction: Transaction) -> str:
        return reverse('core:transaction-detail', args=(transaction.id,))

    @staticmethod
    def _generate_url_for_non_existing_transaction() -> str:
        non_existing_transaction_id = Transaction.objects.count() + 1
        url = reverse('core:transaction-detail', args=(non_existing_transaction_id,))

        return url

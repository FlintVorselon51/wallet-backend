from abc import ABC
from typing import Any, Iterable

from django.urls import reverse

from tools.test import AuthenticatedAPITestCase
from core.models import TransactionCategory
from core.tests.factories import TransactionCategoryFactory


class AbstractTransactionCategoryTestCase(AuthenticatedAPITestCase, ABC):

    def setUp(self) -> None:
        super(AbstractTransactionCategoryTestCase, self).setUp()
        self.existing_transaction_category = TransactionCategoryFactory(creator=self.user)

    def _assert_transaction_category_fields_in_container(self, container) -> None:
        self.assertEqual(len(container), 3)
        self.assertIn('id', container)
        self.assertIn('name', container)
        self.assertIn('is_expense', container)

    @staticmethod
    def _get_id_of_non_existing_transaction_category() -> int:
        return TransactionCategory.objects.count() + 1

    @staticmethod
    def _create_new_transaction_category_for_user(user) -> TransactionCategory:
        return TransactionCategoryFactory(creator=user)

    def _form_transaction_category_payload(
            self,
            excluded_fields: Iterable[str] | None = None,
            **kwargs
    ) -> dict[str, Any]:

        if excluded_fields is None:
            excluded_fields = tuple()

        stub = TransactionCategoryFactory.stub(**kwargs)

        if 'is_expense' in kwargs:
            is_expense = kwargs.get('is_expense')
        else:
            is_expense = self.existing_transaction_category.is_expense

        payload = {
            'name': stub.name,
            'is_expense': is_expense
        }

        for excluded_field in excluded_fields:
            payload.pop(excluded_field)

        return payload


class AbstractTransactionCategoryListTestCase(AbstractTransactionCategoryTestCase, ABC):
    url = reverse('core:transaction-category-list')


class AbstractTransactionCategoryDetailTestCase(AbstractTransactionCategoryTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractTransactionCategoryDetailTestCase, self).setUp()
        self.url = reverse('core:transaction-category-detail', args=(self.existing_transaction_category.id,))

    @classmethod
    def _generate_url_for_non_existing_transaction_category(cls) -> str:
        return reverse('core:transaction-category-detail', args=(cls._get_id_of_non_existing_transaction_category(),))

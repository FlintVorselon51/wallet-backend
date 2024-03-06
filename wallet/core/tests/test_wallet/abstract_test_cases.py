from abc import ABC
from typing import Any, Iterable

from django.urls import reverse
from factory.base import StubObject

from tools.test import AuthenticatedAPITestCase
from core.models import Currency, Wallet
from core.tests.factories import CurrencyFactory, WalletFactory


class AbstractWalletTestCase(AuthenticatedAPITestCase, ABC):

    def setUp(self) -> None:
        super(AbstractWalletTestCase, self).setUp()
        self.existing_wallet = WalletFactory(creator=self.user)

    def _assert_wallet_fields_in_container_without_balance(self, container) -> None:
        self.assertEqual(len(container), 3)
        self.assertIn('id', container)
        self.assertIn('currency', container)
        self.assertIn('name', container)

    def _assert_wallet_fields_in_container(self, container) -> None:
        self.assertEqual(len(container), 4)
        self.assertIn('id', container)
        self.assertIn('currency', container)
        self.assertIn('name', container)
        self.assertIn('balance', container)

    @staticmethod
    def _get_id_of_non_existing_currency() -> int:
        return Currency.objects.count() + 1

    @staticmethod
    def _create_new_currency() -> Currency:
        return CurrencyFactory()

    @staticmethod
    def _create_new_wallet_for_user(user) -> Wallet:
        return WalletFactory(creator=user)

    def _form_wallet_payload(
            self,
            excluded_fields: Iterable[str] | None = None,
            **kwargs
    ) -> dict[str, Any]:

        if excluded_fields is None:
            excluded_fields = tuple()

        stub = WalletFactory.stub(**kwargs)

        if 'currency_id' in kwargs:
            currency = kwargs.get('currency_id')
        elif type(stub.currency) is StubObject:
            currency = self.existing_wallet.currency.id
        else:
            currency = stub.currency.id

        payload = {
            'currency': currency,
            'name': stub.name,
        }

        for excluded_field in excluded_fields:
            payload.pop(excluded_field)

        return payload


class AbstractWalletListTestCase(AbstractWalletTestCase, ABC):
    url = reverse('core:wallet-list')


class AbstractWalletDetailTestCase(AbstractWalletTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractWalletDetailTestCase, self).setUp()
        self.url = reverse('core:wallet-detail', args=(self.existing_wallet.id,))

    @staticmethod
    def _generate_url_for_non_existing_wallet() -> str:
        non_existing_wallet_id = Wallet.objects.count() + 1
        url = reverse('core:wallet-detail', args=(non_existing_wallet_id,))

        return url

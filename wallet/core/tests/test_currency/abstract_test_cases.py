from abc import ABC

from django.urls import reverse

from tools.test import AuthenticatedAPITestCase
from core.models import Currency
from core.tests.factories import CurrencyFactory


class AbstractCurrencyTestCase(AuthenticatedAPITestCase, ABC):

    def _assert_currency_fields_in_container(self, container) -> None:
        self.assertEqual(len(container), 4)
        self.assertIn('id', container)
        self.assertIn('name', container)
        self.assertIn('code', container)
        self.assertIn('symbol', container)


class AbstractCurrencyListTestCase(AbstractCurrencyTestCase, ABC):
    url = reverse('core:currency-list')

    def setUp(self) -> None:
        super(AbstractCurrencyListTestCase, self).setUp()
        self.existing_currency = CurrencyFactory()

    def _assert_common_response_data(self, response_data) -> None:
        self.assertIn('next', response_data)
        self.assertIn('previous', response_data)
        self._assert_currency_fields_in_container(response_data.get('results')[0])


class AbstractCurrencyDetailTestCase(AbstractCurrencyTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractCurrencyDetailTestCase, self).setUp()
        self.existing_currency = CurrencyFactory()
        self.url = reverse('core:currency-detail', args=(self.existing_currency.id,))

    def _assert_common_response_data(self, response_data) -> None:
        self._assert_currency_fields_in_container(response_data)

    @staticmethod
    def _generate_url_for_non_existing_currency() -> str:
        non_existing_currency_id = Currency.objects.count() + 1
        url = reverse('core:currency-detail', args=(non_existing_currency_id,))

        return url

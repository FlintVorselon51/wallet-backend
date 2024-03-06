from rest_framework import status

from core.tests.test_currency.abstract_test_cases import AbstractCurrencyListTestCase


class GetCurrencyListTestCase(AbstractCurrencyListTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_common_response_data(response.data)

from rest_framework import status

from core.tests.test_currency.abstract_test_cases import AbstractCurrencyDetailTestCase


class GetCurrencyDetailTestCase(AbstractCurrencyDetailTestCase):

    def test_get_existing_currency(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_common_response_data(response.data)

    def test_get_non_existing_currency(self):
        response = self.client.get(self._generate_url_for_non_existing_currency())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

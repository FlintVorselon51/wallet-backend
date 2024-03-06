from rest_framework import status

from core.tests.test_currency.abstract_test_cases import AbstractCurrencyDetailTestCase


class PostCurrencyDetailTestCase(AbstractCurrencyDetailTestCase):

    def test_post_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

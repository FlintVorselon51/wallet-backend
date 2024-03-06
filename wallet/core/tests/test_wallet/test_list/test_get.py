from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletListTestCase


class GetWalletListTestCase(AbstractWalletListTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self._assert_wallet_fields_in_container(response.data.get('results')[0])

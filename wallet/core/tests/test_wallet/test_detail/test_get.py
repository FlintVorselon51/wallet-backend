from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletDetailTestCase


class GutWalletDetailTestCase(AbstractWalletDetailTestCase):

    def test_get_user_wallet(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_wallet_fields_in_container(response.data)

    def test_get_another_user_wallet(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existing_wallet(self):
        response = self.client.get(self._generate_url_for_non_existing_wallet())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

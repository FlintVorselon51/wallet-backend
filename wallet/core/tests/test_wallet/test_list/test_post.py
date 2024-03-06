from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletListTestCase


class PostWalletListTestCase(AbstractWalletListTestCase):

    def test_post_wallet_with_non_existing_name(self):
        payload = self._form_wallet_payload()

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._assert_wallet_fields_in_container_without_balance(response.data)

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_wallet_with_existing_name(self):
        payload = self._form_wallet_payload(
            name=self.existing_wallet.name
        )

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_wallet_with_non_existing_currency(self):
        payload = self._form_wallet_payload(
            currency_id=self._get_id_of_non_existing_currency()
        )

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wallet_without_currency(self):
        payload = self._form_wallet_payload(excluded_fields=('currency',))

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wallet_without_name(self):
        payload = self._form_wallet_payload(excluded_fields=('name',))

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletDetailTestCase


class PutWalletDetailTestCase(AbstractWalletDetailTestCase):

    def test_put_wallet(self):
        payload = self._form_wallet_payload()

        for _ in range(2):
            response = self.client.put(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self._assert_wallet_fields_in_container_without_balance(response.data)

    def test_put_wallet_with_existing_name(self):
        wallet = self._create_new_wallet_for_user(self.user)

        payload = self._form_wallet_payload(
            name=wallet.name,
        )

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_put_wallet_with_change_of_currency(self):
        currency = self._create_new_currency()

        payload = self._form_wallet_payload(
            currency=currency
        )

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_another_user_wallet(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_non_existing_wallet(self):
        response = self.client.put(self._generate_url_for_non_existing_wallet())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_wallet_without_currency(self):
        payload = self._form_wallet_payload(excluded_fields=('currency',))

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_wallet_without_name(self):
        payload = self._form_wallet_payload(excluded_fields=('name',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

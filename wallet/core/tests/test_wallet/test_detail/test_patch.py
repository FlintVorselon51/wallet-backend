from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletDetailTestCase


class PatchWalletDetailTestCase(AbstractWalletDetailTestCase):

    def test_patch_wallet(self):
        payload = self._form_wallet_payload()

        for _ in range(2):
            response = self.client.patch(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self._assert_wallet_fields_in_container_without_balance(response.data)

    def test_patch_wallet_with_existing_name(self):
        wallet = self._create_new_wallet_for_user(self.user)

        payload = self._form_wallet_payload(
            name=wallet.name,
        )

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_patch_wallet_with_change_of_currency(self):
        currency = self._create_new_currency()

        payload = self._form_wallet_payload(
            currency=currency
        )

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_patch_another_user_wallet(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_non_existing_wallet(self):
        response = self.client.patch(self._generate_url_for_non_existing_wallet())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wallet_without_currency(self):
        payload = self._form_wallet_payload(excluded_fields=('currency',))

        for _ in range(2):
            response = self.client.patch(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wallet_without_name(self):
        for _ in range(2):
            payload = self._form_wallet_payload(excluded_fields=('name',))
            response = self.client.patch(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

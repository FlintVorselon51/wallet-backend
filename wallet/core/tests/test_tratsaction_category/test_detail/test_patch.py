from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryDetailTestCase


class PatchTransactionCategoryDetailTestCase(AbstractTransactionCategoryDetailTestCase):

    def test_patch_transaction_category(self):
        payload = self._form_transaction_category_payload()

        for _ in range(2):
            response = self.client.patch(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self._assert_transaction_category_fields_in_container(response.data)

    def test_patch_transaction_category_with_existing_name(self):
        transaction_category = self._create_new_transaction_category_for_user(self.user)

        payload = self._form_transaction_category_payload(
            name=transaction_category.name,
        )

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_patch_wallet_with_change_is_expense(self):
        new_is_expense = not self.existing_transaction_category.is_expense

        payload = self._form_transaction_category_payload(
            is_expense=new_is_expense
        )

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_patch_transaction_category_for_another_user(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_non_existing_transaction_category(self):
        response = self.client.patch(self._generate_url_for_non_existing_transaction_category())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_transaction_category_without_name(self):
        payload = self._form_transaction_category_payload(excluded_fields=('name',))

        response = self.client.patch(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_transaction_category_without_is_expense(self):
        payload = self._form_transaction_category_payload(excluded_fields=('is_expense',))

        for _ in range(2):
            response = self.client.patch(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)


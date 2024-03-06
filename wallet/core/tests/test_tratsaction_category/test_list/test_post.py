from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryListTestCase


class PostTransactionCategoryListTestCase(AbstractTransactionCategoryListTestCase):

    def test_post_transaction_category_with_non_existing_name(self):
        payload = self._form_transaction_category_payload()

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._assert_transaction_category_fields_in_container(response.data)

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_transaction_category_with_existing_name(self):
        transaction_category = self._create_new_transaction_category_for_user(self.user)

        payload = self._form_transaction_category_payload(
            name=transaction_category.name
        )

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_transaction_category_without_name(self):
        payload = self._form_transaction_category_payload(excluded_fields=('name',))

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_category_without_is_expense(self):
        payload = self._form_transaction_category_payload(excluded_fields=('is_expense',))

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

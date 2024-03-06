from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryDetailTestCase


class GetTransactionCategoryDetailTestCase(AbstractTransactionCategoryDetailTestCase):

    def test_get_user_transaction_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_transaction_category_fields_in_container(response.data)

    def test_get_another_user_transaction_category(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existing_transaction_category(self):
        response = self.client.get(self._generate_url_for_non_existing_transaction_category())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

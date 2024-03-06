from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryDetailTestCase


class DeleteTransactionCategoryDetailTestCase(AbstractTransactionCategoryDetailTestCase):

    def test_delete_user_transaction_category(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user_transaction_category(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_transaction_category(self):
        response = self.client.delete(self._generate_url_for_non_existing_transaction_category())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

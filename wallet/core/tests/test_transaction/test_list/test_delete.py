from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionListTestCase


class DeleteTransactionListTestCase(AbstractTransactionListTestCase):

    def test_delete_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

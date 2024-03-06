from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryListTestCase


class PutTransactionCategoryListTestCase(AbstractTransactionCategoryListTestCase):

    def test_put_not_allowed(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

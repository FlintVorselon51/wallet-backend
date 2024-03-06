from rest_framework import status

from core.tests.test_tratsaction_category.abstract_test_cases import AbstractTransactionCategoryListTestCase


class GetTransactionCategoryListTestCase(AbstractTransactionCategoryListTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self._assert_transaction_category_fields_in_container(response.data.get('results')[0])

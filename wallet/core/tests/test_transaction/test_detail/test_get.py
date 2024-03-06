from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionDetailTestCase


class GetTransactionDetailTestCase(AbstractTransactionDetailTestCase):

    def test_get_user_transaction(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_transaction_fields_in_container(response.data)

    def test_get_another_user_transaction(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_non_existing_transaction(self):
        response = self.client.get(self._generate_url_for_non_existing_transaction())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

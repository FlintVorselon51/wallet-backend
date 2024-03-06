from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionListTestCase


# noinspection DuplicatedCode
class GetTransactionListTestCase(AbstractTransactionListTestCase):

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self._assert_transaction_fields_in_container(response.data.get('results')[0])

    def test_filter_by_wallet(self):
        new_wallet = self._create_wallet_for_user(self.user)

        self._create_transaction_for_user(self.user, wallet=self.existing_transaction.wallet)
        self._create_transaction_for_user(self.user, wallet=new_wallet)

        self.url += f'?wallet_id={self.existing_transaction.wallet.id}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data.get('results')), 2)

    def test_filter_by_category(self):
        new_category = self._create_category_for_user(self.user)

        self._create_transaction_for_user(self.user, category=self.existing_transaction.category)
        self._create_transaction_for_user(self.user, category=new_category)

        self.url += f'?category_id={self.existing_transaction.category.id}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data.get('results')), 2)

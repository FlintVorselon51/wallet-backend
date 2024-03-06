from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionDetailTestCase
from core.models import Wallet


# noinspection DuplicatedCode
class DeleteTransactionDetailTestCase(AbstractTransactionDetailTestCase):

    def test_delete_user_transaction(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_balance_increases_after_delete(self):
        category = self._create_category_for_user(self.user, is_expense=True)
        transaction = self._create_transaction_for_user(
            user=self.user,
            category=category,
            is_expense=True
        )

        wallet_id = transaction.wallet.id
        balance_before_delete = Wallet.objects.get(id=wallet_id).balance

        response = self.client.delete(self._generate_url_for_transaction(transaction))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        balance_after_delete = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_delete + transaction.value, balance_after_delete)

    def test_balance_decreases_after_delete(self):
        category = self._create_category_for_user(self.user, is_expense=False)
        transaction = self._create_transaction_for_user(
            user=self.user,
            category=category,
            is_expense=False
        )

        wallet_id = transaction.wallet.id
        balance_before_delete = Wallet.objects.get(id=wallet_id).balance

        response = self.client.delete(self._generate_url_for_transaction(transaction))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        balance_after_delete = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_delete - transaction.value, balance_after_delete)

    def test_delete_another_user_transaction(self):
        self.client.force_authenticate(self.another_user)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_transaction(self):
        response = self.client.delete(self._generate_url_for_non_existing_transaction())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

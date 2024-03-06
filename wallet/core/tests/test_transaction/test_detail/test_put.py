from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionDetailTestCase
from core.models import Wallet


# noinspection DuplicatedCode
class PutTransactionListTestCase(AbstractTransactionDetailTestCase):

    def test_put_transaction(self):
        payload = self._form_transaction_payload_for_user(self.user)

        for _ in range(2):
            response = self.client.put(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self._assert_transaction_fields_in_container(response.data)

    def test_balance_increases_after_put_without_changing_wallet(self):
        payload = self._form_transaction_payload_for_user(
            self.user,
            is_expense=False
        )

        transaction_value = payload.get('value')
        wallet_id = payload.get('wallet')
        balance_before_put = Wallet.objects.get(id=wallet_id).balance

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_transaction_fields_in_container(response.data)

        balance_after_put = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_put + transaction_value, balance_after_put)

    def test_balance_decreases_after_put_without_changing_wallet(self):
        payload = self._form_transaction_payload_for_user(
            self.user,
            is_expense=True
        )

        transaction_value = payload.get('value')
        wallet_id = payload.get('wallet')
        balance_before_put = Wallet.objects.get(id=wallet_id).balance

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_transaction_fields_in_container(response.data)

        balance_after_put = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_put - transaction_value, balance_after_put)

    def test_balances_change_after_put_with_changing_wallet(self):
        new_wallet = self._create_wallet_for_user(self.user)
        category = self._create_category_for_user(self.user, is_expense=True)
        transaction = self._create_transaction_for_user(
            user=self.user,
            category=category,
            is_expense=True
        )

        payload = self._form_transaction_payload_for_user(
            self.user,
            wallet=new_wallet,
            is_expense=False
        )

        old_transaction_value = transaction.value
        new_transaction_value = payload.get('value')
        old_wallet_id = transaction.wallet.id

        old_wallet_balance_before_put = Wallet.objects.get(id=old_wallet_id).balance
        new_wallet_balance_before_put = Wallet.objects.get(id=new_wallet.id).balance

        response = self.client.put(self._generate_url_for_transaction(transaction), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_transaction_fields_in_container(response.data)

        old_wallet_balance_after_put = Wallet.objects.get(id=old_wallet_id).balance
        new_wallet_balance_after_put = Wallet.objects.get(id=new_wallet.id).balance

        self.assertEqual(old_wallet_balance_before_put + old_transaction_value, old_wallet_balance_after_put)
        self.assertEqual(new_wallet_balance_before_put + new_transaction_value, new_wallet_balance_after_put)

    def test_put_transaction_with_opposite_is_expense(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['is_expense'] = not payload['is_expense']

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_transaction_with_wallet_of_another_user(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['wallet'] = self._create_wallet_for_user(self.another_user).id

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_transaction_with_category_of_another_user(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['category'] = self._create_category_for_user(self.another_user).id

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_transaction_with_non_existing_wallet(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['wallet'] = self._get_id_of_non_existing_wallet()

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_transaction_with_non_existing_category(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['category'] = self._get_id_of_non_existing_category()

        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_transaction_without_wallet(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('wallet',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_transaction_without_category(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('category',))

        for _ in range(2):
            response = self.client.put(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_transaction_without_executed_at(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('executed_at',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_transaction_without_value(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('value',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_transaction_without_title(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('title',))

        for _ in range(2):
            response = self.client.put(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_transaction_without_description(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('description',))

        for _ in range(2):
            response = self.client.put(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_transaction_without_is_expense_transaction(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('is_expense',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

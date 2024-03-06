from rest_framework import status

from core.tests.test_transaction.abstract_test_cases import AbstractTransactionListTestCase
from core.models import Wallet


# noinspection DuplicatedCode
class PostTransactionListTestCase(AbstractTransactionListTestCase):

    def test_post_transaction(self):
        payload = self._form_transaction_payload_for_user(self.user)

        for _ in range(2):
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self._assert_transaction_fields_in_container(response.data)

    def test_balance_increases_after_post(self):
        payload = self._form_transaction_payload_for_user(
            self.user,
            is_expense=False
        )

        transaction_value = payload.get('value')
        wallet_id = payload.get('wallet')
        balance_before_post = Wallet.objects.get(id=wallet_id).balance

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._assert_transaction_fields_in_container(response.data)

        balance_after_post = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_post + transaction_value, balance_after_post)

    def test_balance_decreases_after_post(self):
        payload = self._form_transaction_payload_for_user(
            self.user,
            is_expense=True
        )

        transaction_value = payload.get('value')
        wallet_id = payload.get('wallet')
        balance_before_post = Wallet.objects.get(id=wallet_id).balance

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._assert_transaction_fields_in_container(response.data)

        balance_after_post = Wallet.objects.get(id=wallet_id).balance

        self.assertEqual(balance_before_post - transaction_value, balance_after_post)

    def test_post_transaction_with_opposite_is_expense(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['is_expense'] = not payload['is_expense']

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_transaction_with_wallet_of_another_user(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['wallet'] = self._create_wallet_for_user(self.another_user).id

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_transaction_with_category_of_another_user(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['category'] = self._create_category_for_user(self.another_user).id

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_transaction_with_non_existing_wallet(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['wallet'] = self._get_id_of_non_existing_wallet()

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_with_non_existing_category(self):
        payload = self._form_transaction_payload_for_user(self.user)
        payload['category'] = self._get_id_of_non_existing_category()

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_without_wallet(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('wallet',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_without_category(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('category',))

        for _ in range(2):
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_transaction_without_executed_at(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('executed_at',))

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_without_value(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('value',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_transaction_without_title(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('title',))

        for _ in range(2):
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_transaction_without_description(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('description',))

        for _ in range(2):
            response = self.client.post(self.url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_transaction_without_is_expense_transaction(self):
        payload = self._form_transaction_payload_for_user(self.user, excluded_fields=('is_expense',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

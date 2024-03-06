from rest_framework import status

from core.tests.test_wallet.abstract_test_cases import AbstractWalletListTestCase


class PatchWalletListTestCase(AbstractWalletListTestCase):

    def test_patch_not_allowed(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

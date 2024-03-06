from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Currency, Wallet, TransactionCategory, Transaction


User = get_user_model()


class FillDBTestCase(TestCase):
    models = (User, Currency, Wallet, TransactionCategory, Transaction)

    def test_fill_db(self):
        call_command('fill_db', '--noinput')
        for model in self.models:
            self.assertNotEqual(model.objects.count(), 0)

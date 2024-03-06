import factory
from faker import Faker
from pytz import timezone

from core import models

fake = Faker()


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Currency

    name = factory.Faker('currency_name')
    code = factory.Faker('currency_code')
    symbol = factory.Faker('currency_symbol')


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Wallet

    currency = factory.SubFactory(CurrencyFactory)
    name = factory.Sequence(lambda _: fake.unique.word())
    balance = 0.00


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TransactionCategory

    name = factory.Sequence(lambda _: fake.unique.word())
    is_expense = factory.Faker('boolean')


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction

    wallet = factory.SubFactory(WalletFactory, creator=factory.SelfAttribute('..creator'),)
    category = factory.SubFactory(TransactionCategoryFactory, creator=factory.SelfAttribute('..creator'),)
    executed_at = factory.Sequence(lambda _: fake.unique.date_time(tzinfo=timezone(fake.timezone())))
    value = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)
    title = factory.Faker('word')
    description = factory.Faker('text')
    is_expense = factory.LazyAttribute(lambda transaction: transaction.category.is_expense)

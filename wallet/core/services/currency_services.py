from core.models import Currency


class CurrencyQuerySetService:

    @staticmethod
    def execute():
        return Currency.objects.all()

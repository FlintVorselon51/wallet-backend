from rest_framework import viewsets, mixins
from rest_framework.viewsets import ModelViewSet

from core.serializers import (
    CurrencySerializer,
    WalletSerializer,
    WalletSerializerWithoutBalance,
    TransactionCategorySerializer,
    TransactionSerializer
)

from core.services import (
    CurrencyQuerySetService,
    WalletQuerySetService,
    WalletCreateService,
    WalletUpdateService,
    TransactionCategoryQuerySetService,
    TransactionCategoryCreateService,
    TransactionCategoryUpdateService,
    TransactionQuerySetService,
    TransactionCreateService,
    TransactionUpdateService,
    TransactionDestroyService
)


class CurrencyViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = CurrencyQuerySetService().execute()
    serializer_class = CurrencySerializer


class WalletViewSet(ModelViewSet):

    def get_queryset(self):
        return WalletQuerySetService(self.request.user).execute()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return WalletSerializerWithoutBalance
        return WalletSerializer

    def perform_create(self, serializer):
        WalletCreateService(self.request.user, serializer).execute()

    def perform_update(self, serializer):
        WalletUpdateService(self.request.user, serializer).execute()


class TransactionCategoryViewSet(ModelViewSet):
    serializer_class = TransactionCategorySerializer

    def get_queryset(self):
        return TransactionCategoryQuerySetService(self.request.user).execute()

    def perform_create(self, serializer):
        TransactionCategoryCreateService(self.request.user, serializer).execute()

    def perform_update(self, serializer):
        TransactionCategoryUpdateService(self.request.user, serializer).execute()


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return TransactionQuerySetService(self.request.user, self.request.query_params).execute()

    def perform_create(self, serializer):
        TransactionCreateService(self.request.user, serializer).execute()

    def perform_update(self, serializer):
        TransactionUpdateService(self.request.user, serializer).execute()

    def perform_destroy(self, instance):
        TransactionDestroyService(self.request.user, instance).execute()

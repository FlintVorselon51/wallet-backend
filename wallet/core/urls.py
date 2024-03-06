from rest_framework.routers import SimpleRouter

from core.views import CurrencyViewSet, WalletViewSet, TransactionCategoryViewSet, TransactionViewSet

app_name = 'core'

router = SimpleRouter()
router.register('currencies', CurrencyViewSet, basename='currency')
router.register('wallets', WalletViewSet, basename='wallet')
router.register('transaction-categories', TransactionCategoryViewSet, basename='transaction-category')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version='0.1.0',
        description="API for the Wallet project",
    ),
    public=True,
    authentication_classes=tuple(),
    permission_classes=(permissions.AllowAny, )
)

# noinspection PyUnresolvedReferences
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls', namespace='auth')),
    path('api/', include('core.urls', namespace='core')),
    path('docs/', schema_view.with_ui('swagger')),
]

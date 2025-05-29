"""
URL configuration for qr_payment_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# qr_payment_service/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings          # Settings importieren
from django.conf.urls.static import static  # static-Funktion importieren
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Einrichtung der Swagger/OpenAPI-Dokumentation
schema_view = get_schema_view(
    openapi.Info(
        title="QR Payment API",
        default_version='v1',
        description="API für den QR-Code Payment Service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),                  # Admin-Oberfläche
    path('api/', include('payments.urls')),            # QR-Endpunkte
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT-Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT-Refresh
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),   # JSON-Schema
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # Swagger-UI
]

# Medien-Dateien in der Entwicklung bereitstellen
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


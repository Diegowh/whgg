from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from summoner_profile.apis.backend.views import test_api_client

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-api-client/', test_api_client, name='test_api_client'),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

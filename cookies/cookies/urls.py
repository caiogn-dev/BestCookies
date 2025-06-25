from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import MeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.static import serve
from loja.views import MediaListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loja.urls')),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('imagens/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('imagens/<path:path>', MediaListView.as_view()),
    path('imagens/', MediaListView.as_view(), {'path': ''}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path, include
from django.contrib import admin
from .views_api import add_to_favorites_ajax, get_route
from rest_framework.routers import DefaultRouter
from .views_api import LocationViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # This generates routes automatically
    path('api/', include(router.urls)),
    path('route/', get_route, name='get_route'),
    # path('ajax/add-favorite/', add_to_favorites_ajax, name='add_to_favorites_ajax'),
]

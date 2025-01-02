# location_app/urls_api.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import LocationViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),  # This generates routes automatically
]

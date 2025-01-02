# location_app/views_api.py
from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Favorite
from .serializers import FavoriteSerializer



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    # Custom endpoint: /api/favorites/my_favorites/
    @action(detail=False, methods=['get'], url_path='my_favorites')
    def my_favorites(self, request):
        # Filter by the current user
        user_favorites = Favorite.objects.filter(user=request.user)
        serializer = self.get_serializer(user_favorites, many=True)
        return Response(serializer.data)

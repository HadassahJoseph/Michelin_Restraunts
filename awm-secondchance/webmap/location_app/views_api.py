# location_app/views_api.py

from rest_framework import viewsets, status
from .models import Location, Favorite
from .serializers import LocationSerializer, FavoriteSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the favorites
        for the currently authenticated user.
        """
        return Favorite.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my_favorites')
    def my_favorites(self, request):
        user_favorites = self.get_queryset()
        serializer = self.get_serializer(user_favorites, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add_favorite')
    def add_favorite(self, request):
        location_id = request.data.get('location_id')
        if not location_id:
            return Response(
                {"success": False, "message": "No location_id provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            location = Location.objects.get(id=location_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, location=location)
            if created:
                logger.info(f"Favorite added: {request.user} - {location}")
                return Response(
                    {"success": True, "message": "Favorite added!"},
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.info(f"Favorite already exists: {request.user} - {location}")
                return Response(
                    {"success": False, "message": "Already in favorites."},
                    status=status.HTTP_200_OK
                )
        except Location.DoesNotExist:
            logger.error(f"Location not found: {location_id}")
            return Response(
                {"success": False, "message": "Location not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Unexpected error adding favorite")
            return Response(
                {"success": False, "message": "An error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST']) # Changed to AllowAny to allow unauthenticated access
def get_route(request):
    """
    Receives start and end coordinates and returns the route using OpenRouteService in GeoJSON format.
    """
    start = request.data.get('start')  # Expected format: "lon,lat"
    end = request.data.get('end')      # Expected format: "lon,lat"
    mode = request.data.get('mode', 'driving-car')  # Default to driving

    if not start or not end:
        return Response({"success": False, "message": "Start and end coordinates are required."}, status=400)

    try:
        start_lon, start_lat = map(float, start.split(','))
        end_lon, end_lat = map(float, end.split(','))
    except ValueError:
        return Response({"success": False, "message": "Invalid coordinate format."}, status=400)

    # Validate coordinate ranges
    if not (-180 <= start_lon <= 180 and -90 <= start_lat <= 90):
        return Response({"success": False, "message": "Invalid start coordinates."}, status=400)
    if not (-180 <= end_lon <= 180 and -90 <= end_lat <= 90):
        return Response({"success": False, "message": "Invalid end coordinates."}, status=400)

    # Validate transportation mode
    valid_modes = ['driving-car', 'cycling-regular', 'foot-walking']
    if mode not in valid_modes:
        return Response({"success": False, "message": "Invalid transportation mode."}, status=400)

    ORS_API_KEY = settings.OPENROUTESERVICE_API_KEY  # Ensure this is set in settings.py

    url = f'https://api.openrouteservice.org/v2/directions/{mode}'
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [
            [start_lon, start_lat],  # [lon, lat]
            [end_lon, end_lat]
        ],
        "geometry_format": "geojson"  # Request GeoJSON geometry
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        logger.debug(f"ORS API Response: {response.json()}")
        return Response(response.json(), status=response.status_code)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return Response({"success": False, "message": f"HTTP error: {http_err}"},
                        status=response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouteService API request failed: {e}")
        return Response({"success": False, "message": str(e)}, status=500)

@login_required
@require_POST
def add_to_favorites_ajax(request):
    location_id = request.POST.get('location_id')
    if not location_id:
        logger.error("No location_id provided")
        return JsonResponse({"success": False, "message": "No location_id provided."}, status=400)
    
    try:
        location = Location.objects.get(id=location_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, location=location)
        if created:
            logger.info(f"Favorite added: {request.user} - {location}")
            return JsonResponse({"success": True, "message": "Favorite added!"})
        else:
            logger.info(f"Favorite already exists: {request.user} - {location}")
            return JsonResponse({"success": False, "message": "Already in favorites."})
    except Location.DoesNotExist:
        logger.error(f"Location not found: {location_id}")
        return JsonResponse({"success": False, "message": "Location not found."}, status=404)
    except Exception as e:
        logger.exception("Unexpected error adding favorite via AJAX")
        return JsonResponse({"success": False, "message": "An error occurred."}, status=500)

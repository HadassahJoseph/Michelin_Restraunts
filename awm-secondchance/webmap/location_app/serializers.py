# location_app/serializers.py
from rest_framework import serializers
from .models import Location, Favorite

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  # or list specific fields: ['id', 'name', 'city', ...]

class FavoriteSerializer(serializers.ModelSerializer):
    # you can nest location data or just return location_id
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'location', 'created_at']
        # or specify whichever fields you want in the API

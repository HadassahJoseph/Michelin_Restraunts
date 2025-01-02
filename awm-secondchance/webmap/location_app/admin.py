# location_app/admin.py

from django.contrib import admin
from .models import Location, Favorite

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'cuisine', 'star_level')
    search_fields = ('name', 'city', 'region', 'cuisine')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'location__name')
    list_filter = ('created_at',)


from django.shortcuts import render
from location_app.models import Location

def location_map(request):
    # Retrieve all locations from the database
    locations = Location.objects.all()
    
    # Prepare data for the template in JSON format
    locations_json = []
    for location in locations:
        # Assuming 'latitude' and 'longitude' are stored as separate fields
        locations_json.append({
            'name': location.name,
            'latitude': location.geom.y,  # Latitude (from PointField)
            'longitude': location.geom.x,  # Longitude (from PointField)
            'city': location.city,
            'region': location.region,
            'cuisine': location.cuisine,
            'star_level': location.star_level,
            'year': location.year,
            # 'notes': location.notes,  # You can include other attributes as needed
        })

    # Pass the data to the template
    return render(request, 'base.html', {'locations': locations_json})

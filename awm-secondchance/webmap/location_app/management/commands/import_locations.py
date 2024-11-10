import csv
from django.core.management.base import BaseCommand
from location_app.models import Location  # Adjust according to your actual model import
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point  # To handle geospatial data

class Command(BaseCommand):
    help = 'Imports locations from a CSV file'

    def handle(self, *args, **kwargs):
        # Specify the path to your cleaned CSV file
        with open(r'C:\Users\C21382216\OneDrive - Technological University Dublin\Desktop\awm-secondchance\CSV\cleaned_michelin_restaurants.csv', mode='r') as file:
            reader = csv.DictReader(file)  # Use DictReader to handle CSV headers as field names

            for row in reader:
                # Extract the relevant columns from the CSV
                name = row['name']
                year = row['year']
                latitude = row['latitude']
                longitude = row['longitude']
                city = row['city']
                region = row['region']
                cuisine = row['cuisine']
                url = row['url']
                star_level = row['star_level']
                
                # Apply default values if necessary
                if not latitude or not longitude:
                    latitude = 0.0  # default value for missing latitude
                    longitude = 0.0  # default value for missing longitude
                
                if not year:
                    year = 2000  # default value for missing year
                
                # If any other fields are null/empty, set default values
                if not name:
                    name = "Unknown"
                if not city:
                    city = "Unknown"
                if not region:
                    region = "Unknown"
                if not cuisine:
                    cuisine = "Unknown"
                if not url:
                    url = "Unknown"
                if not star_level:
                    star_level = "1"  # Assuming the lowest star level is 1 if missing

                # Check if the location already exists to avoid duplicates
                if not Location.objects.filter(name=name, city=city).exists():
                    try:
                        # Create the location instance
                        location_instance = Location(
                            name=name,
                            year=year,
                            city=city,
                            region=region,
                            cuisine=cuisine,
                            url=url,
                            star_level=star_level,
                            geom=Point(float(longitude), float(latitude))  # Create a Point object for geospatial data
                        )
                        location_instance.save()
                        self.stdout.write(f'Successfully imported: {name}')
                    except IntegrityError as e:
                        self.stderr.write(f'Error importing {name}: {e}')
                else:
                    self.stdout.write(f'Skipping duplicate: {name} at {city}')

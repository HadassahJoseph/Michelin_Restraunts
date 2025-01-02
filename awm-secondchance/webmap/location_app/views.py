from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from location_app.models import Location
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse


# def location_map(request):
#     # Retrieve all locations from the database
#     locations = Location.objects.all()
def manifest(request):
    manifest_data = {
        "name": "Michelin Restaurants",
        "short_name": "Michelin",
        "description": "Discover Michelin-starred restaurants with ease.",
        "theme_color": "#1d3247",
        "background_color": "#ffffff",
        "display": "standalone",
        "start_url": "/",
        "id": "/", 
        "icons": [
            # {
            #     "src": "/static/images/icons/icon1.png",
            #     "sizes": "192x192",
            #     "type": "image/png"
            # },
            {
                "src": "/static/images/icons/icon2.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],

        "screenshots": [
            {
                "src": "static/images/screenshots/screenshot1.png", 
                "sizes": "1280x720",
                "type": "image/png",
                "form_factor": "narrow"
            },    
            {
                "src": "static/images/screenshots/screenshot1.png", 
                "sizes": "1280x720",
                "type": "image/png",
                "form_factor": "wide"
            }         
        ],
    }
    response = JsonResponse(manifest_data)
    return response 


@login_required
def location_map(request):
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

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('location_app:signup')  # Use namespaced name

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  # Log in the user
            messages.success(request, "Signup successful!")
            return redirect('location_app:location_map')  # Use namespaced name
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('location_app:signup')  # Use namespaced name

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('location_app:location_map')  # Use the namespaced URL name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('location_app:login')  # Use the namespaced URL name

    return render(request, 'login.html')


def profile_view(request):
    # The currently logged-in user is available through request.user
    context = {
        'user': request.user,
    }
    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('location_app:login')
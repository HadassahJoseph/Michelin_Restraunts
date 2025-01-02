from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from location_app.models import Location, Favorite
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


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
            'id': location.id,
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
    # Favorites for the logged-in user
    user_favorites = Favorite.objects.filter(user=request.user).select_related('location')

    context = {
        'user': request.user,
        'favorites': user_favorites,
    }
    return render(request, 'profile.html', context)


# @login_required
# def add_to_favorites(request, location_id):
#     # Get the location by ID or return 404 if not found
#     location = get_object_or_404(Location, pk=location_id)

#     # Check if already favorited
#     existing_favorite = Favorite.objects.filter(user=request.user, location=location).first()
#     if not existing_favorite:
#         # Create a new Favorite record
#         Favorite.objects.create(user=request.user, location=location)
    
#     # Redirect back to the same page or wherever you want
#     return redirect('location_app:location_map') 
#     # or possibly redirect to the same page you came from


@login_required
@require_POST  # only allow POST
def add_to_favorites_ajax(request):
    location_id = request.POST.get('location_id')
    if not location_id:
        return HttpResponseBadRequest("No location_id provided")

    # Get or create the favorite
    try:
        location = Location.objects.get(id=location_id)
        Favorite.objects.get_or_create(user=request.user, location=location)
        return JsonResponse({"success": True, "message": "Favorite added!"})
    except Location.DoesNotExist:
        return JsonResponse({"success": False, "message": "Location not found."})


@login_required
def remove_from_favorites(request, location_id):
    try:
        favorite = Favorite.objects.get(user=request.user, location_id=location_id)
        favorite.delete()
        messages.success(request, "Removed from favorites.")
    except Favorite.DoesNotExist:
        messages.warning(request, "That location is not in your favorites.")
    return redirect('location_app:profile')



def logout_view(request):
    logout(request)
    return redirect('location_app:login')
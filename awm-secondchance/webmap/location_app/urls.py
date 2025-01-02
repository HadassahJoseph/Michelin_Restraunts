from django.urls import path
from . import views

app_name = 'location_app'  # Declare the app name for namespacing

urlpatterns = [
    # path('webmap/', views.map_view, name='webmap'),
    # path('location_map/', views.location_map, name='location_map'),
    path('',views.location_map,name='location_map'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('manifest.json', views.manifest, name='manifest'),
    path('add-favorite/<int:location_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_favorite/<int:location_id>/', views.remove_from_favorites, name='remove_favorite'),
]


  
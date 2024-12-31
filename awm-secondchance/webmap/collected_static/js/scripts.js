// Initialize the map with a default center (just in case the geolocation fails)
var map = L.map('map').setView([47.0, 13.0], 6);  // Default center for Austria

// Add the OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Try to get the user's location
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        // Get user's latitude and longitude
        var userLat = position.coords.latitude;
        var userLon = position.coords.longitude;

        // Center the map on the user's location
        map.setView([userLat, userLon], 13);  // Set zoom level to 13 for better detail

        // Add a marker for the user's location
        L.marker([userLat, userLon])
            .addTo(map)
            .bindPopup("You are here");
    });
} else {
    alert("Geolocation is not supported by this browser.");
}

// Loop through the locations and add markers to the map
{% for location in locations %}
    var lat = {{ location.latitude }};
    var lon = {{ location.longitude }};
    var name = "{{ location.name }}";
    var year = "{{ location.year }}";
    var city = "{{ location.city }}";
    var region = "{{ location.region }}";
    var cuisine = "{{ location.cuisine }}";
    var star_level = "{{ location.star_level }}";

    // Add a marker for each location
    L.marker([lat, lon])
        .addTo(map)
        .bindPopup("<b>" + name + "</b><br>Year: " + year + "<br>City: " + city + "<br>Region: " + region + "<br>Cuisine: " + cuisine + "<br>Star Level: " + star_level);
{% endfor %}

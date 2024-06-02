import folium
import csv
from firebase_mod.firebase_helper import FirebaseHelper
from firebase_mod.firebase_config import firebaseConfig, service_account_path
from firebase_admin import credentials, storage, db

class mapPlotter:
    def __init__(self, coordinates):
        self.m = folium.Map(location=[0, 0], zoom_start=2)
        self.location_name = "location"
        self.location_idx = 1
        self.new_location = ""
        self.coordinates = coordinates

    def render_map(self):

        for place in self.coordinates:
            folium.Marker(
                location=[place["lat"], place["lon"]],
                popup=place["name"],
            ).add_to(self.m)

            # Calculate center of the coordinates
        latitudes = [place["lat"] for place in self.coordinates]
        longitudes = [place["lon"] for place in self.coordinates]
        center_lat = sum(latitudes) / len(latitudes)
        center_lon = sum(longitudes) / len(longitudes)

        self.m.location = [center_lat, center_lon]
        self.m.fit_bounds([[min(latitudes), min(longitudes)], [max(latitudes), max(longitudes)]])
        self.m.zoom_control = False

        # Save the map to an HTML file
        self.m.save(r"C:\Users\USER\source\repos\GPS\templates\map_with_coordinates.html")
        return self.coordinates

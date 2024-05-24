import folium
import csv

# Create a map centered around a specific point (latitude, longitude)
# Example coordinates: latitude 0, longitude 0 (equator and prime meridian intersection)
m = folium.Map(location=[0, 0], zoom_start=2)
file_path = 'coordinates.csv'
location_name = "location"
location_idx = 1
new_location = ""

coordinates = []

with open(file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)

    # Optionally, get the header
    headers = next(csv_reader, None)

    # Read each row of the CSV file
    for row in csv_reader:
        if row[1] != "":
            new_location = location_name + str(location_idx)
            new_coordinates = {"name": new_location, "lat": float(row[1]), "lon": float(row[2])}
            coordinates.append(new_coordinates)
            location_idx += 1

for x in coordinates:
    print(x)

# Add markers to the map
for place in coordinates:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=place["name"],
    ).add_to(m)

# Save the map to an HTML file
m.save("map_with_coordinates.html")

# To display the map in a Jupyter Notebook, you can use the following
# Display the map in the notebook (only works in Jupyter environment)
#m

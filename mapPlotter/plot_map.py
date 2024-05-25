import folium
import csv

class mapPlotter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.m = folium.Map(location=[0, 0], zoom_start=2)
        self.location_name = "location"
        self.location_idx = 1
        self.new_location = ""
        self.coordinates = []

    def read_csv(self):
        with open(self.filepath, mode='r', newline='') as file:
            csv_reader = csv.reader(file)

            # Optionally, get the header
            headers = next(csv_reader, None)

            # Read each row of the CSV file
            for row in csv_reader:
                if row[1] != "":
                    new_location = self.location_name + str(self.location_idx)
                    date_time = row[0].split()
                    new_coordinates = {"date": date_time[0], "time": date_time[1], "name": new_location, "lat": float(row[1]), "lon": float(row[2]), "detected": int(row[3]), "harvested": int (row[4])}
                    self.coordinates.append(new_coordinates)
                    self.location_idx += 1

        # Add markers to the map
        for place in self.coordinates:
            folium.Marker(
                location=[place["lat"], place["lon"]],
                popup=place["name"],
            ).add_to(self.m)

        # Save the map to an HTML file
        self.m.save(r"C:\Users\USER\source\repos\GPS\templates\map_with_coordinates.html")
        return self.coordinates


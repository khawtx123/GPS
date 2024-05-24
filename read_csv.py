import csv

file_path = 'coordinates.csv'
location_name = "location"
location_idx = 1
new_location = ""

coordinates = []

# Open and read the CSV file
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

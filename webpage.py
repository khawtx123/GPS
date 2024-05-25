from flask import Flask, render_template
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from firebase_mod.firebase_helper import FirebaseHelper
from firebase_mod.firebase_config import firebaseConfig, service_account_path
from mapPlotter.plot_map import mapPlotter
import folium
import csv
import subprocess

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map_with_coordinates')
def map_with_coordinates():
    return render_template('map_with_coordinates.html')

@app.route('/detection_page')
def detection_page():
    image_url = firebase_helper.fetch_image("images/day_1/location_1/palm_oil_1.jpg")
    print(image_url)
    return render_template('detection_page.html', image_url=image_url)

@app.route('/harvesting_report')
def harvesting_report():
    data = {
        "Name": "John",
        "Age": 30,
        "City": "New York"
    }

    # Generate HTML table from dictionary
    html_table = dict_to_html_table(data)
    with open('templates/harvesting_report.html', 'w') as file:
        file.write(html_table)
    # Render HTML template with the generated table
    return render_template('harvesting_report.html', table=html_table)


@app.route('/next')
def next():
    return render_template('next.html')


def upload_data(coordinates):
    for coordinate in coordinates:
        day = coordinate['date'].replace("/", "")
        example_data = {
            "timestamp" : coordinate['time'],
            "latitude": coordinate['lat'],
            "longitude": coordinate['lon'],
            "palm oils detected": coordinate['detected'],
            "palm oils harvested": coordinate['harvested']
        }
        location = coordinate['name']
        word_to_split_by = "location"
        split_strings = location.split(word_to_split_by)
        if int(split_strings[1])<10:
            split_strings[1] = "0" + split_strings[1]
        coordinate['name'] = "location" + split_strings[1]

        example_location = day + "/" + coordinate['name']
        # Call upload_data function
        firebase_helper.upload_data(example_data, example_location)


def dict_to_html_table(data):
    # Start building the HTML table
    html = "<table border='1'>\n"
    keys = ["date", "time", "location", "latitude", "longitude", "palm oils detected", "palm oils harvested"]
    # Add table header
    html += "<tr>"
    for key in keys:
        html += f"<th>{key}</th>"
    html += "</tr>\n"

    # Add table data
    html += "<tr>"
    for value in data.values():
        html += f"<td>{value}</td>"
    html += "</tr>\n"

    # Close the table
    html += "</table>"

    return html


if __name__ == '__main__':
    location = mapPlotter("mapPlotter/coordinates.csv")
    coordinates = location.read_csv()
    firebase_helper = FirebaseHelper(firebaseConfig, service_account_path)

    upload_data(coordinates)
    firebase_helper.fetch_data()

    app.run(debug=True)

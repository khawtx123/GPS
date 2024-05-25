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

@app.route('/next')
def next():
    return render_template('next.html')



if __name__ == '__main__':
    location = mapPlotter("mapPlotter/coordinates.csv")
    location.read_csv()
    # Create an instance of FirebaseHelper
    firebase_helper = FirebaseHelper(firebaseConfig, service_account_path)

    # Example usage
    firebase_helper.upload_image(r'C:\Users\USER\source\repos\GPS\detected_pics\segmentation_test.jpg',
                                 'images/day_1/location_1/palm_oil_1.jpg')

    # Example data to upload
    example_data = {
        "longitude": 100.23,
        "latitude": 30.456,
        "palm oils detected": 3
    }

    # Example location to upload data
    example_location = "day_1/location_1"

    # Call upload_data function
    firebase_helper.upload_data(example_data, example_location)

    # Fetch data
    data = firebase_helper.fetch_data(example_location)
    print(data['latitude'])

    app.run(debug=True)

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from firebase_mod.firebase_helper import FirebaseHelper
from firebase_mod.firebase_config import firebaseConfig, service_account_path
from mapPlotter.plot_map import mapPlotter
from collections import OrderedDict
import glob
import os
from jinja2 import Environment, FileSystemLoader

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
    return render_template('detection_page.html')

@app.route('/harvesting_report')
def harvesting_report():
    html_table = dict_to_html_table()
    with open('templates/harvesting_report.html', 'w') as file:
        file.write(html_table)
    # Render HTML template with the generated table
    return render_template('harvesting_report.html', table=html_table)

@app.route('/robot_location')
def robot_location_page():
    data = firebase_helper.get_last_entry()
    image_dir = firebase_helper.list_jpg_files("robot_location")
    for img in image_dir: image_url = firebase_helper.fetch_image(img)
    return render_template('robot_location.html', data = data, image_url=image_url)

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


def upload_images():
    directory = "detected_pics"
    entries = os.listdir(directory)

    # Filter the entries to include only directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]

    for folder in folders:
        subfolder = os.path.join(directory, folder)
        entries = os.listdir(subfolder)
        JPEG_folders = [entry for entry in entries if os.path.isdir(subfolder)]

        for dir in JPEG_folders:
            target = os.path.join(subfolder, dir)
            jpeg_files = glob.glob(target + "/*.jpg")
            for file in jpeg_files:
                uploaded_file_path = file.replace("\\", "/")
                firebase_helper.upload_image(file, uploaded_file_path)


def upload_robot_images():
    directory = "robot_location"
    jpeg_files = glob.glob(directory + "/*.jpg")
    for file in jpeg_files:
        uploaded_file_path = file.replace("\\", "/")
        firebase_helper.upload_image(file, uploaded_file_path)


def dict_to_html_table():
    html = "<p> Harvesting Report</p>\n"
    for key, value in coordinates.items():
        # Start building the HTML table
        html+= "<div>"
        html += f"<p> {key}</p>\n"
        html += "<table border='1'>\n"
        keys = ["location", "latitude", "longitude", "palm oils detected", "palm oils harvested", "time"]
        # Add table header
        html += "<tr>"
        for key in keys:
            html += f"<th>{key}</th>"
        html += "</tr>"
        # html += f"<td>{key}</td>"

        html += "<tr>"
        for location, data in value.items():
            html += "<tr>"
            html += f"<td>{location}</td>"
            for detail, data in data.items():
                html += f"<td>{data}</td>"
            html += "</tr>\n"
        html += "</tr>\n"

        # Close the table
        html += "</table>\n"
        html += "</div>"

    return html


def detection_page_content(keys1, data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/detection_page_template.html')
    html_content = template.render(keys1=keys1, data=data)
    return html_content


# Save HTML content to a file
def save_detection_page_html(html_content):
    with open('templates/detection_page.html', 'w') as html_file:
        html_file.write(html_content)

def fetch_image_urls(path):
    urls = []
    jpg_files = firebase_helper.list_jpg_files(path)
    for file in jpg_files:
        urls.append(firebase_helper.fetch_image(file))
    return urls


@app.route('/fetch_image_url', methods=['POST'])
def get_image_url():
    data = request.json
    image_path = data['path']
    if image_path:
        image_urls = fetch_image_urls(image_path)
        print(image_urls)
        return jsonify({'image_url': image_urls})
    return jsonify({'error': 'Image path not provided'}), 400

if __name__ == '__main__':
    location = mapPlotter("mapPlotter/coordinates.csv")
    coordinates = location.read_csv()
    firebase_helper = FirebaseHelper(firebaseConfig, service_account_path)
    print("Welcome to HarvestMate")
    upload_data(coordinates)
    coordinates = firebase_helper.fetch_data()

    top_level_keys = list(coordinates.keys())
    html_content = detection_page_content(top_level_keys, coordinates)
    save_detection_page_html(html_content)

    # upload_images()
    upload_robot_images()
    app.run(debug=True)

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from firebase_mod.firebase_helper import FirebaseHelper
from firebase_mod.firebase_config import firebaseConfig, service_account_path
from mapPlotter.plot_map import mapPlotter
from collections import OrderedDict
import glob
import os
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    image_urls = fetch_image_urls("css")
    print(image_urls)
    return render_template('index.html', harvestmate=image_urls[0], img1 = image_urls[1], img2 = image_urls[2], img3 = image_urls[3])

@app.route('/map_with_coordinates')
def map_with_coordinates():
    location = mapPlotter("mapPlotter/coordinates.csv")
    coordinates = location.read_csv()
    return render_template('map_with_coordinates.html')

@app.route('/detection_page')
def detection_page():
    coordinates = firebase_helper.fetch_data()
    top_level_keys = list(coordinates.keys())
    html_content = detection_page_content(top_level_keys, coordinates)
    save_detection_page_html(html_content)
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


def generate_3d_plot(x, y, z, filename, color='b', marker ='o', title = 'Palm Oils Detected'):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, c=color, marker=marker)

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Palm Oils')
    ax.set_title(title)
    for i in range(len(x)):
        latitude = str(x[i]).split(".")
        longitude = str(y[i]).split(".")
        ax.text(x[i], y[i], z[i], f'(.{latitude[1][:3]}, .{longitude[1][:3]}, {z[i]})', fontsize=8, color='black')
    # Save the figure as an image
    directory = os.path.join(filename.split("/")[0], filename.split("/")[1].split(".")[0])
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(filename)

def generate_2d_plot(x,y, filename, color='b', marker ='o', linestyle ='-', title = 'Palm Oils Detected'):
    plt.figure(figsize=(8, 6))
    plt.plot(x, marker=marker, linestyle=linestyle, color=color)  # Plot with blue color, circles as markers, and solid lines
    plt.plot(y, marker='x', linestyle=linestyle,color='r')  # Plot with blue color, circles as markers, and solid lines
    plt.title('Detected vs Harvested')
    plt.grid(True)  # Add grid lines
    plt.savefig(filename)  # Save the plot to a file
    plt.close()  # Close the plot to free memory

def dict_to_html_table():
    coordinates = firebase_helper.fetch_data()
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Harvesting Report</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap">
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/styles.css') }}">
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                max-width: 600px;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            p {
                font-weight: bold;
            }
            img {
                max-width: 70%;
                height: auto;
            }   
            h1 {text-align: center};
        </style>
        
    </head>
    <body>
    <div class="header">
          <h2>Harvesting Report</h2>
    </div>

    """

    for key, value in coordinates.items():
        # Start building the HTML table
        date = key
        html += "<div class=""inline-container-harvesting-report"">\n"
        key = key[:2] + "/" + key[2] + "/" + key[3:len(key)]
        html += f"<p> {key}</p>\n"
        html += "<table border='1'>\n"
        keys = ["location", "latitude", "longitude", "palm oils detected", "palm oils harvested", "time"]
        # Add table header
        html += "<tr>"
        for key in keys:
            html += f"<th>{key}</th>"
        html += "</tr>"

        html += "<tr>"
        latitude = []
        longitude = []
        palm_oils_detected = []
        palm_oils_harvested = []
        for location, data in value.items():
            html += "<tr>"
            html += f"<td>{location}</td>"
            latitude.append(data['latitude'])
            longitude.append(data['longitude'])
            palm_oils_detected.append(data['palm oils detected'])
            palm_oils_harvested.append(data['palm oils harvested'])
            for detail, data in data.items():
                html += f"<td>{data}</td>"
            html += "</tr>\n"

        detected_harvested_graph = "graphs/" + date + "/" + "detected_vs_harvested.jpg"
        palm_oils_detected_graph = "graphs/" + date + "/" + "palm oils detected.jpg"
        palm_oils_harvested_graph = "graphs/" + date + "/" + "palm oils harvested.jpg"

        generate_2d_plot(palm_oils_detected, palm_oils_harvested, detected_harvested_graph)
        generate_3d_plot(latitude, longitude, palm_oils_detected, palm_oils_detected_graph)
        generate_3d_plot(latitude, longitude, palm_oils_harvested, palm_oils_harvested_graph, color='r', title = 'Palm Oil Harvested')

        firebase_helper.upload_image(detected_harvested_graph, detected_harvested_graph)
        firebase_helper.upload_image(palm_oils_detected_graph, palm_oils_detected_graph)
        firebase_helper.upload_image(palm_oils_harvested_graph, palm_oils_harvested_graph)
        # Close the table
        html += "</table>\n"

        detected = firebase_helper.fetch_image(palm_oils_detected_graph)
        harvested = firebase_helper.fetch_image(palm_oils_harvested_graph)
        detected_harvested = firebase_helper.fetch_image(detected_harvested_graph)

        detected_string =  f"<img src="f"{detected}"" >"
        harvested_string = f"<img src="f"{harvested}"" >"
        detected_harvested_string = f"<img src="f"{detected_harvested}"" >"

        html += detected_harvested_string
        html += detected_string
        html += harvested_string
        html += "</div>\n"
    html += """

    
    < / body >
    < / html >
    """
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

    firebase_helper = FirebaseHelper(firebaseConfig, service_account_path)
    print("Welcome to HarvestMate")
    # upload_data(coordinates)


    # upload_images()
    upload_robot_images()
    app.run(debug=True)

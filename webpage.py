from flask import Flask, render_template
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader

import subprocess

app = Flask(__name__)
CORS(app)


def run_python_script():
    # Replace 'script.py' with the name of your Python script file
    script_path = 'plot_map.py'

    try:
        # Run the Python script using subprocess
        subprocess.run(['python', script_path], check=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")


@app.route('/')
def home():
    run_python_script()
    return render_template('index.html')

@app.route('/map_with_coordinates')
def map_with_coordinates():
    return render_template('map_with_coordinates.html')

if __name__ == '__main__':
    app.run(debug=True)

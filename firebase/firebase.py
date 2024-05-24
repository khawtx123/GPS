import urllib.request
import json
import firebase_admin
import pyrebase as pyrebase
from firebase_admin import credentials, db
import re

firebaseConfig = {
  'apiKey': "AIzaSyAdZ-a5GLJqi0p-Dp3Ho4UvvMss82Yq10c",
  'authDomain': "rodent-palm-oil-analysis.firebaseapp.com",
  'databaseURL': "https://rodent-palm-oil-analysis-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "rodent-palm-oil-analysis",
  'storageBucket': "rodent-palm-oil-analysis.appspot.com",
  'messagingSenderId': "486061030096",
  'appId': "1:486061030096:web:ff6f3edac0ac550d9ebcd5",
  'measurementId': "G-S4EKEBFS0B",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
realtime_db =firebase.database()
storage = firebase.storage()

cred = credentials.Certificate("rodent-palm-oil-analysis-firebase-adminsdk-wn9th-801e13fdd6.json")
firebase_admin.initialize_app(cred, { 'databaseURL': "https://rodent-palm-oil-analysis-default-rtdb.asia-southeast1.firebasedatabase.app"})

""""""""""""
#Extract data from real time database
ref = db.reference('/')
data_arr = []
rodent_arr = []
# Extract data from a specific location in the database
data = ref.get()

json_data = json.dumps(data, indent=2)
parsed_data = json.loads(json_data)

# Separate arrays for each attribute
bite_marks_array = []
day_array = []
holes_array = []
palm_oils_array = []

# Iterate over the objects and store values in arrays
for obj_key, obj_value in parsed_data.get("rodent palm oils", {}).items():
    bite_marks_array.append(obj_value.get("bite marks", None))
    day_array.append(obj_value.get("day", None))
    holes_array.append(obj_value.get("holes", None))
    palm_oils_array.append(obj_value.get("palm oils", None))

# Print or process the arrays as needed
print("Bite Marks Array:", bite_marks_array)
print("Day Array:", day_array)
print("Holes Array:", holes_array)
print("Palm Oils Array:", palm_oils_array)
print("\n")

#reading file from storage
print("Rodent Holes and bite marks for each palm oil of each day")
for i in range(len(palm_oils_array)):
    cloud_filename = "Images/" + f"day {i+1}" + "/" + "rodent_data.txt"
    url = storage.child(cloud_filename).get_url(None)
    data =urllib.request.urlopen(url).read()
    text = data.decode('utf-8')
    integers = re.findall(r'\b\d+\b', text)
    integers = [int(num) for num in integers]
    rodent_data = []
    for i in range(len(integers)-1):
        tmp = []
        tmp.append(integers[i])
        tmp.append(integers[i+1])
        rodent_data.append(tmp)

    print(rodent_data)
import firebase_admin
import pyrebase
from firebase_admin import credentials, storage
from firebase_mod.firebase_config import firebaseConfig, service_account_path
import os
from datetime import timezone, datetime

class FirebaseHelper:
    def __init__(self, config, service_account_path):
        self.current_time = int(datetime.now(tz=timezone.utc).timestamp())
        # Initialize Pyrebase
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.realtime_db = self.firebase.database()
        self.config = config

        # Initialize Firebase Admin SDK (only if not already initialized)
        if not firebase_admin._apps:
            self.cred = credentials.Certificate(service_account_path)
            self.app = firebase_admin.initialize_app(self.cred, {
                'databaseURL': config['databaseURL'],
                'storageBucket': config['storageBucket']
            })
        else:
            self.app = firebase_admin.get_app()

    def upload_image(self, file_path, destination_blob_name):
        """Uploads a file to the bucket."""
        bucket = storage.bucket(app=self.app)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {destination_blob_name}.")

    def upload_data(self, data, location):
        """Uploads data to the specified location in the Realtime Database."""
        self.realtime_db.child(location).set(data)
        print(f"Data uploaded to location: {location}")

    def fetch_data(self, data_location):
        """Fetches data from the Realtime Database."""
        data = self.realtime_db.child(data_location).get().val()
        print("Data fetched:")
        print(data)
        return data

    def fetch_data(self):
        """Fetches data from the Realtime Database."""
        data = self.realtime_db.child("").get().val()
        print("Data fetched:")
        print(data)
        return data

    def fetch_image(self, data_location):
        """Fetches an image URL from Firebase Storage."""
        bucket = storage.bucket(app=self.app)
        blob = bucket.blob(data_location)
        image_url = blob.generate_signed_url(expiration= self.current_time+ 3600, method='GET')
        print(f"Generated signed URL: {image_url}")
        return image_url


    def download_images(self, image_location):
        """Downloads images from Firebase Storage."""
        bucket = storage.bucket(app=self.app)
        blobs = bucket.list_blobs(prefix=image_location)
        images = []
        for blob in blobs:
            image_path = os.path.join(os.getcwd(), "downloaded_images", os.path.basename(blob.name))
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            blob.download_to_filename(image_path)
            images.append(image_path)
            print(f"Image downloaded: {image_path}")
        return images

firebase_helper = FirebaseHelper(firebaseConfig, service_account_path)
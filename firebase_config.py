import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Load Firebase credentials from environment variable
firebase_cred_json = os.getenv("FIREBASE_CREDENTIALS")

if firebase_cred_json:
    cred_dict = json.loads(firebase_cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    raise ValueError("Firebase credentials not found. Ensure FIREBASE_CREDENTIALS is set.")

# Initialize Firestore database
db = firestore.client()
users_collection = db.collection("users")  # ✅ Add this line

print("✅ Firestore is working! Database connected.")

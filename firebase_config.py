import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# ✅ Use a direct file path instead of an environment variable
FIREBASE_CREDENTIALS_PATH = "serviceAccountKey.json"

if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise ValueError("Firebase credentials file is missing. Please check serviceAccountKey.json.")

# ✅ Load the Firebase credentials
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

# ✅ Initialize Firestore database
db = firestore.client()
users_collection = db.collection("users")  # ✅ Keep this line

print("✅ Firestore is working! Database connected.")

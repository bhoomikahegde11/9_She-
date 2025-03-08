import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import logging

# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Firebase Credentials Path
FIREBASE_CREDENTIALS_PATH = "serviceAccountKey.json"

# 🔹 Check if credentials exist
if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    logging.error("❌ Firebase credentials file is missing. Ensure serviceAccountKey.json exists.")
    raise ValueError("Firebase credentials file is missing. Please check serviceAccountKey.json.")

try:
    # 🔹 Load the Firebase credentials
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)

    # 🔹 Initialize Firebase Admin SDK
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # 🔹 Initialize Firestore database
    db = firestore.client()
    users_collection = db.collection("users")  # ✅ Keep Firestore users collection

    logging.info("✅ Firestore is working! Database connected successfully.")

except Exception as e:
    logging.error(f"❌ Error initializing Firebase: {e}")
    raise ValueError(f"Failed to initialize Firebase: {str(e)}")

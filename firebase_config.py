import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase with your service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()

# Reference to Firestore collection
users_collection = db.collection('users')

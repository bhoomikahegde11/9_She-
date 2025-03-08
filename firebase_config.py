import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore instance
db = firestore.client()

# Test Firestore Write
test_doc_ref = db.collection("test_collection").document("test_document")
test_doc_ref.set({"message": "Hello from Firestore!"})

print("✅ Firestore is working! Data written successfully.")
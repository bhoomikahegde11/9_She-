from flask import Flask, request, jsonify
from firebase_config import db  # Import Firestore
from ussd_handler import process_ussd_request  # Import the USSD logic

app = Flask(__name__)

@app.route("/add_user", methods=["POST"])
def add_user():
    """Stores user details in Firestore."""
    data = request.json
    phone_number = data.get("phone_number")
    name = data.get("name")

    if not phone_number or not name:
        return jsonify({"error": "Missing phone_number or name"}), 400

    user_ref = db.collection("users").document(phone_number)
    user_ref.set({"name": name, "phone_number": phone_number})

    return jsonify({"message": "User added successfully"}), 200

@app.route("/get_user/<phone_number>", methods=["GET"])
def get_user(phone_number):
    """Retrieves user details from Firestore."""
    user_ref = db.collection("users").document(phone_number)
    user = user_ref.get()

    if user.exists:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/ussd", methods=["POST"])
def ussd():
    """Handles incoming USSD requests and interacts with Firestore"""
    
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text", "")

    response_text = process_ussd_request(text, phone_number)

    return response_text, 200  # Return response to the USSD request

if __name__ == "__main__":
    app.run(debug=True)

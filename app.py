from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
from firebase_config import db  # Import Firestore
from ussd_handler import process_ussd_request  # Import the USSD logic

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Allow requests from any origin


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


@app.route("/get_users", methods=["GET"])
def get_users():
    """Fetch all users from Firestore."""
    users_ref = db.collection("users").stream()
    users_list = [{"phone_number": user.id, **user.to_dict()} for user in users_ref]

    return jsonify(users_list), 200

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
    """Handles USSD requests and logs user interactions."""
    if not request.is_json:  # ✅ Ensure request is JSON
        return jsonify({"error": "Invalid Content-Type. Use application/json"}), 415
    
    data = request.get_json()  # ✅ Properly parse JSON
    phone_number = data.get("phone_number")
    user_input = data.get("user_input", "")  # Default empty input

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    response = process_ussd_request(user_input, phone_number)

    return jsonify({"message": response})

@app.route("/get_user_activity/<phone_number>", methods=["GET"])
def get_user_activity(phone_number):
    """Retrieve full activity log of a user."""
    user_ref = db.collection("users").document(phone_number)
    user = user_ref.get()

    if user.exists:
        user_data = user.to_dict()
        return jsonify(user_data.get("activity_log", [])), 200
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)

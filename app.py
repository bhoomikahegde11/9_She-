from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
from firebase_config import db  # ✅ Import Firestore
from ussd_handler import process_ussd_request  # ✅ Import USSD logic
import logging

# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Allow requests from any origin


@app.route("/add_user", methods=["POST"])
def add_user():
    """Stores user details in Firestore."""
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Use application/json"}), 415

    data = request.get_json()
    phone_number = data.get("phone_number")
    name = data.get("name")

    if not phone_number or not name:
        return jsonify({"error": "Missing phone_number or name"}), 400

    user_ref = db.collection("users").document(phone_number)
    user_ref.set({"name": name, "phone_number": phone_number}, merge=True)  # ✅ Prevents overwriting

    logging.info(f"✅ User {phone_number} added successfully")
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
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Use application/json"}), 415
    
    data = request.get_json()
    phone_number = data.get("phone_number")
    user_input = data.get("user_input", "")  # Default empty input

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    response = process_ussd_request(user_input, phone_number)
    logging.info(f"✅ USSD interaction: {phone_number} -> {user_input}")

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


@app.route("/get_popular_menus", methods=["GET"])
def get_popular_menus():
    """Returns the most accessed menus across all users"""
    users_ref = db.collection("users").stream()

    menu_counts = {}
    for user in users_ref:
        user_data = user.to_dict()
        activity_log = user_data.get("activity_log", [])

        for activity in activity_log:
            menu = activity.get("menu_displayed", "Unknown")
            menu_counts[menu] = menu_counts.get(menu, 0) + 1  # Count each menu selection

    # Sort menus by popularity
    sorted_menus = sorted(menu_counts.items(), key=lambda x: x[1], reverse=True)

    logging.info(f"✅ Popular menus fetched successfully")
    return jsonify({"popular_menus": sorted_menus}), 200


if __name__ == "__main__":
    app.run(debug=True)

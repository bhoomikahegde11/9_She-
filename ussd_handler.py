from firebase_config import db  # Import Firestore database
from datetime import datetime  # For timestamps
from google.cloud.firestore import ArrayUnion

def process_ussd_request(user_input, phone_number):
    """Handles USSD requests and logs all interactions in Firestore"""

    user_ref = db.collection("users").document(phone_number)
    user = user_ref.get()

    # If user doesn't exist, create a new entry with an empty activity log
    if not user.exists:
        user_ref.set({"phone_number": phone_number, "activity_log": []})

    # USSD Menu
    menu_options = {
        "": "Welcome to Rural Rise!\n1. Financial Literacy\n2. Govt Aid\n3. UPI Guide\n4. Exit",
        "1": "Financial Literacy Topics:\n1. Saving Money\n2. Budgeting\n3. Digital Banking\n0. Back",
        "1*1": "Saving Money Tips:\n- Save 20% of income\n- Invest in low-risk savings\n0. Back",
        "2": "Govt Aid Programs:\n1. PM Jan Dhan Yojana\n2. Women Entrepreneurship Scheme\n3. Back to Main Menu",
        "3": "UPI Guide:\n- How to set up UPI\n- Secure your transactions\n- List of supported banks\n0. Back",
        "4": "Thank you for using Rural Rise!"
    }

    # Get response based on input
    response = menu_options.get(user_input, "Invalid choice. Please try again.")

    # Log user activity
    activity_data = {
        "timestamp": datetime.utcnow().isoformat(),  # Current UTC time
        "user_input": user_input,
        "menu_displayed": response
    }

    # Update Firestore to append the activity
    user_ref.update({
    "activity_log": ArrayUnion([activity_data])  # ✅ Correct way to append data in Firestore
})


    return response

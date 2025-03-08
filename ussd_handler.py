from firebase_config import users_collection

def process_ussd_request(user_input, phone_number):
    """Handles USSD requests and logs interactions in Firebase"""

    user_ref = users_collection.document(phone_number)
    user = user_ref.get()

    if not user.exists:
        user_ref.set({"phone_number": phone_number, "last_menu_accessed": ""})

    if user_input == "":
        return "Welcome to Rural Rise!\n1. Financial Literacy\n2. Govt Aid\n3. UPI Guide"

    elif user_input == "1":
        user_ref.update({"last_menu_accessed": "Financial Literacy"})
        return "Financial Literacy Topics:\n1. Saving Money\n2. Budgeting\n3. Digital Banking"

    elif user_input == "1*1":
        user_ref.update({"last_menu_accessed": "Saving Money"})
        return "Saving Money Tips:\n- Save 20% of income\n- Invest in low-risk savings"

    elif user_input == "2":
        user_ref.update({"last_menu_accessed": "Government Aid"})
        return "Govt Aid Programs:\n1. PM Jan Dhan Yojana\n2. Women Entrepreneurship Scheme"

    else:
        return "Invalid choice. Please try again."

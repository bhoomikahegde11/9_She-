from firebase_config import db  # Import Firestore database

def process_ussd_request(user_input, phone_number):
    """Handles USSD requests and logs interactions in Firestore"""

    user_ref = db.collection("users").document(phone_number)  # ✅ Use db.collection
    user = user_ref.get()

    # If user doesn't exist, create a new entry
    if not user.exists:
        user_ref.set({"phone_number": phone_number, "last_menu_accessed": "Welcome"})

    # Root menu
    if user_input == "":  # First time user dials USSD
        return ("Welcome to Rural Rise!\n"
                "1. Financial Literacy\n"
                "2. Government Aid\n"
                "3. UPI Guide\n"
                "4. Exit")

    # Financial Literacy
    elif user_input == "1":
        user_ref.update({"last_menu_accessed": "Financial Literacy"})
        return ("Financial Literacy Topics:\n"
                "1. Saving Money\n"
                "2. Budgeting\n"
                "3. Digital Banking\n"
                "4. Back to Main Menu")

    elif user_input == "1*1":
        user_ref.update({"last_menu_accessed": "Saving Money"})
        return ("Saving Money Tips:\n"
                "- Save 20% of income\n"
                "- Invest in low-risk savings\n"
                "0. Back")

    elif user_input == "1*2":
        user_ref.update({"last_menu_accessed": "Budgeting"})
        return ("Budgeting Tips:\n"
                "- Track expenses\n"
                "- Use 50-30-20 rule\n"
                "0. Back")

    # Government Aid
    elif user_input == "2":
        user_ref.update({"last_menu_accessed": "Government Aid"})
        return ("Govt Aid Programs:\n"
                "1. PM Jan Dhan Yojana\n"
                "2. Women Entrepreneurship Scheme\n"
                "3. Agri Loan Assistance\n"
                "4. Back to Main Menu")

    # UPI Guide
    elif user_input == "3":
        user_ref.update({"last_menu_accessed": "UPI Guide"})
        return ("UPI Guide:\n"
                "- How to set up UPI\n"
                "- Secure your transactions\n"
                "- List of supported banks\n"
                "0. Back")

    # Navigation Options
    elif user_input == "4" or user_input == "0":
        return "Returning to Main Menu.\n1. Financial Literacy\n2. Govt Aid\n3. UPI Guide\n4. Exit"

    # Exit Option
    elif user_input == "4":
        user_ref.update({"last_menu_accessed": "Exited"})
        return "Thank you for using Rural Rise!"

    else:
        return "Invalid choice. Please try again."

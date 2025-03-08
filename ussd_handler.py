from firebase_config import db  # Import Firestore database
from datetime import datetime  # For timestamps
from google.cloud.firestore import ArrayUnion

def process_ussd_request(user_input, phone_number):
    """Handles USSD requests and logs all interactions in Firestore"""

    try:
        user_ref = db.collection("users").document(phone_number)
        user = user_ref.get()

        # If user doesn't exist, create a new entry with an empty activity log
        if not user.exists:
            user_ref.set({
                "phone_number": phone_number,
                "activity_log": []
            })

        # USSD Menu Options
        menu_options = {
            "": "Welcome to Rural Rise!\n1. Financial Literacy\n2. Govt Aid\n3. SMS Banking\n4. Exit",
            "1": "Financial Literacy Topics:\n1. Mann Deshi Mahila Sahakari Bank\n2. Kudumbashree\n3. Rang De\n4. MAVIM\n5. RGMVP\n6. SERP\n7. Back to Main Menu",
            "1*1": "💰 Mann Deshi Bank: Microfinance for rural women entrepreneurs.\nEligibility: Low-income rural women\n0. Back",
            "1*2": "👩‍👩‍👧 Kudumbashree helps BPL families in Kerala through savings groups.\n0. Back",
            "1*3": "💸 Rang De: Low-interest loans for women’s education & business.\n0. Back",
            "1*4": "📊 MAVIM: Financial inclusion for marginalized women in Maharashtra.\n0. Back",
            "1*5": "👭 RGMVP: SHGs for financial literacy in Uttar Pradesh.\n0. Back",
            "1*6": "🌱 SERP: SHG empowerment & finance access in Andhra Pradesh.\n0. Back",
            "1*7": "Returning to Main Menu.\n1. Financial Literacy\n2. Govt Aid\n3. SMS Banking\n4. Exit",
            "2": "🏛 Government Aid Programs:\n1. Janani Suraksha Yojana (JSY)\n2. MGNREGA\n3. YSR Aasara\n4. National Food Security Act (NFSA)\n5. Bibipur Model\n6. Sambhali Trust\n7. CRHP\n8. Sangham Radio\n9. Back to Main Menu",
            "2*1": "🏥 Janani Suraksha Yojana provides maternity financial assistance.\n\nIn some states, where fewer mothers give birth in hospitals, extra benefits are provided.\n\n📌 Are you from one of these states?\n✅ Assam, Bihar, Chhattisgarh, Jammu & Kashmir, Jharkhand, Madhya Pradesh, Odisha, Rajasthan, Uttar Pradesh, Uttarakhand\n1. Yes\n2. No",
            "2*1*1": "✅ You are eligible for JSY benefits!\n👶 What you get: ₹1,400 for rural mothers (₹1,000 for urban)\n📍 How to apply: Visit your nearest Government Health Center with Aadhar & Mother-Child Card.\n📞 Helpline: 1800-xxx-xxxx\n0. Back",
            "2*1*2": "📌 Are you from a BPL, SC, or ST family?\n1. Yes\n2. No",
            "2*1*2*1": "✅ You are eligible for JSY benefits!\n👶 What you get: ₹700 for rural mothers (₹600 for urban)\n📍 How to apply: Visit your nearest Government Health Center with Aadhar & Mother-Child Card.\n📞 Helpline: 1800-xxx-xxxx\n0. Back",
            "2*1*2*2": "❌ You may not qualify for JSY.\n💡 Try other maternity benefit schemes like *Pradhan Mantri Matru Vandana Yojana (PMMVY)*.\n📞 Contact health authorities for guidance.\n0. Back",
            "3": "📲 SMS Banking Services:\n1. Check Bank Balance\n2. Mini Statement\n3. Send Money\n4. Block ATM Card\n5. Govt Bank Schemes for Women\n6. Back to Main Menu",
            "4": "✅ Thank you for using Rural Rise!"
        }

        # Get response based on input
        response = menu_options.get(user_input, "⚠️ Invalid choice. Please try again.")

        # Log user activity
        activity_data = {
            "timestamp": datetime.utcnow().isoformat(),  # Current UTC time
            "user_input": user_input,
            "menu_displayed": response
        }

        # ✅ Append activity log correctly
        user_ref.update({
            "activity_log": ArrayUnion([activity_data])
        })

        return response

    except Exception as e:
        print(f"🔥 Error processing USSD request: {str(e)}")
        return "⚠️ System error. Please try again later."

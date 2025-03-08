from firebase_config import db  # Import Firestore database
from datetime import datetime  # For timestamps
from google.cloud.firestore import ArrayUnion

def calculate_emi(loan_amount, interest_rate, tenure):
    """Calculates EMI based on loan amount, interest rate & tenure"""
    if interest_rate == 0:
        return round(loan_amount / tenure, 2)  # Simple division if no interest

    monthly_interest = (interest_rate / 100) / 12  # Convert annual interest to monthly
    emi = (loan_amount * monthly_interest * (1 + monthly_interest) * tenure) / ((1 + monthly_interest) * tenure - 1)
    return round(emi, 2)

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

        # Define the menu options here instead of as a separate dictionary
        menu_options = {
            "": "Welcome to Rural Rise!\n1. Advice & Information\n2. EMI Calculator\n3. Budget Planner\n4. Exit",

            # 📌 1️⃣ Advice & Information (Merges Financial Literacy, Govt Aid, SMS Banking)
            "1": "📖 Advice & Information:\n1. Financial Literacy\n2. Government Aid\n3. SMS Banking\n4. Back to Main Menu",

            ## Financial Literacy (1*1)
            "1*1": "📊 Financial Literacy Topics:\n1. Mann Deshi Mahila Sahakari Bank\n2. Kudumbashree\n3. Rang De\n4. MAVIM\n5. RGMVP\n6. SERP\n7. Back",
            "1*1*1": "💰 Mann Deshi Bank: Microfinance for rural women entrepreneurs.\nEligibility: Low-income rural women\n0. Back",
            "1*1*2": "👩‍👩‍👧 Kudumbashree helps BPL families in Kerala through savings groups.\n0. Back",
            "1*1*3": "💸 Rang De: Low-interest loans for women's education & business.\n0. Back",
            "1*1*4": "📊 MAVIM: Financial inclusion for marginalized women in Maharashtra.\n0. Back",
            "1*1*5": "👭 RGMVP: SHGs for financial literacy in Uttar Pradesh.\n0. Back",
            "1*1*6": "🌱 SERP: SHG empowerment & finance access in Andhra Pradesh.\n0. Back",
            "1*1*7": "Returning to Advice & Information Menu.\n1. Financial Literacy\n2. Government Aid\n3. SMS Banking\n4. Back",

            ## Government Aid (1*2)
            "1*2": "🏛 Government Aid Programs:\n1. Janani Suraksha Yojana (JSY)\n2. MGNREGA\n3. YSR Aasara\n4. National Food Security Act (NFSA)\n5. Bibipur Model\n6. Sambhali Trust\n7. CRHP\n8. Sangham Radio\n9. Back",
            "1*2*1": "🏥 Janani Suraksha Yojana provides maternity financial assistance.\n\n📌 Are you from Assam, Bihar, Chhattisgarh, J&K, Jharkhand, MP, Odisha, Rajasthan, UP, Uttarakhand?\n1. Yes\n2. No",
            "1*2*1*1": "✅ Eligible! ₹1,400 for rural mothers (₹1,000 for urban)\n📍 Apply: Nearest Govt Health Center with Aadhar & Mother-Child Card.\n📞 Helpline: 1800-xxx-xxxx\n0. Back",
            "1*2*1*2": "📌 Are you from a BPL, SC, or ST family?\n1. Yes\n2. No",
            "1*2*1*2*1": "✅ Eligible! ₹700 for rural mothers (₹600 for urban)\n📍 Apply: Nearest Govt Health Center.\n📞 Helpline: 1800-xxx-xxxx\n0. Back",
            "1*2*1*2*2": "❌ You may not qualify.\n💡 Try PM Matru Vandana Yojana (PMMVY).\n📞 Contact health authorities.\n0. Back",
            "1*2*9": "Returning to Advice & Information Menu.\n1. Financial Literacy\n2. Government Aid\n3. SMS Banking\n4. Back",

            ## SMS Banking (1*3)
            "1*3": "📲 SMS Banking Services:\n1. Check Bank Balance\n2. Mini Statement\n3. Send Money\n4. Block ATM Card\n5. Govt Bank Schemes for Women\n6. Back",
            "1*3*1": "💰 Check Bank Balance:\n📌 Send SMS 'BAL' to 09223766666\n0. Back",
            "1*3*2": "📜 Mini Statement:\n📌 Send SMS 'MSTMT' to 09223866666\n0. Back",
            "1*3*3": "💸 Send Money:\n📌 SMS 'TRF <Mobile> <Amount> <MPIN>' to 567676\n0. Back",
            "1*3*4": "🛑 Block ATM Card:\n📌 SMS 'BLOCK <Last 4 digits>' to 567676\n0. Back",
            "1*3*5": "🏦 Govt Bank Schemes:\n1. PM Jan Dhan Yojana\n2. Sukanya Samriddhi Yojana\n3. Stand-Up India\n4. Back",
            "1*3*5*1": "💰 PM Jan Dhan: Zero balance savings & insurance.\nApply at any bank.\n0. Back",
            "1*3*5*2": "👧 Sukanya Samriddhi: Savings for girl child.\nApply at post office/bank.\n0. Back",
            "1*3*5*3": "🚀 Stand-Up India: Loans for women entrepreneurs.\nApply at designated banks.\n0. Back",
            "1*3*5*4": "Returning to SMS Banking Menu.\n1. Check Balance\n2. Mini Statement\n3. Send Money\n4. Block ATM Card\n5. Govt Bank Schemes\n6. Back",
            "1*3*6": "Returning to Advice & Information Menu.\n1. Financial Literacy\n2. Government Aid\n3. SMS Banking\n4. Back",
            "1*4": "Returning to Main Menu.\n1. Advice & Information\n2. EMI Calculator\n3. Budget Planner\n4. Exit",

            # 📌 4️⃣ Exit
            "4": "✅ Thank you for using Rural Rise!"
        }

        # Handle specific flows that require calculations or dynamic responses

        # 📌 EMI Calculator Flow
        if user_input == "2":
            return "🏦 EMI Calculator:\nEnter loan amount in ₹:"

        elif user_input.startswith("2*") and len(user_input.split("*")) == 2:  # Loan Amount Input
            loan_amount = int(user_input.split("*")[1])
            user_ref.update({"emi_loan_amount": loan_amount})
            return "📊 Enter annual interest rate (e.g., 7 for 7%):"

        elif user_input.startswith("2*") and len(user_input.split("*")) == 3:  # Interest Rate Input
            parts = user_input.split("*")
            interest_rate = float(parts[2])
            user_ref.update({"emi_interest_rate": interest_rate})
            return "📆 Enter loan tenure in months (e.g., 24 for 2 years):"

        elif user_input.startswith("2*") and len(user_input.split("*")) == 4:  # Tenure Input & EMI Calculation
            parts = user_input.split("*")
            tenure = int(parts[3])

            user_data = user_ref.get().to_dict()
            loan_amount = user_data.get("emi_loan_amount", 0)
            interest_rate = user_data.get("emi_interest_rate", 0)

            emi = calculate_emi(loan_amount, interest_rate, tenure)

            # Log EMI details in Firestore with batch update
            emi_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "tenure": tenure,
                "emi": emi
            }
            user_ref.update({
                "emi_loan_amount": loan_amount,
                "emi_interest_rate": interest_rate,
                "emi_tenure": tenure,
                "emi_calculations": ArrayUnion([emi_data])
            })

            return f"✅ Your estimated EMI is ₹{emi}/month.\n1. Loan Assistance\n2. Exit"

        # 📌 Budget Planner Flow
        elif user_input == "3":
            return "💰 Budget Planner:\nEnter your monthly income in ₹:"

        elif user_input.startswith("3*") and len(user_input.split("*")) == 2:  # Income Input
            income = int(user_input.split("*")[1])
            user_ref.update({"budget_income": income})
            return "📊 Enter your monthly expenses in ₹:"

        elif user_input.startswith("3*") and len(user_input.split("*")) == 3:  # Expenses Input & Calculation
            parts = user_input.split("*")
            expenses = int(parts[2])
            
            user_data = user_ref.get().to_dict()
            income = user_data.get("budget_income", 0)
            
            savings = income - expenses
            
            # Log budget details
            budget_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "income": income,
                "expenses": expenses,
                "savings": savings
            }
            
            user_ref.update({
                "budget_income": income,
                "budget_expenses": expenses,
                "budget_savings": savings,
                "budget_calculations": ArrayUnion([budget_data])
            })
            
            return f"✅ You save ₹{savings}/month!"

        # Get response for static menu options
        response = menu_options.get(user_input, "⚠ Invalid choice. Please try again.")

        # Log user activity
        activity_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "menu_displayed": response
        }

        user_ref.update({
            "activity_log": ArrayUnion([activity_data])
        })

        return response

    except Exception as e:
        print(f"🔥 Error processing USSD request: {str(e)}")
        return "⚠ System error. Please try again later."
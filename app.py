from flask import Flask, request
from ussd_handler import process_ussd_request

app = Flask(__name__)

@app.route("/ussd", methods=["POST"])
def ussd():
    """Receives USSD requests and interacts with Firebase"""
    
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text", "")

    response_text = process_ussd_request(text, phone_number)

    return response_text, 200

if __name__ == "__main__":
    app.run(debug=True)

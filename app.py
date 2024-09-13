"""
app.py

Contents:
1. Configure the Flask application
2. Handle the users login information
3. Generate a verification code with Twilio Verify
4. Handle the verification tokens

The code in this file serves as the backend client to process user authentication to your website.
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

"""
1. Configure the Flask application

The Flask app will also have a secret_key for some level of encryption. Any random string can replace 
"secretkey". This is also required in our project since we need to store the users' account information and 
pass it along to other routes on the site using Flask's session.

Retrieve the environment variables from the .env file, as well as the list of known participants that was 
imported from the settings.py file. 
"""

load_dotenv()
app = Flask(__name__)
app.secret_key = 'secretkey'
app.config.from_object('settings')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID= os.environ.get('VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

KNOWN_PARTICIPANTS = app.config['KNOWN_PARTICIPANTS']

"""
2. Handle the users login information
A POST request is made to allow the participant's username to be stored in the Flask session. If the username is 
in the database, in this case the KNOWN_PARTICIPANTS dictionary, then the username is stored in the current Flask 
session and the verification token is sent to the corresponding phone number. The participant is redirected to 
another route where they will see another form allowing them to submit the verification code.

However, if the user enters an unknown username, then the page will be refreshed with an error message.
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if username in KNOWN_PARTICIPANTS:
            session['username'] = username
            send_verification(username)
            return redirect(url_for('generate_verification_code'))
        error = "User not found. Please try again."
        return render_template('index.html', error = error)
    return render_template('index.html')

"""
3. Generate a verification code with Twilio Verify
The Twilio Client sends a verification token to the phone number associated with the username stored in the current 
Flask session. The specified channel in this case is SMS but it can be sent as a call if you prefer.
"""

def send_verification(username):
    phone = KNOWN_PARTICIPANTS.get(username)
    client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verifications \
        .create(to=phone, channel='sms')

"""
4. Handle the verification tokens
The POST request takes in the Flask session's phone number and the verification_code that the user typed into the 
textbox and calls the Verify API to make sure they entered the one time passcode correctly.

If the passcode was correct, the success page is rendered. Similar to the logic for the login page, if the 
participant enters an incorrect verification code, the page will refresh and show an error message. 

The page will also let the user enter the verification code again.
"""

@app.route('/verifyme', methods=['GET', 'POST'])
def generate_verification_code():
    username = session['username']
    phone = KNOWN_PARTICIPANTS.get(username)
    error = None
    if request.method == 'POST':
        verification_code = request.form['verificationcode']
        if check_verification_token(phone, verification_code):
            return render_template('success.html', username = username)
        else:
            error = "Invalid verification code. Please try again."
            return render_template('verifypage.html', error = error)
    return render_template('verifypage.html', username = username)

def check_verification_token(phone, token):
    check = client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verification_checks \
        .create(to=phone, code=token)    
    return check.status == 'approved'
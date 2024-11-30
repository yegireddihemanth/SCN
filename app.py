import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import re  # For email validation

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['SCN']
collection = db['directApplies']

# Admin email setup (notification email)
admin_email = 'skillcatalystnexus.inst@gmail.com'  # Replace with your admin email

# Function to send confirmation email
def send_confirmation_email(to_email, name):
    from_email = 'hemanthyegireddyad@gmail.com'
    from_password = 'jydx bgqd xjnt udph'  # If using 2FA, use the app-specific password here

    subject = 'Registration Success - Confirm Your Email'
    body = f"Hello {name},\n\nThank you for registering! Please confirm your registration by clicking the link below:\n\n"

    # Create MIME email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debugging output from the SMTP server
        server.starttls()  # Start TLS encryption
        server.login(from_email, from_password)  # Login to your Gmail account
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)  # Send the email
        server.quit()
        print(f"Confirmation email sent to {to_email}")
        return True  # Return True if email sent successfully
    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"SMTP Authentication Error: {auth_error}")
        return False  # Return False if authentication fails
    except smtplib.SMTPException as smtp_error:
        print(f"SMTP Error: {smtp_error}")
        return False  # Return False for other SMTP errors

# Function to send notification email to the admin
def send_admin_notification(name, email, phone, course):
    from_email = 'hemanthyegireddyad@gmail.com'
    from_password = 'jydx bgqd xjnt udph'  # If using 2FA, use the app-specific password here

    subject = 'New User Registration Notification'
    body = f"A new user has registered:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nCourse: {course}\n"

    # Create MIME email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = admin_email  # Send to admin email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debugging output from the SMTP server
        server.starttls()  # Start TLS encryption
        server.login(from_email, from_password)  # Login to your Gmail account
        text = msg.as_string()
        server.sendmail(from_email, admin_email, text)  # Send the notification to the admin
        server.quit()
        print(f"Admin notification sent to {admin_email}")
    except smtplib.SMTPException as e:
        print(f"Error sending admin notification: {e}")

# Function to validate email format using regex
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Home route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to process form data and send email
@app.route('/process', methods=['POST'])
def process_data():
    # Get user data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    course = request.form.get('course')

    # Validate email format
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email address. Please enter a valid email address.'}), 400

    # Capture the user's IP address
    user_ip = request.remote_addr

    # Capture the current timestamp
    current_time = datetime.now()

    # Send confirmation email
    email_sent = send_confirmation_email(email, name)

    if email_sent:
        # If email is sent successfully, store the data in the database
        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'course': course,
            'ip_address': user_ip,
            'timestamp': current_time
        }
        collection.insert_one(data)
        
        # Send admin notification email
        send_admin_notification(name, email, phone, course)

        return jsonify({'message': 'Registration successful, please check your email for confirmation.'})
    else:
        return jsonify({'message': 'There was an error sending the email. Please try again later.'}), 500

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient(
    'mongodb+srv://Hemanth:Yv1FlyNivMIXEGfy@scn.g0yg7.mongodb.net/?retryWrites=true&w=majority&appName=SCN',
    connectTimeoutMS=10000,  # Increased timeout to 10 seconds
    socketTimeoutMS=10000,   # Increased socket timeout to 10 seconds
    tls=True,
    tlsAllowInvalidCertificates=False
)

# Access the database and collection
db = client['SCN']
collection = db['directApplies']

# Function to store data in MongoDB
def store_data_in_mongo(name, email, phone, course, user_ip, current_time):
    data = {
        'name': name,
        'email': email,
        'phone': phone,
        'course': course,
        'ip_address': user_ip,
        'timestamp': current_time
    }
    try:
        collection.insert_one(data)
        print(f"Data inserted: {data}")
        return True
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")
        return False

# Home route to display the form
@app.route('/')
def index():
    return "<h1>Welcome to the Registration Page</h1>"

# Route to process form data and store in MongoDB
@app.route('/process', methods=['POST'])
def process_data():
    # Get user data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    course = request.form.get('course')

    # Capture the user's IP address
    user_ip = request.remote_addr

    # Capture the current timestamp
    current_time = datetime.now()

    # Store data in MongoDB
    if store_data_in_mongo(name, email, phone, course, user_ip, current_time):
        return jsonify({'message': 'Registration successful and data stored.'})
    else:
        return jsonify({'message': 'There was an error storing the data. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

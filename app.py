from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['SCN']
collection = db['directApplies']
app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML file from the templates folder
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    print("Form data:", request.form)
    name = request.form.get('name')
    id_ = request.form.get('id')

    data = {
        'cid' : id_,
        'name' : name
    }
    collection.insert_one(data)

    print(f"Name: {name}, ID: {id_}")
    return f"<h1>Received:</h1><p>Name: {name}</p><p>ID: {id_}</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

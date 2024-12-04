from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import uuid

app = Flask(__name__)

# Connect to MongoDB Atlas (replace connection string below with your own MongoDB Atlas connection string)
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://shanrahan02:Jonesborough2004!@savedtexts.frnzs.mongodb.net/?retryWrites=true&w=majority&appName=savedTexts")
client = MongoClient(MONGO_URI)
db = client['editor']  # Database name
collection = db['savedTexts']  # Collection name

@app.route('/api/saveText', methods=['POST'])
def save_text():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate a unique identifier for the text
    text_id = str(uuid.uuid4())

    # Insert the text into the MongoDB collection
    collection.insert_one({'_id': text_id, 'text': text})

    # Return the generated ID
    return jsonify({'id': text_id}), 200

@app.route('/api/getText/<text_id>', methods=['GET'])
def get_text(text_id):
    # Retrieve text by ID from MongoDB
    text_entry = collection.find_one({'_id': text_id})
    if text_entry is None:
        return jsonify({"error": "Text not found"}), 404

    # Return the retrieved text
    return jsonify({'text': text_entry['text']}), 200

if __name__ == "__main__":
    # Make the application externally visible
    app.run(host="0.0.0.0", port=5008)

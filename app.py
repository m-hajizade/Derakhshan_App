from flask import Flask, request, jsonify, send_file, render_template
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

KINDWISE_API_KEY = 'your_kindwise_api_key_here'  # Replace with your actual API key
KINDWISE_API_URL = 'https://api.kindwise.com/v1/identify'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    result = identify_plant(filepath)
    return jsonify(result)

def identify_plant(image_path):
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        headers = {'Authorization': f'Bearer {KINDWISE_API_KEY}'}
        response = requests.post(KINDWISE_API_URL, headers=headers, files=files)
    
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


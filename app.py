import os
from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configuration: Folder to save images and allowed file types
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max image upload

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve the processed image
@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Image conversion route
@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert image to grayscale using OpenCV
        img = cv2.imread(file_path)
        if img is None:
            return jsonify({'status': 'error', 'error': 'Invalid image format'}), 400
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save the processed image as PNG
        processed_filename = f'bw_{filename.rsplit(".", 1)[0]}.png'
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        cv2.imwrite(processed_path, gray)

        # Return the path to the processed image
        return jsonify({'status': 'success', 'bw_image_url': f'/processed/{processed_filename}'})
    else:
        return jsonify({'status': 'error', 'error': 'File type not allowed'}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

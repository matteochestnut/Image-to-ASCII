# app/routes.py
# This file defines the routes and handles image uploads, processing, and downloads

import os
from flask import Blueprint, render_template, request, send_file, jsonify, send_file
from werkzeug.utils import secure_filename
from app.utils.image_processing import convert_to_ASCII
import io

bp = Blueprint('main', __name__)

# Route to render the main index page
@bp.route('/')
def index():
    """Render the index page."""
    return send_file('../index.html')

# Route to handle the file upload and image processing
@bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and conversion."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        image_bytes = file.read()

        # Convert the image using the image processing function
        processed_image = convert_to_ASCII(image_bytes)

        # Create an in-memory file and return the processed image as a response
        img_io = io.BytesIO()
        processed_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=False)
    
    except Exception as e:
        # Handle errors and return a JSON response
        return jsonify({'error': str(e)}), 500

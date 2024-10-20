import os
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app.utils.image_processing import convert_to_black_and_white

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def configure_routes(app):
    """Configure the routes for the Flask app."""
    
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

            # Convert the image using utility function
            processed_filename = convert_to_black_and_white(file_path, filename, app.config['PROCESSED_FOLDER'])

            # Return the path to the processed image
            return jsonify({'status': 'success', 'bw_image_url': f'/processed/{processed_filename}'})
        else:
            return jsonify({'status': 'error', 'error': 'File type not allowed'}), 400

    @app.route('/processed/<filename>')
    def processed_file(filename):
        """Serve the processed image."""
        return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

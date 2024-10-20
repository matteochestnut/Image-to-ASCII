from flask import Flask
from app.routes import configure_routes

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['PROCESSED_FOLDER'] = 'processed'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max image upload
    
    # Initialize routes
    configure_routes(app)

    return app

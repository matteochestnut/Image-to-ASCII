# app/__init__.py
# Initializes the Flask app and registers routes

from flask import Flask

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    
    # Set up caching to optimize performance
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Register the routes
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

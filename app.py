# app.py
# This file instantiates the Flask app

from app import create_app

# Initialize the app
app = create_app()

if __name__ == "__main__":
    # Run the app locally
    app.run(debug=True)

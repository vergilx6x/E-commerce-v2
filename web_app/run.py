from web_app.app import create_app
import os

# Create the app instance
app = create_app()

# Set the secret key using environment variables or fallback
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5002, debug=True)

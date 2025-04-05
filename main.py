# Import the create_app function from the website module
from website import app, create_app
from waitress import serve

# Call the create_app function to initialize the Flask application
wsig_app = app

# If the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    create_app()
    serve(wsgi_app, host='0.0.0.0', url_prefix="/login")

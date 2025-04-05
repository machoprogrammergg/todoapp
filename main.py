# Import the create_app function from the website module
from website import create_app
from waitress import serve

# Call the create_app function to initialize the Flask application


# If the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    serve(create_app())

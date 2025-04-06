from waitress import serve
from website import create_app

# Call the create_app function to initialize the Flask application


# If the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    create_app()
    #serve(create_app(), host='0.0.0.0', port=8080)
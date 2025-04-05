# Import the create_app function from the website module
from website import create_app

# Call the create_app function to initialize the Flask application
app = create_app()

# If the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    app.run()

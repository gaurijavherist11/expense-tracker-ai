import google.generativeai as palm

# Configure the API key
palm.configure(api_key="AIzaSyA8woctpGdHKqDJB7kudFZ38caYQX9QUgU")

# List models
try:
    models = palm.list_models()
    print("Available models:")
    for model in models:
        print(model)  # Print model details
except Exception as e:
    print(f"An error occurred: {e}")

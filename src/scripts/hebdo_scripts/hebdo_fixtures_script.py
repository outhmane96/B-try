import requests
import json
import os

# Define the main function that fetches data from the API and saves it
def fetch_and_save_data(endpoint, querystring):
    """
    Fetch data from the specified API endpoint with the given query parameters,
    and save the response to a JSON file.
    """
    # Define the base URL and headers
    base_url = "https://api-football-v1.p.rapidapi.com/v3/"
    headers = {
        "x-rapidapi-key": "52aa8d992emsh754cf83efed69a3p176b39jsn0ad1c64373be",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    
    # Construct the full URL
    url = f"{base_url}{endpoint}"

    # Set the file path in the "data" directory
    data_folder = os.path.join(os.path.dirname(__file__), '../../data')  # Relative path to 'data' folder
    os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(data_folder, "hebdo_pl_fixtures.json")

    # Check if the file exists and load existing data
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        data = []  # Initialize an empty list if the file doesn't exist

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        # Append the new data entry to the list
        data.append({
            "endpoint": endpoint,
            "query": querystring,
            "response": response.json()
        })
        
        # Write the updated data back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Response from '{endpoint}' saved successfully.")
    else:
        print(f"Failed to retrieve data from '{endpoint}': {response.status_code}")

# Example usage of the function

# fixture id man city vs brighton 1208124
# man city team id 50
# haaland player id 1100
# PL id 39
fetch_and_save_data("fixtures", {"league": "39","season": "2024"})

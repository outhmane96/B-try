import requests
import json
import os

# Define the main function that fetches data from the API and saves it
def fetch_and_save_data(endpoint, querystring, output_file):
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

    # Check if the file exists and load existing data
    if os.path.exists(output_file):
        with open(output_file, "r") as file:
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
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Response from '{endpoint}' with query {querystring} saved successfully.")
    else:
        print(f"Failed to retrieve data from '{endpoint}': {response.status_code}")

# Function to process teams and fetch players
def fetch_players_from_teams(teams_json_path, output_file):
    """
    Read team data from a JSON file and fetch player data for each team.
    """
    # Load the teams JSON
    with open(teams_json_path, "r") as file:
        teams_data = json.load(file)
    
    # Iterate over each team in the JSON

    # Iterate over each team in the JSON
    for team_entry in teams_data:
        teams = team_entry["response"]["response"]
        for team in teams:
            team_id = team["team"]["id"]  # Extract team ID
            print(f"Fetching players for Team ID: {team_id}")
            fetch_and_save_data("players/squads", {"team": str(team_id)}, output_file)
            
# Define paths
teams_json_path = "teams.json"  # Path to the teams JSON file
output_file = "players.json"  # Path to save player data


# Fetch players for all teams
fetch_players_from_teams(teams_json_path, output_file)
import requests
import json
import os

def fetch_player_statistics(player_id, season, output_dir):
    """
    Fetch statistics for a player and save to a file.
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    headers = {
        "x-rapidapi-key": "52aa8d992emsh754cf83efed69a3p176b39jsn0ad1c64373be",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    querystring = {"id": str(player_id), "season": season, "league": league}

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        # Define the file path
        file_path = os.path.join(output_dir, f"{player_id}.json")

        # Save response to a file
        with open(file_path, "w") as file:
            json.dump(response.json(), file, indent=4)

        print(f"Player statistics for ID {player_id} saved successfully.")
    else:
        print(f"Failed to fetch data for player ID {player_id}: {response.status_code}")

def parse_players_and_fetch_stats(players_json_path, output_dir, season, limit, start_from_id=None):
    """
    Parse players from the given JSON and fetch their statistics.
    - Saves each player's stats in a separate file.
    - Stops after processing `limit` players or when all players are processed.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the players data
    with open(players_json_path, "r") as file:
        players_data = json.load(file)

    # Initialize variables
    count = 0
    start_processing = start_from_id is None  # Start processing immediately if no start_from_id
    next_player_id = None  # Placeholder for the next player ID

    # Process each player in the JSON
    for index, player in enumerate(players_data):
        player_id = player["id"]

        # Check if we've reached the starting point
        if not start_processing and player_id == start_from_id:
            start_processing = True

        # Skip until the starting point is found
        if not start_processing:
            continue
        
        # Fetch player statistics and save
        fetch_player_statistics(player_id, season, output_dir)

        print(f"Processing player ID: {player_id}")
        count += 1

        # Check if we've hit the limit
        if count >= limit:
            # Set the next player's ID if there are more players
            if index + 1 < len(players_data):
                next_player_id = players_data[index + 1]["id"]
            print(f"Reached limit of {limit} players. Stopping.")
            break

    # Output the next player's ID
    if next_player_id:
        print(f"The next player ID to process is: {next_player_id}")
    else:
        print("No more players left to process.")

    print("Processing completed.")

# Example Usage
players_json_path = "C:\\Users\\outhm\\Documents\\projects\\B-try\\static_data\\players.json"  # Path to your JSON file containing player data
output_dir = r"D:\\b_try\\players"        # Directory to save player statistics
season = "2024"
league = "39"# Specify the season
limit = 30                              # Number of players to process in one run
start_from_id = 18860                    # Start from the beginning, or specify a player ID

parse_players_and_fetch_stats(players_json_path, output_dir, season, limit, start_from_id)

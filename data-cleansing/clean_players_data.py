import os
import json

# Define the path to the players folder
players_folder = r"D:\b_try\players"

def clean_player_folder():
    """
    Remove player files from the folder if they meet the criteria for removal.
    Criteria:
    1. Rating is null.
    2. Appearances are less than 10.
    3. Minutes played are less than 100.
    """
    removed_players = []

    # Iterate through all JSON files in the folder
    for filename in os.listdir(players_folder):
        if filename.endswith(".json"):  # Process only JSON files
            filepath = os.path.join(players_folder, filename)

            try:
                # Open and parse the player's JSON file
                with open(filepath, "r") as file:
                    player_data = json.load(file)

                # Check if the response has valid statistics
                if not player_data.get("response"):
                    continue
                
                player_stats = player_data["response"][0]["statistics"][0]["games"]
                
                # Check the criteria for removal
                if (
                    player_stats["appearences"] == None or player_stats["appearences"] == 0 
                ):
                    # Remove the file and log the player
                    # os.remove(filepath)
                    removed_players.append(player_data["response"][0]["player"]["id"])
                    print(f"Removed player ID: {player_data['response'][0]['player']['id']}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    print(f"Cleanup completed. Removed {len(removed_players)} players.")

# Call the function to clean the player folder
clean_player_folder()

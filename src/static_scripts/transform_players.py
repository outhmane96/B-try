import json

# Path to the input and output JSON files
input_file = "C:\\Users\\outhm\\Documents\\projects\\B-try\\static_data\\players.json"
output_file = "C:\\Users\\outhm\\Documents\\projects\\B-try\\static_data\\simplified_players.json"

# Load the original JSON
with open(input_file, "r") as file:
    players_data = json.load(file)

# Extract players into a simplified structure
simplified_players = []

for team_entry in players_data:
    response = team_entry.get("response", {}).get("response", [])
    for team in response:
        players = team.get("players", [])
        for player in players:
            # Add player data to the simplified list
            simplified_players.append(player)

# Save the simplified players to a new JSON file
with open(output_file, "w") as file:
    json.dump(simplified_players, file, indent=4)

print(f"Simplified player data saved to {output_file}.")

import json
import unicodedata

# Function to normalize names
def normalize_name(name):
    return unicodedata.normalize('NFKC', name)

# Step 1: Normalize names in the problematic JSON file
def normalize_names_in_place(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Normalize names in the JSON data
    for player in data:
        if "name" in player:
            player["name"] = normalize_name(player["name"])
    
    # Overwrite the original file with normalized data
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Normalized names in file: {file_path}")

def main():
    # Define file paths
    problematic_file = 'C:\\Users\\outhm\\Documents\\projects\\B-try\\static_data\\players.json'

    # Normalize the problematic file
    normalize_names_in_place(problematic_file)


# Run the script
if __name__ == "__main__":
    main()

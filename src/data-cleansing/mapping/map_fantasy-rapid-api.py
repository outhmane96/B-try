import json
import unicodedata

# Function to normalize names
def normalize_name(name):
    return unicodedata.normalize('NFKC', name).strip().lower()

# Function to check partial match
def is_partial_match(name, first_name, second_name, web_name):
    normalized_name = normalize_name(name)
    return (
        normalized_name in normalize_name(first_name) or
        normalized_name in normalize_name(second_name) or
        normalized_name in normalize_name(web_name)
    )

# Function to check composed name match
def is_composed_name_match(name, first_name, second_name):
    name_parts = name.split()
    if len(name_parts) == 2:  # Only process composed names with exactly two parts
        first_part = normalize_name(name_parts[0])
        second_part = normalize_name(name_parts[1])
        return first_part in normalize_name(first_name) and second_part in normalize_name(second_name)
    return False

# Step 1: Map players based on improved matching logic
def map_players(file1, file2, output_mapping_file, unmapped_file):
    # Load both files
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)  # JSON with initials
        data2 = json.load(f2)  # JSON with nested player info

    # Extract the elements list from the second file
    data2_elements = data2.get("elements", [])

    # Create a dictionary for exact match mapping
    data2_mapping = {
        (normalize_name(player["second_name"]), player["first_name"][0].lower()): player["id"]
        for player in data2_elements
    }

    # Map IDs from file1
    id_mapping = {}
    unmapped_from_file1 = []
    for player in data1:
        name = player.get("name", "")
        matched = False

        if "." in name:
            # Exact match logic
            name_parts = name.split(".")
            first_initial = name_parts[0].strip().lower() if len(name_parts) > 1 else ""
            second_name = name_parts[-1].strip()
            normalized_key = (normalize_name(second_name), first_initial)

            if normalized_key in data2_mapping:
                id_mapping[player["id"]] = data2_mapping[normalized_key]
                matched = True

        # Check for composed name match
        if not matched and " " in name and "." not in name:
            for player2 in data2_elements:
                if is_composed_name_match(name, player2["first_name"], player2["second_name"]):
                    id_mapping[player["id"]] = player2["id"]
                    matched = True
                    break

        # Fallback to partial matching
        if not matched:
            for player2 in data2_elements:
                if is_partial_match(name, player2["first_name"], player2["second_name"], player2["web_name"]):
                    id_mapping[player["id"]] = player2["id"]
                    matched = True
                    break

        if not matched:
            unmapped_from_file1.append(player["id"])

    # Track unmatched IDs from file2
    mapped_ids_from_file2 = set(id_mapping.values())
    unmapped_from_file2 = [
        player["id"] for player in data2_elements if player["id"] not in mapped_ids_from_file2
    ]

    # Save the results
    with open(output_mapping_file, 'w', encoding='utf-8') as mapped_file:
        json.dump(id_mapping, mapped_file, indent=4, ensure_ascii=False)

    with open(unmapped_file, 'w', encoding='utf-8') as unmapped_file_out:
        json.dump({
            "unmapped_from_file1": unmapped_from_file1,
            "unmapped_from_file2": unmapped_from_file2
        }, unmapped_file_out, indent=4, ensure_ascii=False)

    print(f"ID mapping saved to: {output_mapping_file}")
    print(f"Unmapped IDs saved to: {unmapped_file}")

# Step 2: Execute the process
def main():
    # Define file paths
    file1 = 'C:\\Users\\outhm\\Documents\\projects\\B-try\\static_data\\players.json'  # JSON file with initials in names
    file2 = 'C:\\Users\\outhm\\Documents\\projects\\B-try\\data\\fantasy_data.json'  # JSON file with first_name, second_name, and web_name
    output_mapping_file = 'id_mapping.json'
    unmapped_file = 'unmapped_ids.json'

    # Map players and save the mapping with trace for unmapped IDs
    map_players(file1, file2, output_mapping_file, unmapped_file)

# Run the script
if __name__ == "__main__":
    main()

import json

# Function to check if a player is transferred or loaned
def check_transfer_or_loan(player):
    news = player.get("news", "").lower()
    if "permanent transfer to" in news or "transferred to" in news or "loan" in news or "loaned to" in news:
        return True, news
    return False, None

# Process unmapped players from File 2
def process_unmapped_players(file2, unmapped_file, output_transfers_file):
    # Load File 2 and unmapped players
    with open(file2, 'r', encoding='utf-8') as f2, open(unmapped_file, 'r', encoding='utf-8') as uf:
        data2 = json.load(f2)  # Full player data
        unmapped_data = json.load(uf)  # Unmapped players info

    # Extract elements and unmapped IDs
    data2_elements = data2.get("elements", [])
    unmapped_ids_file2 = set(unmapped_data.get("unmapped_from_file2", []))

    # Track players who are transferred or loaned
    transfer_or_loaned_players = []
    ids_to_remove = []

    for player in data2_elements:
        if player["id"] in unmapped_ids_file2:
            is_transferred, news = check_transfer_or_loan(player)
            if is_transferred:
                transfer_or_loaned_players.append({
                    "id": player["id"],
                    "name": f'{player["first_name"]} {player["second_name"]}',
                    "news": news
                })
                ids_to_remove.append(player["id"])

    # Save transfer/loan results to output file
    with open(output_transfers_file, 'w', encoding='utf-8') as outfile:
        json.dump(transfer_or_loaned_players, outfile, indent=4, ensure_ascii=False)

    # Update only `unmapped_from_file2` in unmapped_ids.json
    remaining_ids_file2 = list(unmapped_ids_file2 - set(ids_to_remove))
    unmapped_data["unmapped_from_file2"] = remaining_ids_file2

    # Save updated unmapped_ids.json
    with open(unmapped_file, 'w', encoding='utf-8') as uf:
        json.dump(unmapped_data, uf, indent=4, ensure_ascii=False)

    print(f"Transfer/Loan information saved to: {output_transfers_file}")
    print(f"Updated unmapped IDs saved to: {unmapped_file}")

# Step 2: Execute the process
def main():
    # Define file paths
    file2 = 'C:\\Users\\outhm\\Documents\\projects\\B-try\\data\\fantasy_data.json'  # JSON file with nested player data
    unmapped_file = 'unmapped_ids.json'  # File containing unmapped IDs
    output_transfers_file = 'transfered_or_loaned_players.json'  # Output file for transfers/loans

    # Process unmapped players for transfers/loans
    process_unmapped_players(file2, unmapped_file, output_transfers_file)

# Run the script
if __name__ == "__main__":
    main()

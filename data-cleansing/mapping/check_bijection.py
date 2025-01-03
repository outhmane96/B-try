import json

def check_bijection(mapping_file):
    with open(mapping_file, 'r', encoding='utf-8') as file:
        id_mapping = json.load(file)

    # Extract keys (IDs from file1) and values (IDs from file2)
    file1_ids = list(id_mapping.keys())
    file2_ids = list(id_mapping.values())

    # Check for duplicates
    duplicate_file1_ids = [id for id in file1_ids if file1_ids.count(id) > 1]
    duplicate_file2_ids = [id for id in file2_ids if file2_ids.count(id) > 1]

    # Ensure mapping is bijective
    is_bijection = not duplicate_file1_ids and not duplicate_file2_ids

    # Print results
    if is_bijection:
        print("The mapping is a bijection (one-to-one).")
    else:
        print("The mapping is NOT a bijection. Details below:")

        if duplicate_file1_ids:
            print(f"Duplicate keys in file1 IDs: {set(duplicate_file1_ids)}")

        if duplicate_file2_ids:
            print(f"Duplicate values in file2 IDs: {set(duplicate_file2_ids)}")

# Main function to execute the script
def main():
    mapping_file = 'C:\\Users\\outhm\\Documents\\projects\\B-try\\data\\mapped_id_fantasy_rapide\\id_mapping.json'  # Path to the mapping file
    check_bijection(mapping_file)

if __name__ == "__main__":
    main()

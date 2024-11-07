import requests

# Replace this with your API key
API_KEY = 'd8b30b876c624d75bb7ddebd25fd7e41'
BASE_URL = 'https://api.football-data.org/v4'

# Set headers for authentication
headers = {
    'X-Auth-Token': API_KEY
}

# Function to get competitions (leagues) data
def get_competitions():
    url = f"{BASE_URL}/competitions"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Returns JSON response if successful
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to get matches for a specific competition (e.g., Premier League)
def get_matches(competition_id):
    url = f"{BASE_URL}/competitions/{competition_id}/matches"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    # Fetch and display competitions
    print("Fetching list of competitions...")
    competitions = get_competitions()
    if competitions:
        print("Available Competitions:")
        for competition in competitions.get("competitions", []):
            print(f"{competition['id']} - {competition['name']}")

    # Example to get matches for a specific competition, e.g., Premier League
    competition_id = 2021  # Premier League competition ID
    print(f"\nFetching matches for competition ID {competition_id}...")
    matches = get_matches(competition_id)
    if matches:
        print("Recent Matches:")
        for match in matches.get("matches", [])[:5]:  # Show only the first 5 matches
            print(f"{match['utcDate']}: {match['homeTeam']['name']} vs {match['awayTeam']['name']} - Status: {match['status']}")

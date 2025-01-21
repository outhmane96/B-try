from btry.api import BaseAPI
from loguru import logger
from typing import List, Dict

class FantasyAPI(BaseAPI):
    def __init__(self):
        url = "https://fantasy.premierleague.com/api"
        super().__init__(base_url=url)

    def get_players(self) -> List[Dict]:
        """
        Fetch all players from the Fantasy Premier League API.

        Returns:
            List[Dict]: List of player details as dictionaries.
        """
        endpoint = "bootstrap-static/"
        logger.info("Calling {} to fetch all players", endpoint)
        response = self._make_request(endpoint=endpoint)
        logger.info("Successfully fetched players data from {}", endpoint)

        players = response.get("elements", [])
        logger.info("Retrieved {} players from the API", len(players))
        return players

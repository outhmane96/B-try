from btry.api import BaseAPI
from btry.utilities import get_var_from_env, END_POINTS
from loguru import logger
from typing import List

class RapidAPI(BaseAPI):
    def __init__(self):
        url = "https://api-football-v1.p.rapidapi.com/v3"
        api_key = get_var_from_env("RAPID_API_KEY")
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
        }
        super().__init__(api_key=api_key, base_url=url , headers=headers)
    
    def get_team_players(self, team_id: int):
        """Fetch data for all players from the API."""
        endpoint = END_POINTS['rapid_api']['team_players']
        params = {
            "team": str(team_id)
        }
        logger.info("Calling {}, with params: {} ", endpoint , params)
        response = self._make_request(endpoint=endpoint, params=params)
        logger.info("Calling {} ended successfully", endpoint , params)
        return response

    def get_teams(self, league_id: int, season: int) -> List[int]:
        """fetch all the team for a certain league 

        Args:
            league_id (int): league id 

        Returns:
            List[int]: List of ids
        """
        endpoint = END_POINTS['rapid_api']['teams']
        params = {
            "league": str(league_id),
            "season": str(season)
        }
        logger.info("Calling {}, with params: {} ", endpoint, params)
        response = self._make_request(endpoint=endpoint, params= params)
        logger.info("Calling {} ended successfully", endpoint)
        return response
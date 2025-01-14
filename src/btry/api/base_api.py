import requests
from abc import ABC
from loguru import logger

class BaseAPI(ABC):
    def __init__(self, base_url: str, api_key: str = None, headers: dict = None): 
        self.base_url = base_url
        self.api_key = api_key
        self.headers = headers
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: dict = None):
        """Make an HTTP GET request to the API."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
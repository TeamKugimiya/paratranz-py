import requests


class ParaTranzAPI:
    def __init__(self, api_headers: dict, api_url: str):
        """
        Base class for ParaTranz API.

        Parameters:
        api_headers (dict): The API headers.
        api_url (str): The base API URL.
        """
        self._api_headers = api_headers
        self._api_url = api_url

        self.session = requests.Session()
        self.session.headers.update(self._api_headers)

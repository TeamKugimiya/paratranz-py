import requests

from loguru import logger
from typing import Optional, Union


class ParaTranzAPI:
    def __init__(self, api_headers: dict, api_url: str):
        """Base class for ParaTranz API.

        Args:
            api_headers (dict):
                The API headers.
            api_url (str):
                The base API URL.
        """
        self._api_headers = api_headers
        self._api_url = api_url

        self.session = requests.Session()
        self.session.headers.update(self._api_headers)

    def _request(
        self, method: str, url: str, return_status: bool = False,
        timeout: int = 10, **kwargs
    ) -> Optional[Union[int, dict, list, str]]:
        """General API request method.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            url (str): API request URL.
            return_status (bool): Whether to return the HTTP status code (default: False). # noqa
            timeout (int): Timeout for the request in seconds (default: 10).
            kwargs: Other `requests` parameters, such as json, data, params, etc.

        Returns:
            - If `return_status=True`, returns the HTTP status code (int).
            - If `return_status=False`, returns the JSON response (dict | list).
            - On failure, returns the response text (str) or None.
        """
        try:
            response = self.session.request(method, url, timeout=timeout, **kwargs) # noqa
            response.raise_for_status()

            if return_status:
                return response.status_code

            try:
                return response.json()
            except ValueError:
                logger.error(f"Invalid JSON response from {url}: {response.text}") # noqa
                return response.text

        except requests.Timeout:
            logger.error(f"Request timed out: {method} {url}")
        except requests.ConnectionError:
            logger.error(f"Failed to connect: {method} {url}")
        except requests.HTTPError as e:
            logger.error(f"HTTP error on: {method} {str(e)}") # noqa
        except requests.RequestException as e:
            logger.error(f"Unexpected error during {method} {url}: {str(e)}")

        return None

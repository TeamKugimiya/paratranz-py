import requests

from loguru import logger
from .base import ParaTranzAPI


class Scores(ParaTranzAPI):
    """
    ParaTranz 成員貢獻 API 類別
    ParaTranz Scores API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_scores(self, project_id: int) -> dict:
        """獲取 ParaTranz 所有成員貢獻資訊 | Get all scores information from ParaTranz.

        Returns:
            dict:
                所有成員貢獻資訊 | All scores information.
        """
        scores_url = f"{self._projects_url}/{project_id}/scores"
        try:
            response = self.session.get(scores_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            logger.error("Request to ParaTranz API timed out.")
        except requests.ConnectionError:
            logger.error("Failed to connect to ParaTranz API.")
        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Unexpected error: {str(e)}")

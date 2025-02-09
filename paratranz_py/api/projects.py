import requests
from loguru import logger

from .base import ParaTranzAPI


class Projects(ParaTranzAPI):
    """
    ParaTranz 專案 API 類別。
    ParaTranz Projects API class.

    目前僅實現 GET 方法的 API (如獲取所有專案資訊、獲取特定專案資訊)。
    仍缺少建立新專案、更新專案、刪除專案等功能。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_projects(self) -> dict | None:
        """
        獲取 ParaTranz 整個網站的所有專案資訊。
        Get all projects information from ParaTranz.

        Returns:
        dict: 所有專案資訊.｜Whole projects information.
        None: 失敗｜Fail.
        """
        try:
            response = self.session.get(self._projects_url, timeout=10)
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

        return None

    def get_project(self, project_id: int) -> dict | None:
        """
        獲取特定 ID 的專案資訊。
        Get the project information by the project ID.

        Parameters:
        project_id (int): 專案 ID｜The project ID

        Returns:
        dict: The project information.
        None: 失敗｜Fail.
        """
        project_url = f"{self._projects_url}/{project_id}"
        try:
            response = self.session.get(project_url, timeout=10)
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

        return None

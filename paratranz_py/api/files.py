import requests

from loguru import logger
from .base import ParaTranzAPI


class Files(ParaTranzAPI):
    """
    ParaTranz 檔案 API 類別。
    ParaTranz Files API class.

    目前僅實現 部分 GET 方法的 API (如獲取特定專案的檔案資訊)。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_files(self, project_id: int) -> dict | None:
        """
        獲取特定 ID 的專案的檔案資訊。
        Get the files information by the project ID.

        Parameters:
        project_id (int): 專案 ID｜The project ID

        Returns:
        dict: The files information.
        None: 失敗｜Fail.
        """
        project_url = f"{self._projects_url}/{project_id}/files"
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

    def delete_file(self, project_id: int, file_id: int):
        try:
            response = self.session.delete(
                f"{self._projects_url}/{project_id}/files/{file_id}",
                timeout=10
            )
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

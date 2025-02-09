import requests

from pathlib import Path
from loguru import logger
from .base import ParaTranzAPI


class Files(ParaTranzAPI):
    """
    ParaTranz 檔案 API 類別。
    ParaTranz Files API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_files(self, project_id: int) -> dict:
        """獲取特定 ID 專案的所有檔案資訊 | Get all files information from a specific project ID. # noqa

        Args:
            project_id (int):
                專案 ID｜The project ID

        Returns:
            dict:
                所有檔案資訊 | All files information
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

    def upload_file(self, project_id: int, file_path: Path, path: str) -> dict: # noqa
        """上傳檔案 | Upload the file.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_path (Path):
                要上傳的檔案路徑 | The file path to upload
            path (str):
                上傳後所在的路徑（不可包含檔案名） | The path to upload to (without the file name) # noqa

        Returns:
            dict:
                上傳後的檔案資訊 | The uploaded file information
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        try:
            response = self.session.post(
                f"{self._projects_url}/{project_id}/files",
                data={"path": path},
                files={"file": file_path.open("rb")},
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

    def get_file(self, project_id: int, file_id: int) -> dict:
        """獲取特定 ID 的檔案資訊 | Get the file information by the file ID.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_id (int):
                檔案 ID | The file ID

        Returns:
            dict:
                The file information.
        """
        file_url = f"{self._projects_url}/{project_id}/files/{file_id}"
        try:
            response = self.session.get(file_url, timeout=10)
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

    def update_file(self, project_id: int, file_path: Path, file_id: int) -> dict: # noqa
        """更新檔案 | Update the file.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_path (Path):
                要更新的檔案路徑 | The file path to update
            file_id (int):
                檔案 ID | The file ID

        Returns:
            dict:
                更新後的檔案資訊 | The updated file information
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        try:
            response = self.session.post(
                f"{self._projects_url}/{project_id}/files/{file_id}",
                files={"file": file_path.open("rb")},
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

    def delete_file(self, project_id: int, file_id: int) -> requests.status_codes: # noqa
        """刪除檔案 | Delete the file.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_id (int):
                檔案 ID | The file ID

        Returns:
            requests.status_codes:
                刪除檔案的狀態碼 | The status code of the file deletion.
        """
        try:
            response = self.session.delete(
                f"{self._projects_url}/{project_id}/files/{file_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.status_code
        except requests.Timeout:
            logger.error("Request to ParaTranz API timed out.")
        except requests.ConnectionError:
            logger.error("Failed to connect to ParaTranz API.")
        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Unexpected error: {str(e)}")

    def get_translation_file(self, project_id: int, file_id: int) -> list:
        """獲取翻譯檔案 | Get the translation file.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_id (int):
                檔案 ID | The file ID

        Returns:
            list:
                翻譯檔案 | The translation
        """
        file_url = f"{self._projects_url}/{project_id}/files/{file_id}/translation" # noqa
        try:
            response = self.session.get(file_url, timeout=10)
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

    def update_translation_file(self, project_id: int, file_path: Path, file_id: int, force: bool = False) -> dict: # noqa
        """更新翻譯檔案 | Update the translation file.

        Args:
            project_id (int):
                專案 ID | The project ID
            file_path (Path):
                要更新的翻譯檔案路徑 | The translation file path to update
            file_id (int):
                檔案 ID | The file ID
            force (bool):
                強制覆蓋現有的翻譯 | Force overwrite the existing translation

        Returns:
            dict:
                更新後的翻譯檔案 | The updated translation file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        try:
            response = self.session.post(
                f"{self._projects_url}/{project_id}/files/{file_id}/translation", # noqa
                data={"force": force},
                files={"file": file_path.open("rb")},
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

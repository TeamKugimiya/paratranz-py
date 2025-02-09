import requests

from loguru import logger
from .base import ParaTranzAPI


class Projects(ParaTranzAPI):
    """
    ParaTranz 專案 API 類別
    ParaTranz Projects API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_projects(self) -> dict | None:
        """獲取 ParaTranz 所有專案資訊 | Get all projects information from ParaTranz.

        Returns:
            dict:
                所有專案資訊 | All projects information.
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

    def create_project(
        self, project_name: str, project_description: str, source_lang: str,
        dest_lang: str, game_name: str, privacy_mode: int, download_mode: int,
        issue_mode: int, review_mode: int, join_mode: int
    ) -> dict:
        """建立新專案 | Create a new project.

        Args:
            project_name (str):
                專案名稱 | The project name
            project_description (str):
                專案描述 | The project description
            source_lang (str):
                原文語言 | The source language
                    en: 英文 | English
                    zh-tw: 繁體中文 | Traditional Chinese
                    zh-cn: 簡體中文 | Simplified Chinese
                    es: 西班牙語 | Spanish
            dest_lang (str):
                目標語言 | The target language
                    en: 英文 | English
                    zh-tw: 繁體中文 | Traditional Chinese
                    zh-cn: 簡體中文 | Simplified Chinese
                    es: 西班牙語 | Spanish
            game_name (str):
                遊戲名稱 | The game name
                    mc: Minecraft
            privacy_mode (int):
                專案隱私 | Privacy mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            download_mode (int):
                下載模式 | Download mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            issue_mode (int):
                討論權限 | Issue mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            review_mode (int):
                校對等級 | Review mode
                    0: 無須校對 | No need to review
                    1: 一次校對 | Review once
                    2: 二次校對 | Review twice
            join_mode (int):
                加入方式 | Join mode
                    0: 任何人都可以直接加入 | Anyone can join directly
                    1: 加入專案需要提交申請 | Join by application
                    2: 加入專案需要完成測試 | Join by test
                    3: 僅管理員可以新增成員 | Only admins can add members
                    4: 加入專案需要輸入口令 | Join by password

        Returns:
            dict:
                新專案資訊 | The new project information.
        """
        project_data = {
            "name": project_name,
            "desc": project_description,
            "source": source_lang,
            "dest": dest_lang,
            "game": game_name,
            "privacy": privacy_mode,
            "download": download_mode,
            "issueMode": issue_mode,
            "reviewMode": review_mode,
            "joinMode": join_mode
        }
        try:
            response = self.session.post(
                self._projects_url, json=project_data, timeout=10
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

    def get_project(self, project_id: int) -> dict | None:
        """獲取特定 ID 的專案資訊 | Get the project information by the project ID.

        Args:
            project_id (int):
                專案 ID | The project ID

        Returns:
            dict:
                The project information.
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

    def update_project(
        self, project_id: int,
        project_name: str, project_description: str,
        game_name: str, privacy_mode: int, download_mode: int,
        issue_mode: int, review_mode: int, join_mode: int
    ) -> dict:
        """更新專案資訊 | Update the project information.

        Args:
            project_id (int):
                專案 ID | The project ID
            project_name (str):
                專案名稱 | The project name
            project_description (str):
                專案描述 | The project description
            game_name (str):
                遊戲名稱 | The game name
                    mc: Minecraft
            privacy_mode (int):
                專案隱私 | Privacy mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            download_mode (int):
                下載模式 | Download mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            issue_mode (int):
                討論權限 | Issue mode
                    0: 公開 | Public
                    1: 內部 | Internal
                    2: 私密 | Private
            review_mode (int):
                校對等級 | Review mode
                    0: 無須校對 | No need to review
                    1: 一次校對 | Review once
                    2: 二次校對 | Review twice
            join_mode (int):
                加入方式 | Join mode
                    0: 任何人都可以直接加入 | Anyone can join directly
                    1: 加入專案需要提交申請 | Join by application
                    2: 加入專案需要完成測試 | Join by test
                    3: 僅管理員可以新增成員 | Only admins can add members
                    4: 加入專案需要輸入口令 | Join by password

        Returns:
            dict:
                更新後的專案資訊 | The updated project information.
        """
        project_data = {
            "name": project_name,
            "desc": project_description,
            "game": game_name,
            "privacy": privacy_mode,
            "download": download_mode,
            "issueMode": issue_mode,
            "reviewMode": review_mode,
            "joinMode": join_mode
        }
        project_url = f"{self._projects_url}/{project_id}"
        try:
            response = self.session.put(
                project_url, json=project_data, timeout=10
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

    def delete_project(self, project_id: int) -> requests.status_codes:
        """刪除專案 | Delete the project.

        Args:
            project_id (int):
                專案 ID | The project ID

        Returns:
            requests.status_codes:
                HTTP 狀態碼 | HTTP status code
        """
        project_url = f"{self._projects_url}/{project_id}"
        try:
            response = self.session.delete(project_url, timeout=10)
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

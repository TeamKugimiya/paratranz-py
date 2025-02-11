from loguru import logger
from .base import ParaTranzAPI


class Members(ParaTranzAPI):
    """
    ParaTranz 成員 API 類別
    ParaTranz Members API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_members(self, project_id: int) -> list:
        """獲取專案成員 | Get project members

        Args:
            project_id (int):
                專案 ID | Project ID

        Returns:
            list:
                專案成員 | Project members
        """
        member_url = f"{self._projects_url}/{project_id}/members"
        return self._request("GET", member_url)

    def add_member(
        self, project_id: int, member_uid: int,
        permission: int, note: str = None
    ) -> dict:
        """獲取專案成員 | Get project member

        Args:
            project_id (int):
                專案 ID | Project ID
            member_uid (int):
                成員 ID | Member UID
            permission (int):
                權限 | Permission
                    1: 翻譯 | Translator
                    2: 校對 | Proofreader
                    3: 管理 | Manager
                    10: 擁有者 | Owner
            note (str):
                備註 | Note

        Returns:
            dict:
                成員資訊 | Member information
        """
        permission_list = [1, 2, 3]
        if permission not in permission_list:
            logger.error(f"Permission should be one of {permission_list}")
            return
        member_url = f"{self._projects_url}/{project_id}/members"
        data = {
            "uid": member_uid,
            "permission": permission,
            "note": note
        }
        return self._request("POST", member_url, json=data)

    def update_member(
        self, project_id: int, member_id: int,
        permission: int, note: str = None
    ) -> dict:
        """更新專案成員 | Update project member

        Args:
            project_id (int):
                專案 ID | Project ID
            member_id (int):
                成員 ID (不是 UID) | Member ID (not UID)
            permission (int):
                權限 | Permission
                    1: 翻譯 | Translator
                    2: 校對 | Proofreader
                    3: 管理 | Manager
                    10: 擁有者 | Owner
            note (str):
                備註 | Note

        Returns:
            dict:
                成員資訊 | Member information
        """
        permission_list = [1, 2, 3]
        if permission not in permission_list:
            logger.error(f"Permission should be one of {permission_list}")
            return
        member_url = f"{self._projects_url}/{project_id}/members/{member_id}"
        data = {
            "permission": permission,
            "note": note
        }
        return self._request("PUT", member_url, json=data)

    def delete_member(self, project_id: int, member_id: int) -> int:
        """刪除專案成員 | Delete project member

        Args:
            project_id (int):
                專案 ID | Project ID
            member_uid (int):
                成員 ID (不是 UID) | Member ID (not UID)

        Returns:
            int:
                狀態碼 | Status code
        """
        member_url = f"{self._projects_url}/{project_id}/members/{member_id}"
        return self._request("DELETE", member_url, return_status=True)

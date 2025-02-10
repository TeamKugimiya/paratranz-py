from loguru import logger
from .base import ParaTranzAPI


class History(ParaTranzAPI):
    """
    ParaTranz 檔案 API 類別
    ParaTranz Files API class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_history(
        self, project_id: int, page: int = 1, page_size: int = 50,
        uid: int = None, tid: int = None, type: str = "text"
    ) -> dict:
        """獲取專案歷史記錄 | Get project history

        Args:
            project_id (int):
                專案 ID | Project ID
            page (int):
                頁碼 | Page number (default: 1)
            page_size (int):
                每頁數量 | Number of items per page (default: 50)
            uid (int):
                使用者 ID | User ID
            tid (int):
                詞條 ID | Term ID
            type (str):
                歷史記錄類型 | History type (default: "text")
                    text: 詞條歷史 | Term history
                    import: 導入歷史 | Import history
                    comment: 評論記錄 | Comment history

        Returns:
            dict:
                帳號歷史記錄 | Account history
        """
        params = {
            "project": project_id,
            "page": page,
            "pageSize": page_size,
            "uid": uid,
            "tid": tid,
            "type": type
        }
        type_list = ["text", "import", "comment"]
        if type and type not in type_list:
            logger.error(f"Invalid history type: {type}.")
            return

        return self._request("GET", f"{self._api_url}/history", params=params)

    def get_file_revisions(
        self, project_id: int, page: int = 1, page_size: int = 50,
        file_id: int = None, type: str = None
    ) -> dict:
        """獲取檔案歷史記錄 | Get file history

        Args:
            project_id (int):
                專案 ID | Project ID
            page (int):
                頁碼 | Page number (default: 1)
            page_size (int):
                每頁數量 | Number of items per page (default: 50)
            file_id (int):
                檔案 ID (若未指定將是獲取全部) | File ID (if not specified, will get all)
            type (str):
                歷史記錄類型 | History type (default: "None")
                    create: 建立歷史 | Create history
                    update: 更新歷史 | Update history
                    import: 匯入歷史 | Import history

        Returns:
            dict:
                檔案歷史記錄 | File history
        """
        history_url = f"{self._projects_url}/{project_id}/files/revisions"
        params = {
            "page": page,
            "pageSize": page_size,
            "file": file_id,
            "type": type
        }
        type_list = ["create", "update", "import"]
        if type and type not in type_list:
            logger.error(f"Invalid history type: {type}.")
            return

        return self._request("GET", history_url, params=params)

    def get_project_term_history(self, project_id: int, term_id: int) -> list:
        """獲取術語歷史 | Get term history

        Args:
            project_id (int):
                專案 ID | Project ID
            term_id (int):
                詞條 ID | Term ID

        Returns:
            list:
                術語歷史 | Term history
        """
        history_url = f"{self._projects_url}/{project_id}/terms/{term_id}/history" # noqa
        return self._request("GET", history_url)

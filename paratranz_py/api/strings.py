from .base import ParaTranzAPI


class Strings(ParaTranzAPI):
    """
    ParaTranz 詞條 API 類別
    ParaTranz Strings API class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._projects_url = f"{self._api_url}/projects"

    def get_strings(
        self,
        project_id: int,
        file_id: int = None,
        stage: int = 0,
        page: int = 1,
        page_size: int = 50,
    ) -> dict:
        """獲取詞條資訊 | Get strings information

        Args:
            project_id (int):
                專案 ID | Project ID
            file_id (int):
                檔案 ID (為 None 將回傳所有詞條) | File ID (if None, return all strings)
            stage (int):
                詞條翻譯狀態 | Strings translation status
                    0: 未翻譯 | Untranslated
                    1: 已翻譯 | Translated
                    2: 有疑問 | Questionable
                    3: 已審核 | Reviewed
                    5: 已二次審核 | Double reviewed
                    9: 已鎖定 | Locked
                    -9: 已隱藏 | Hidden
            page (int):
                頁碼 | Page number (default: 1)
            page_size (int):
                每頁數量 | Number of items per page (default: 50)

        Returns:
            dict:
                詞條資訊 | Strings information
        """
        data = {"file": file_id, "stage": stage, "page": page, "pageSize": page_size}
        strings_url = f"{self._projects_url}/{project_id}/strings"
        return self._request("GET", strings_url, params=data)

    # def create_strings(
    #     self,
    #     key: str,
    #     project_id: int,
    #     original_text: str,
    #     translate_text: str,
    #     file: int,
    #     stage: int = 0,
    #     context: str = None
    # ) -> dict:
    #     """新增詞條 | Create strings

    #     Args:
    #         project_id (int):
    #             專案 ID | Project ID
    #         key (str):
    #             詞條 Key | Strings Key
    #         original_text (str):
    #             原文 | Original text
    #         translate_text (str):
    #             譯文 | Translated text
    #         file (int):
    #             檔案 ID | File ID
    #         stage (int):
    #             詞條翻譯狀態 | Strings translation status
    #             0: 未翻譯 | Untranslated
    #             1: 已翻譯 | Translated
    #             2: 有疑問 | Questionable
    #             3: 已審核 | Reviewed
    #             5: 已二次審核 | Double reviewed
    #             9: 已鎖定 | Locked
    #             -9: 已隱藏 | Hidden
    #         context (str):
    #             上下文 | Context

    #     Returns:
    #         dict:
    #             詞條資訊 | Strings information
    #     """
    #     strings_url = f"{self._projects_url}/{project_id}/strings"
    #     data = {
    #         "key": key,
    #         "original": original_text,
    #         "translation": translate_text,
    #         "file": {"name": file},
    #         "stage": stage,
    #         "context": context
    #     }
    #     return self._request("POST", strings_url, json=data)

    def get_string(self, project_id: int, string_id: int) -> dict:
        """獲取單一詞條資訊 | Get single string information

        Args:
            project_id (int):
                專案 ID | Project ID
            string_id (int):
                詞條 ID | String ID

        Returns:
            dict:
                詞條資訊 | String information
        """
        strings_url = f"{self._projects_url}/{project_id}/strings/{string_id}"
        return self._request("GET", strings_url)

    def update_string(
        self,
        project_id: int,
        string_id: int,
        key: str = None,
        original_text: str = None,
        translate_text: str = None,
        stage: int = None,
        context: str = None,
    ) -> dict:
        """更新詞條 | Update string

        Args:
            project_id (int):
                專案 ID | Project ID
            string_id (int):
                詞條 ID | String ID
            key (str):
                詞條 Key | Strings Key
            original_text (str):
                原文 | Original text
            translate_text (str):
                譯文 | Translated text
            stage (int):
                詞條翻譯狀態 | Strings translation status
                0: 未翻譯 | Untranslated
                1: 已翻譯 | Translated
                2: 有疑問 | Questionable
                3: 已審核 | Reviewed
                5: 已二次審核 | Double reviewed
                9: 已鎖定 | Locked
                -9: 已隱藏 | Hidden
            context (str):
                上下文 | Context

        Returns:
            dict:
                詞條資訊 | Strings information
        """
        strings_url = f"{self._projects_url}/{project_id}/strings/{string_id}"
        data = {
            "key": key,
            "original": original_text,
            "translation": translate_text,
            "stage": stage,
            "context": context,
        }
        return self._request("PUT", strings_url, json=data)

    def delete_string(self, project_id: int, string_id: int) -> int:
        """刪除詞條 | Delete string

        Args:
            project_id (int):
                專案 ID | Project ID
            string_id (int):
                詞條 ID | String ID

        Returns:
            int:
                狀態碼 | Status code
        """
        strings_url = f"{self._projects_url}/{project_id}/strings/{string_id}"
        return self._request("DELETE", strings_url, return_status=True)

from paratranz.api.projects import Projects

class ParaTranz:
    __slots__ = ("_api_token", "_api_url", "_headers")

    DEFAULT_API_URL = "https://paratranz.cn/api"

    def __init__(self, api_token: str=None, api_url: str=None):
        """
        初始化 ParaTranz 類別。
        Initialize the ParaTranz class.

        Parameters:
        api_token (str): The API token.
        api_url (str): The API URL (default: https://paratranz.cn/api).
        """
        self._api_token = api_token
        self._api_url = api_url or self.DEFAULT_API_URL
        self._headers = {
            "Authorization": api_token,
            "User-Agent": "paratranz-py | Made by @xMikux"
        }

    @property
    def projects(self):
        return Projects(
            api_headers=self._headers,
            api_url=self._api_url            
        )

from .api.projects import Projects
# from .api.strings import Strings
from .api.files import Files
from .api.history import History
from .api.scores import Scores


class ParaTranz:
    __slots__ = ("_api_token", "_api_url", "_headers")

    DEFAULT_API_URL = "https://paratranz.cn/api"

    def __init__(self, api_token: str = None, api_url: str = None):
        """初始化 ParaTranz 類別 | Initialize the ParaTranz class.

        Args:
            api_token (str):
                The API token.
            api_url (str):
                The API URL (default: https://paratranz.cn/api).
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

    # @property
    # def strings(self):
    #     return Strings(
    #         api_headers=self._headers,
    #         api_url=self._api_url
    #     )

    @property
    def files(self):
        return Files(
            api_headers=self._headers,
            api_url=self._api_url
        )

    @property
    def scores(self):
        return Scores(
            api_headers=self._headers,
            api_url=self._api_url
        )

    @property
    def history(self):
        return History(
            api_headers=self._headers,
            api_url=self._api_url
        )

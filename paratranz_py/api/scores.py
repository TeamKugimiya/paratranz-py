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
        return self._request("GET", scores_url)

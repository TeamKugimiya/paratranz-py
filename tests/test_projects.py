import pytest
from unittest.mock import patch

from paratranz_py.api.projects import Projects


HEADERS = {"Authorization": "test-token"}
BASE_URL = "https://paratranz.cn/api"


@pytest.fixture
def projects():
    return Projects(api_headers=HEADERS, api_url=BASE_URL)


class TestUpdateProject:
    def _call(self, projects_api, **kwargs):
        with patch.object(projects_api, "_request", return_value={"id": 1}) as mock_req:
            result = projects_api.update_project(project_id=1, **kwargs)
        return result, mock_req

    def test_single_field_only_sends_that_field(self, projects):
        """非擁有者管理員只改 review_mode 時，不應送出 privacy/joinMode 等擁有者欄位"""
        _, mock_req = self._call(projects, review_mode=1)
        body = mock_req.call_args.kwargs["json"]
        assert body == {"reviewMode": 1}
        assert "privacy" not in body
        assert "joinMode" not in body

    def test_all_fields_sent_when_all_provided(self, projects):
        _, mock_req = self._call(
            projects,
            project_name="名稱",
            project_description="描述",
            game_name="mc",
            privacy_mode=0,
            download_mode=0,
            issue_mode=0,
            review_mode=1,
            join_mode=0,
        )
        body = mock_req.call_args.kwargs["json"]
        assert body == {
            "name": "名稱",
            "desc": "描述",
            "game": "mc",
            "privacy": 0,
            "download": 0,
            "issueMode": 0,
            "reviewMode": 1,
            "joinMode": 0,
        }

    def test_none_fields_omitted(self, projects):
        _, mock_req = self._call(projects, project_name="X", privacy_mode=None)
        body = mock_req.call_args.kwargs["json"]
        assert "privacy" not in body
        assert body["name"] == "X"

    def test_uses_put_method(self, projects):
        _, mock_req = self._call(projects, project_name="X")
        assert mock_req.call_args.args[0] == "PUT"

    def test_uses_correct_url(self, projects):
        _, mock_req = self._call(projects, project_name="X")
        assert mock_req.call_args.args[1] == f"{BASE_URL}/projects/1"

import pytest
import requests
from unittest.mock import MagicMock, patch

from paratranz_py.api.base import ParaTranzAPI


HEADERS = {"Authorization": "test-token"}
BASE_URL = "https://paratranz.cn/api"


@pytest.fixture
def api():
    return ParaTranzAPI(api_headers=HEADERS, api_url=BASE_URL)


def _mock_response(status_code=200, json_data=None, text=""):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.text = text
    resp.json.return_value = json_data if json_data is not None else {}
    resp.raise_for_status.return_value = None
    return resp


class TestRequest:
    def test_returns_json_on_success(self, api):
        resp = _mock_response(json_data={"id": 1})
        with patch.object(api.session, "request", return_value=resp):
            result = api._request("GET", f"{BASE_URL}/projects")
        assert result == {"id": 1}

    def test_returns_status_code_when_return_status_true(self, api):
        resp = _mock_response(status_code=204)
        with patch.object(api.session, "request", return_value=resp):
            result = api._request("DELETE", f"{BASE_URL}/projects/1", return_status=True)
        assert result == 204

    def test_returns_none_on_timeout(self, api):
        with patch.object(api.session, "request", side_effect=requests.Timeout):
            result = api._request("GET", f"{BASE_URL}/projects")
        assert result is None

    def test_returns_none_on_connection_error(self, api):
        with patch.object(api.session, "request", side_effect=requests.ConnectionError):
            result = api._request("GET", f"{BASE_URL}/projects")
        assert result is None

    def test_http_error_logs_status_and_body(self, api):
        resp = _mock_response(status_code=403, text='{"message":"Permission denied"}')
        http_err = requests.HTTPError(response=resp)
        resp.raise_for_status.side_effect = http_err
        with patch.object(api.session, "request", return_value=resp):
            with patch("paratranz_py.api.base.logger") as mock_logger:
                result = api._request("PUT", f"{BASE_URL}/projects/1/strings/1")
        assert result is None
        logged = mock_logger.error.call_args[0][0]
        assert "403" in logged
        assert "Permission denied" in logged

    def test_returns_text_on_invalid_json(self, api):
        resp = _mock_response(text="not-json")
        resp.json.side_effect = ValueError("No JSON")
        with patch.object(api.session, "request", return_value=resp):
            result = api._request("GET", f"{BASE_URL}/projects")
        assert result == "not-json"

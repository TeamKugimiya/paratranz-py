import pytest
from unittest.mock import patch

from paratranz_py.api.strings import Strings


HEADERS = {"Authorization": "test-token"}
BASE_URL = "https://paratranz.cn/api"


@pytest.fixture
def strings():
    return Strings(api_headers=HEADERS, api_url=BASE_URL)


class TestUpdateString:
    def _call(self, strings_api, **kwargs):
        with patch.object(strings_api, "_request", return_value={"id": 42}) as mock_req:
            result = strings_api.update_string(project_id=1, string_id=42, **kwargs)
        return result, mock_req

    def test_only_translation_is_sent_when_only_translate_text_provided(self, strings):
        """核心 bug 修正：一般翻譯者只傳 translate_text，不應送出 original/key"""
        result, mock_req = self._call(strings, translate_text="你好")
        body = mock_req.call_args.kwargs["json"]
        assert body == {"translation": "你好"}
        assert "original" not in body
        assert "key" not in body

    def test_stage_zero_is_not_filtered(self, strings):
        """stage=0 是合法值，不能被 None 過濾掉"""
        _, mock_req = self._call(strings, translate_text="hello", stage=0)
        body = mock_req.call_args.kwargs["json"]
        assert body["stage"] == 0

    def test_all_fields_sent_when_all_provided(self, strings):
        _, mock_req = self._call(
            strings,
            key="test.key",
            original_text="Hello",
            translate_text="你好",
            stage=1,
            context="greeting",
        )
        body = mock_req.call_args.kwargs["json"]
        assert body == {
            "key": "test.key",
            "original": "Hello",
            "translation": "你好",
            "stage": 1,
            "context": "greeting",
        }

    def test_none_fields_are_omitted(self, strings):
        """None 欄位一律過濾，避免觸發管理員權限檢查"""
        _, mock_req = self._call(strings, translate_text="world", context=None)
        body = mock_req.call_args.kwargs["json"]
        assert "context" not in body

    def test_uses_correct_url(self, strings):
        _, mock_req = self._call(strings, translate_text="x")
        url = mock_req.call_args.args[1]
        assert url == f"{BASE_URL}/projects/1/strings/42"

    def test_uses_put_method(self, strings):
        _, mock_req = self._call(strings, translate_text="x")
        method = mock_req.call_args.args[0]
        assert method == "PUT"


class TestGetStrings:
    def test_default_params_returns_all_stages(self, strings):
        """預設不帶 stage，回傳所有狀態的詞條"""
        with patch.object(strings, "_request", return_value={}) as mock_req:
            strings.get_strings(project_id=5)
        params = mock_req.call_args.kwargs["params"]
        assert params["page"] == 1
        assert params["pageSize"] == 50
        assert "stage" not in params

    def test_stage_zero_forwarded_when_explicitly_passed(self, strings):
        """stage=0 明確傳入時必須送出"""
        with patch.object(strings, "_request", return_value={}) as mock_req:
            strings.get_strings(project_id=5, stage=0)
        params = mock_req.call_args.kwargs["params"]
        assert params["stage"] == 0

    def test_file_id_param(self, strings):
        with patch.object(strings, "_request", return_value={}) as mock_req:
            strings.get_strings(project_id=5, file_id=99)
        params = mock_req.call_args.kwargs["params"]
        assert params["file"] == 99

    def test_file_id_omitted_when_not_provided(self, strings):
        with patch.object(strings, "_request", return_value={}) as mock_req:
            strings.get_strings(project_id=5)
        params = mock_req.call_args.kwargs["params"]
        assert "file" not in params


class TestCreateString:
    def _call(self, strings_api, **kwargs):
        with patch.object(strings_api, "_request", return_value={"id": 1}) as mock_req:
            result = strings_api.create_string(
                project_id=1, key="test.key", original_text="Hello", file=10, **kwargs
            )
        return result, mock_req

    def test_required_fields_are_sent(self, strings):
        _, mock_req = self._call(strings)
        body = mock_req.call_args.kwargs["json"]
        assert body["key"] == "test.key"
        assert body["original"] == "Hello"
        assert body["file"] == 10

    def test_file_sent_as_int_not_dict(self, strings):
        _, mock_req = self._call(strings)
        body = mock_req.call_args.kwargs["json"]
        assert isinstance(body["file"], int)

    def test_optional_fields_omitted_when_not_provided(self, strings):
        _, mock_req = self._call(strings)
        body = mock_req.call_args.kwargs["json"]
        assert "translation" not in body
        assert "stage" not in body
        assert "context" not in body

    def test_optional_fields_sent_when_provided(self, strings):
        _, mock_req = self._call(
            strings, translate_text="你好", stage=1, context="greeting"
        )
        body = mock_req.call_args.kwargs["json"]
        assert body["translation"] == "你好"
        assert body["stage"] == 1
        assert body["context"] == "greeting"

    def test_uses_post_method(self, strings):
        _, mock_req = self._call(strings)
        assert mock_req.call_args.args[0] == "POST"

    def test_uses_correct_url(self, strings):
        _, mock_req = self._call(strings)
        assert mock_req.call_args.args[1] == f"{BASE_URL}/projects/1/strings"


class TestGetString:
    def test_correct_url(self, strings):
        with patch.object(strings, "_request", return_value={}) as mock_req:
            strings.get_string(project_id=1, string_id=7)
        url = mock_req.call_args.args[1]
        assert url == f"{BASE_URL}/projects/1/strings/7"


class TestDeleteString:
    def test_uses_delete_with_return_status(self, strings):
        with patch.object(strings, "_request", return_value=200) as mock_req:
            result = strings.delete_string(project_id=1, string_id=7)
        assert mock_req.call_args.kwargs.get("return_status") is True
        assert result == 200

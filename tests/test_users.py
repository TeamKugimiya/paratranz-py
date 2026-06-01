import pytest
from unittest.mock import patch

from paratranz_py.api.users import Users


HEADERS = {"Authorization": "test-token"}
BASE_URL = "https://paratranz.cn/api"


@pytest.fixture
def users():
    return Users(api_headers=HEADERS, api_url=BASE_URL)


class TestUpdateUser:
    def _call(self, users_api, **kwargs):
        with patch.object(users_api, "_request", return_value={"id": 1}) as mock_req:
            result = users_api.update_user(user_id=1, **kwargs)
        return result, mock_req

    def test_only_nickname_sent_when_only_nickname_provided(self, users):
        """局部更新：只傳 nickname 時不應送出 bio/avatar（避免覆寫現有值）"""
        _, mock_req = self._call(users, nickname="新暱稱")
        body = mock_req.call_args.kwargs["json"]
        assert body == {"nickname": "新暱稱"}
        assert "bio" not in body
        assert "avatar" not in body

    def test_all_fields_sent_when_all_provided(self, users):
        _, mock_req = self._call(
            users, nickname="A", bio="bio text", avatar="https://example.com/img.png"
        )
        body = mock_req.call_args.kwargs["json"]
        assert body == {
            "nickname": "A",
            "bio": "bio text",
            "avatar": "https://example.com/img.png",
        }

    def test_none_fields_omitted(self, users):
        _, mock_req = self._call(users, nickname="X", bio=None, avatar=None)
        body = mock_req.call_args.kwargs["json"]
        assert "bio" not in body
        assert "avatar" not in body

    def test_uses_put_method(self, users):
        _, mock_req = self._call(users, nickname="X")
        assert mock_req.call_args.args[0] == "PUT"

    def test_uses_correct_url(self, users):
        _, mock_req = self._call(users, nickname="X")
        assert mock_req.call_args.args[1] == f"{BASE_URL}/users/1"

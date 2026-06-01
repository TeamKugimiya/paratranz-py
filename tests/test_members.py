import pytest
from unittest.mock import patch

from paratranz_py.api.members import Members


HEADERS = {"Authorization": "test-token"}
BASE_URL = "https://paratranz.cn/api"


@pytest.fixture
def members():
    return Members(api_headers=HEADERS, api_url=BASE_URL)


class TestUpdateMember:
    def test_note_none_is_omitted(self, members):
        with patch.object(members, "_request", return_value={}) as mock_req:
            members.update_member(project_id=1, member_id=5, permission=1)
        body = mock_req.call_args.kwargs["json"]
        assert "note" not in body
        assert body["permission"] == 1

    def test_note_is_sent_when_provided(self, members):
        with patch.object(members, "_request", return_value={}) as mock_req:
            members.update_member(project_id=1, member_id=5, permission=2, note="備註")
        body = mock_req.call_args.kwargs["json"]
        assert body["note"] == "備註"

    def test_invalid_permission_returns_none(self, members):
        result = members.update_member(project_id=1, member_id=5, permission=10)
        assert result is None


class TestAddMember:
    def test_invalid_permission_returns_none(self, members):
        result = members.add_member(project_id=1, member_uid=99, permission=10)
        assert result is None

    def test_valid_permission_sends_request(self, members):
        with patch.object(members, "_request", return_value={}) as mock_req:
            members.add_member(project_id=1, member_uid=99, permission=1)
        assert mock_req.called

    def test_note_none_is_omitted(self, members):
        with patch.object(members, "_request", return_value={}) as mock_req:
            members.add_member(project_id=1, member_uid=99, permission=1)
        body = mock_req.call_args.kwargs["json"]
        assert "note" not in body

    def test_note_sent_when_provided(self, members):
        with patch.object(members, "_request", return_value={}) as mock_req:
            members.add_member(project_id=1, member_uid=99, permission=1, note="備註")
        body = mock_req.call_args.kwargs["json"]
        assert body["note"] == "備註"

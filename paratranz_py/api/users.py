from .base import ParaTranzAPI


class Users(ParaTranzAPI):
    """
    ParaTranz 使用者 API 類別
    ParaTranz Users API class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._users_url = f"{self._api_url}/users"

    def get_user(self, user_id: int):
        """獲取使用者資訊 | Get user info.

        Args:
            user_id (int):
                使用者 ID | User ID

        Returns:
            dict: 使用者資訊 | User info.
        """
        return self._request("GET", f"{self._users_url}/{user_id}")

    def update_user(
        self, user_id: int, nickname: str = None, bio: str = None, avatar: str = None
    ) -> dict:
        """更新使用者資訊 | Update user info.

        Args:
            user_id (int):
                使用者 ID | User ID
            nickname (str):
                暱稱 | Nickname
            bio (str):
                簡介 | Bio
            avatar (str):
                頭像連結 | Avatar URL

        Returns:
            dict: 更新後的使用者資訊 | Updated user info.
        """
        data = {"nickname": nickname, "bio": bio, "avatar": avatar}
        return self._request("PUT", f"{self._users_url}/{user_id}", json=data)

class SlackAdapterMock:
    def create_channel(self, channel_name: str, is_private: bool):
        return {
            "ok": True,
            "channel": {"id": "C12345"}
        }

    def set_channel_owner(self, channel_id: str, user_email: str):
        return {"ok": True}

    def add_users_to_channel(self, channel_id: str, user_email_list: list):
        return {"ok": True}

    def post_message_on_channel(self, channel_id: str, message: str):
        return {"ok": True}

    def _get_user_id_by_email(self, user_email):
        return "U12345"

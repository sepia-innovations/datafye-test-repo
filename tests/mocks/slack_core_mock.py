class SlackCoreMock:
    def __init__(self, logger):
        self.logger = logger

    def create_channel(self, channel_name: str, is_private: bool):
        return {"status_code": 200, "channel_id": "C12345", "message": f"{channel_name} channel created with id C12345"}

    def set_channel_owner(self, channel_id: str, user_email: str):
        return {"status_code": 200, "message": f"{user_email} set as channel {channel_id} owner"}

    def add_users_to_channel(self, channel_id: str, user_email_list: list):
        return {"status_code": 200, "message": f"Users {user_email_list} successfully added to channel {channel_id}"}

    def post_message_on_channel(self, channel_id: str, message: str):
        return {"status_code": 200, "message": f"Message successfully posted on channel {channel_id}"}

from unittest.mock import Mock

class SlackServiceMock(Mock):
    def create_channel(self, request):
        return 200, {"status_code": 200, "channel_id": "C12345", "message": "Channel created"}

    def set_channel_owner(self, channel_id, request):
        return 200, {"status_code": 200, "message": "Owner set"}

    def add_users_to_channel(self, channel_id, request):
        return 200, {"status_code": 200, "message": "Users added"}

    def post_message_on_channel(self, channel_id, request):
        return 200, {"status_code": 200, "message": "Message posted"}

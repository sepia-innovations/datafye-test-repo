import os
import requests
from adapter.slack_adapter import SlackAdapter


class SlackCore:
    def __init__(self, logger):
        self.logger = logger
        self.slack_adapter = SlackAdapter(logger)


    def handle_api_response(self, response, success_message, failure_message):
        if response.get("ok"):
            self.logger.info(success_message)
            # Special handling for `create_channel` to extract `channel_id`
            if 'channel' in response and 'id' in response['channel']:
                return {
                    "status_code": 200,
                    "channel_id": response['channel']['id'],
                    "message": success_message
                }
            return {
                "status_code": 200,
                "message": success_message
            }

        error_message = response.get("error", "Unknown error")
        user_friendly_message = self.get_user_friendly_message(error_message, failure_message)
        self.logger.error(failure_message + f": {error_message}")
        return {
            "status_code": response.get("status_code", 400),
            "error": user_friendly_message
        }
    

    def get_user_friendly_message(self, error_message, failure_message):
        if "permission" in error_message.lower():
            return f"{failure_message} due to insufficient permissions. Please ensure you have the necessary rights."
        elif "user_not_in_channel" in error_message.lower():
            return "Failed to set owner: The user is not a member of the channel."
        elif "user_not_found" in error_message.lower():
            return "Failed to add users: One or more users were not found."
        elif "channel_not_found" in error_message.lower():
            return f"{failure_message}: The channel does not exist."
        else:
            return f"{failure_message}: {error_message}"
        

    def create_channel(self, channel_name: str, is_private: bool):
        try:
            self.logger.info("Making call to create channel")
            response = self.slack_adapter.create_channel(channel_name, is_private)
            success_message = f"Channel with name \"{channel_name}\" created successfully."
            return self.handle_api_response(response, success_message, "Channel creation failed")
        
        except Exception as e:
            self.logger.error(f"Exception occurred while creating channel: {e}")
            return {
                "status_code": 500,
                "error": "An unexpected error occurred while creating the channel."
            }


    def set_channel_owner(self, channel_id: str, user_email: str):
        try:
            self.logger.info(f"Making call to set user {user_email} as owner of channel {channel_id}")
            response = self.slack_adapter.set_channel_owner(channel_id, user_email)
            success_message = f"User {user_email} is successfully set as owner of channel id {channel_id}."
            return self.handle_api_response(response, success_message, "Failed to set channel owner")
        
        except Exception as e:
            self.logger.error(f"Exception occurred while setting channel owner: {e}")
            return {
                "status_code": 500,
                "error": "An unexpected error occurred while setting the channel owner."
            }


    def add_users_to_channel(self, channel_id: str, user_email_list: list):
        try:
            self.logger.info(f"Making call to add users - {user_email_list} to channel id {channel_id}")
            response = self.slack_adapter.add_users_to_channel(channel_id, user_email_list)
            success_message = f"Users {user_email_list} were successfully added to channel id {channel_id}."
            return self.handle_api_response(response, success_message, "Failed to add users to channel")
        
        except Exception as e:
            self.logger.error(f"Exception occurred while adding users to channel: {e}")
            return {
                "status_code": 500,
                "error": "An unexpected error occurred while adding users to the channel."
            }


    def post_message_on_channel(self, channel_id: str, message: str):
        try:
            self.logger.info(f"Making call to post message on channel id {channel_id}")
            response = self.slack_adapter.post_message_on_channel(channel_id, message)
            success_message = "Message successfully posted."
            return self.handle_api_response(response, success_message, "Failed to post message on channel")
        
        except Exception as e:
            self.logger.error(f"Exception occurred while posting message on channel: {e}")
            return {
                "status_code": 500,
                "error": "An unexpected error occurred while posting the message."
            }

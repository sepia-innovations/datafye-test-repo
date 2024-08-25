import os
import requests

class SlackAdapter:
    def __init__(self, logger):
        self.logger = logger
        self.slack_base_url = os.environ.get("SLACK_BASE_URL")
        self.slack_token = os.environ.get("SLACK_TOKEN")


    def create_channel(self, channel_name: str, is_private: bool):
        create_channel_endpoint = f"{self.slack_base_url}/conversations.create"
        self.logger.info(f"making call to channel creation api - {create_channel_endpoint}")
        payload = {
            "name": channel_name,
            "is_private": is_private
        }
        headers = {
            "Authorization": f"Bearer {self.slack_token}",
            "Content-Type": "application/json"
        }
        
        def request_func(url, json = None, headers = None):
            return requests.post(url, json = json, headers = headers, timeout = 600)

        response = self._handle_request(request_func, create_channel_endpoint, json = payload, headers = headers)
        
        return response
    

    def set_channel_owner(self, channel_id: str, user_email: str):
        self.logger.info("Make call to get user id for {user_email}")
        user_id = self._get_user_id_by_email(user_email)

        self.logger.info(f"Make call to add user {user_id} to channel {channel_id}")
        response = self.add_users_to_channel(channel_id, user_email.split(","))

        set_owner_endpoint = f"{self.slack_base_url}/conversations.setOwner"
        self.logger.info(f"making call to set channel owner api - {set_owner_endpoint}")
        
        payload = {
            "channel": channel_id,
            "user": user_id
        }
        headers = {
            "Authorization": f"Bearer {self.slack_token}",
            "Content-Type": "application/json"
        }
        
        def request_func(url, json = None, headers = None):
            return requests.post(url, json = json, headers = headers, timeout = 600)

        response = self._handle_request(request_func, set_owner_endpoint, json=payload, headers=headers)
        
        return response
    

    def add_users_to_channel(self, channel_id: str, user_email_list: list):
        self.logger.info("Make call to get user id for {user_email_list}")
        user_id_list = []
        for user_email in user_email_list:
            user_id = self._get_user_id_by_email(user_email)
            user_id_list.append(user_id)

        slack_invite_endpoint = f"{self.slack_base_url}/conversations.invite"
        self.logger.info(f"making call to add users to channel api - {slack_invite_endpoint}")

        payload = {
            "channel": channel_id,
            "users": ','.join(user_id_list)
        }
        headers = {
            "Authorization": f"Bearer {self.slack_token}",
            "Content-Type": "application/json"
        }

        def request_func(url, json = None, headers = None):
            return requests.post(url, json = json, headers = headers, timeout = 600)

        response = self._handle_request(request_func, slack_invite_endpoint, json = payload, headers = headers)
        
        return response
    

    def post_message_on_channel(self, channel_id: str, message: str):
        self.logger.info("Make call to post message on channel {channel_id}")
        slack_post_message_endpoint = f"{self.slack_base_url}/chat.postMessage"
        self.logger.info(f"Making call to post message on channel api - {slack_post_message_endpoint}")

        payload = {
            "channel": channel_id,
            "text": message
        }
        headers = {
            "Authorization": f"Bearer {self.slack_token}",
            "Content-Type": "application/json"
        }

        def request_func(url, json = None, headers = None):
            return requests.post(url, json = json, headers = headers, timeout = 600)

        response = self._handle_request(request_func, slack_post_message_endpoint, json = payload, headers = headers)
        
        return response
    

    def _get_user_id_by_email(self, user_email):
        slack_channel_endpoint = f"{self.slack_base_url}/users.lookupByEmail"
        self.logger.info("Making call to get user id from email id api - {slack_channel_endpoint}")
        payload = {
            "email": user_email
        }
        headers = {
            "Authorization": f"Bearer {self.slack_token}"
        }

        def request_func(url, json = None, headers = None):
            return requests.post(url, json = json, headers = headers, timeout = 600)

        response = self._handle_request(request_func, slack_channel_endpoint, json = payload, headers = headers)
    
        if response.status_code == 200:
            user_info = response.json()
            if user_info.get("ok"):
                return user_info["user"]["id"]
            self.logger.error(f"Error in getting user id for {user_email}: {user_info['error']}")
        else:
            self.logger.error(f"Failed to connect to Slack API: {response.status_code}")

        return None
    

    def _handle_request(self, request_func, *args, **kwargs):
        try:
            response = request_func(*args, **kwargs)
            response.raise_for_status()
            return response.json()
        
        except requests.HTTPError as http_err:
            return {
                "status_code": response.status_code if response else 500,
                "error": f"HTTP error occurred: {http_err}"
            }
        
        except requests.RequestException as req_err:
            return {
                "status_code": 500,
                "error": f"Request error occurred: {req_err}"
            }
        
        except Exception as ex:
            return {
                "status_code": 500,
                "error": f"An unexpected error occurred: {ex}"
            }

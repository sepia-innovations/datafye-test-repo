from core.slack_core import SlackCore
from models.add_users_request import AddUserToChannelRequest
from models.create_channel_request import CreateChannelRequest
from models.post_message_request import PostMessageRequest
from models.set_owner_request import SetOwnerRequest


class SlackService:
    def __init__(self, logger):
        self.slack_core = SlackCore(logger)
        self.logger = logger


    def create_channel(self, request: CreateChannelRequest):
        try:
            self.logger.info("Validating the request")
            request_errors = []

            if not request.channel_name:
                self.logger.error("Invalid Request. Channel name is missing.")
                request_errors.append("Invalid Request. Channel name is missing.")

            if len(request_errors) > 0:
                return 400, {
                                "status_code": 500, 
                                "error": request_errors
                            }
            
            self.logger.info("Request id valid")
            response = self.slack_core.create_channel(request.channel_name, request.is_private)
            return response["status_code"], response

        except Exception as ex:
            self.logger.error(f"Exception occurred while serving request to create channel - {ex}")
            return 500, {
                            "status_code": 500, 
                            "error": "Internal server error - Failed to create channel"
                        }
    

    def set_channel_owner(self, channel_id: str, request: SetOwnerRequest):
        try:
            self.logger.info("Validating the request")
            request_errors = []

            if not channel_id:
                self.logger.error("Invalid Request. Channel id is missing.")
                request_errors.append("Invalid Request. Channel id is missing.")

            if not request.user_email:
                self.logger.error("Invalid Request. User email is missing.")
                request_errors.append("Invalid Request. User email is missing.")

            if len(request_errors) > 0:
                return 400, {
                                "status_code": 500, 
                                "error": request_errors
                            }
            
            self.logger.info("Request id valid")
            response = self.slack_core.set_channel_owner(channel_id, request.user_email)
            return response["status_code"], response

        except Exception as ex:
            self.logger.error(f"Exception occurred while serving request to set channel owner - {ex}")
            return 500, {
                            "status_code": 500, 
                            "error": "Internal server error - Failed to set channel owner"
                        }
    

    def add_users_to_channel(self, channel_id: str, request: AddUserToChannelRequest):
        try:
            self.logger.info("Validating the request")
            request_errors = []

            if not channel_id:
                self.logger.error("Invalid Request. Channel id is missing.")
                request_errors.append("Invalid Request. Channel id is missing.")

            if len(request.user_email_list) == 0:
                self.logger.error("Invalid Request. User email is missing.")
                request_errors.append("Invalid Request. User email is missing.")

            if len(request_errors) > 0:
                return 400, {
                                "status_code": 500, 
                                "error": request_errors
                            }
            
            self.logger.info("Request id valid")
            response = self.slack_core.add_users_to_channel(channel_id, request.user_email_list)
            return response["status_code"], response
        
        except Exception as ex:
            self.logger.error(f"Exception occurred while serving request to add user(s) to channel - {ex}")
            return 500, {
                            "status_code": 500, 
                            "error": "Internal server error - Failed to add user(s) to channel"
                        }
    

    def post_message_on_channel(self, channel_id: str, request: PostMessageRequest):
        try:
            self.logger.info("Validating the request")
            request_errors = []

            if not channel_id:
                self.logger.error("Invalid Request. Channel id is missing.")
                request_errors.append("Invalid Request. Channel id is missing.")

            if len(request.message) == 0:
                self.logger.error("Invalid Request. User email is missing.")
                request_errors.append("Invalid Request. User email is missing.")

            if len(request_errors) > 0:
                return 400, {
                                "status_code": 500, 
                                "error": request_errors
                            }
            
            self.logger.info("Request id valid")
            response = self.slack_core.post_message_on_channel(channel_id, request.message)
            return response["status_code"], response
            
        except Exception as ex:
            self.logger.error(f"Exception occurred while serving request to post message on channel - {ex}")
            return 500, {
                            "status_code": 500, 
                            "error": "Internal server error - Failed to post message on channel"
                        }

import os
import requests

class OktaService:
    def __init__(self):
        self.okta_token = os.getenv("OKTA_TOKEN")

    def get_okta_user_details(self):
        okta_user_info_url = "https://avahi.okta.com/oauth2/default/v1/userinfo"
        headers = {
            "Authorization": f"Bearer {self.okta_token}"
        }
        response = requests.get(okta_user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()

import requests

from config import API_BASE_URL


class API:

    def __init__(self):
        self.API_BASE_URL = API_BASE_URL

    def generate_key(self, telegram_id: int) -> dict:
        link = f'{self.API_BASE_URL}/users/{telegram_id}/generate-key'
        response = requests.get(link)

        return response.json()

    def create_user(self, username: str, telegram_id: int) -> dict:
        link = f'{self.API_BASE_URL}/users'
        data = dict(username=username, telegram_id=telegram_id)

        response = requests.post(link, json=data)

        response_json = response.json()
        response_json['status'] = True if response.status_code == 201 else False

        return response_json

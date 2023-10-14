import requests
import os

from dotenv import load_dotenv

class UserService:
    load_dotenv()
    HOST = os.getenv('USERS_PATH')

    def get_user_me(self, token) :
        try:
            response = requests.get(f'{self.HOST}/users/me', headers={'Authorization': f'Bearer {token}', 'Content-type': 'application/json', 'Accept': 'application/json'})
            if response.status_code == 200:
                return True
            else :
                return False
        except Exception as e:
                    raise e
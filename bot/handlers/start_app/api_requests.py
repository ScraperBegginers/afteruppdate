import requests
from config import API_TOKEN

def create_user(user_id, first_name, username):
    response = requests.post(
        'https://afteruppdate.onrender.com/api/register_user',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  # Убедимся, что это JSON
        }, 
        json={  # Отправляем JSON вместо data
            'user_id': user_id,
            'firstname': first_name,
            'username': username
        }
    )
    if response.status_code == 200:
        pass
    else:
        print(response.json())


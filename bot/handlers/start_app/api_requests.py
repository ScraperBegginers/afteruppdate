import requests
from config import API_TOKEN

def create_user(user_id, first_name, username):
    response = requests.post(
        'https://afteruppdate.onrender.com/api/register_user',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'user_id': user_id,
            'firstname': first_name,
            'username': username
        }
    )
    if response.status_code == 200:
        print('Пользователь был создан')
    else:
        print(response.json())

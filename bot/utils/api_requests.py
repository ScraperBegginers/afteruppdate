import requests
from config import API_TOKEN

URL = 'https://afteruppdate.onrender.com/api'

def create_user(user_id, first_name, username):
    response = requests.post(
        URL + '/register_user',
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
        
def get_all_channels():
    response = requests.get(
        URL + '/tasks'
    )
    return response.json()

def add_channel(channel_id, channel_link):
    response = requests.post(
        URL + '/add_tasks',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'link': channel_link,
            'channel_id': channel_id,
        }
    )
    if response.status_code == 200:
        print('Канал был добавлен для подписок!')
    else:
        print(response.json())
    
    
def def_channel(channel_id):
    response = requests.post(
        URL + '/del_tasks',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'channel_id': channel_id,
        }
    )
    if response.status_code == 200:
        print('Канал был удален из подписок!')
    else:
        print(response.json())
    
def add_referral(user_id, referral_id):
    response = requests.post(
        URL + '/add_tasks',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'user_id': user_id,
            'referral': referral_id,
        }
    )
    if response.status_code == 200:
        print('Реферал был добавлен')
    else:
        print(response.json())
        
def get_all_sub():
    response = requests.get(
        URL + '/get_subscription_trhrottling'
    )
    return response.json()

def add_complete_sub(user_id, channel_id):
    response = requests.post(
        URL + '/add_complete_tasks',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'user_id': user_id,
            'channel_id': channel_id,
        }
    )
    
    responseAddIncrement = requests.post(
        URL + '/spins/increment',
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'  
        }, 
        json={ 
            'user_id': user_id
        }
    )
    
    if response.status_code == 200:
        print(f'{user_id} подписался на {channel_id}')
    if responseAddIncrement.status_code == 200:
        print(f'Пользователю: {user_id} прибавлен спин')
import requests
from telegram import Bot
from dotenv import load_dotenv
import os
import json


load_dotenv()
token = os.getenv('TG_TOKEN')
bot = Bot(token)
chat_id = os.getenv('CHAT_ID')
url = 'https://dvmn.org/api/long_polling/'
headers = {
    "Authorization": f"Token {os.getenv('TOKEN')}",
}
params = {}
while True:
    try:
        response = requests.get(url, headers=headers, timeout=5, params=params)
        print(response.request.url)
        response.raise_for_status()
        data = response.json()
        if data['status']=='found':
            reviews = data['new_attempts']
            review = reviews[0]
            lesson_title = review['lesson_title']
            lesson_url = review['lesson_url']
            if review['is_negative']==True:
                result = 'К сожалению, в работе нашлись ошибки'
            else:
                result = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
            timestamp = data['last_attempt_timestamp']
            bot.send_message(chat_id=chat_id, text=f'У вас проверили работу "{lesson_title}." {result}. {lesson_url}')
        elif data['status']=='timeout':
            timestamp = data['timestamp_to_request']
        params['timestamp']=timestamp
        print(json.dumps(data, ensure_ascii=False, indent=4))
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue
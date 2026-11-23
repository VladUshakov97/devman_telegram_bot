import json
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot


def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    bot = Bot(tg_token)
    tg_chat_id = os.environ['CHAT_ID']
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
    "Authorization": f"Token {os.environ['DEVMAN_TOKEN']}",
    }
    params = {}
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=5, params=params)
            response.raise_for_status()
            response_body = response.json()
            if response_body['status']=='found':
                reviews = response_body['new_attempts']
                review = reviews[0]
                lesson_title = review['lesson_title']
                lesson_url = review['lesson_url']
                if review['is_negative']==True:
                    result = 'К сожалению, в работе нашлись ошибки'
                else:
                    result = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
                timestamp = response_body['last_attempt_timestamp']
                bot.send_message(chat_id=tg_chat_id, text=f'У вас проверили работу "{lesson_title}." {result}. {lesson_url}')
            elif response_body['status']=='timeout':
                timestamp = response_body['timestamp_to_request']
            params['timestamp']=timestamp
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()

    
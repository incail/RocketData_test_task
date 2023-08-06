import json
import logging

import requests
from bs4 import BeautifulSoup


def yapdomik():
    logging.info('Start parsing yapdomik')
    cities = ['achinsk', 'berdsk', 'krsk', 'nsk', 'omsk', 'tomsk']
    result = get_data(cities)
    with open('yapdomik.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, sort_keys=False, ensure_ascii=False)
    logging.info(f'{len(result)} found')
    logging.info('Successfully')


def get_data(cities: list):
    """" Get locations from: https://yapdomik.ru/ """
    result_cards = []
    for city in cities:
        link = f'https://{city}.yapdomik.ru/'
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.find('a').find('img').get('alt')
        phones = soup.find('div', 'contacts__phone').text.replace('\n', '')
        scripts = soup.find_all('script')
        # tag that stores json data such as addresses, phone numbers and working hours
        data = json.loads(scripts[2].text[22:])
        for shop in data['shops']:
            result_cards.append(
                {
                    'name': name,
                    'address': '{}, {}'.format(data['city']['name'], shop['address']),
                    'latlon': [shop['coord']['latitude'], shop['coord']['longitude']],
                    'phones': [phones],
                    'working_hours': [
                        'Пн - Вс {} - {}'.format(shop['schedule'][0]['openTime'], shop['schedule'][0]['closeTime'])
                    ]
                }
            )
    return result_cards

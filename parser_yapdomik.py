import json
import logging

import requests
from bs4 import BeautifulSoup


def yapdomik():
    logging.info('Start parsing yapdomik')
    cities = ['achinsk', 'berdsk', 'krsk', 'nsk', 'omsk', 'tomsk']
    result = []
    for city in cities:
        result += parser(city)
    with open('yapdomik.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, sort_keys=False, ensure_ascii=False)
    logging.info('Successfully')


def parser(city: str):
    link = f'https://{city}.yapdomik.ru/'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('a').find('img').get('alt')
    phones = soup.find('div', 'contacts__phone').text.replace('\n', '')

    scripts = soup.find_all('script')
    data = json.loads(scripts[2].text[22:])
    result_card = {}
    for shop in data['shops']:
        result_card['name'] = name
        result_card['address'] = '{}, {}'.format(data['city']['name'], shop['address'])
        result_card['latlon'] = [shop['coord']['latitude'], shop['coord']['longitude']]
        result_card['phones'] = [phones]
        result_card['working_hours'] = [
            'Пн - Вс {} - {}'.format(shop['schedule'][0]['openTime'], shop['schedule'][0]['closeTime'])]
        yield result_card

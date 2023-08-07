import json
import logging
import re

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Yandex


def santaelena():
    logging.info('Start parsing santaelena')
    session = requests.Session()
    link = 'https://www.santaelena.com.co/tiendas-pasteleria/'
    response = session.get(url=link)
    soup = BeautifulSoup(response.text, 'lxml')
    # getting links to the cities where this company is located
    html_cities = soup.find('li', class_='menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-489 current_page_item menu-item-has-children menu-item-512').find_all('a')
    links_cities = [link.get('href') for link in html_cities]
    result = get_data(links_cities[1::], session)
    with open('santaelena.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, sort_keys=False, ensure_ascii=False)
    logging.info('Successfully')


def get_data(links: list, session: requests):

    """" Get all locations from: https://www.santaelena.com"""
    result_cards = []
    for link in links:
        response = session.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        html_with_cards = soup.find('div', class_='elementor-section-wrap')
        # these html tags store information about the names of the institution
        html_names = html_with_cards.find_all('h3', class_='elementor-heading-title elementor-size-default')
        # these tags store information about the address, working time and phones of the institutions
        html_locations = html_with_cards.find_all('div', class_='elementor-text-editor elementor-clearfix')
        locations = []
        for loc in html_locations:
            if len(re.findall(r'<p>', str(loc))) < 2:
                continue
            locations.append(loc.text)
        names = [name.text for name in html_names]
        for i in range(len(names)):
            address = re.findall(r'(?=Dirección:|Dirección:\n)(.+?)(?=Teléfono|\n)', locations[i])
            working_hours = re.findall(r'Horario de atención:.(.+)', locations[i], re.DOTALL)
            result_cards.append({
                'name': names[i],
                'address': re.sub(r'(Dirección:|Dirección:\n)', '', ''.join(address)).strip(),
                'latlon': None,
                'phones': re.findall(r'\d{7}\s\D{3}\s\d{4}|\d{3}\s\d{3}\s\d{4}|\d{7,10}', locations[i]),
                'working_hours': working_hours[0].strip()
            })
    logging.info(f'{len(result_cards)} locations found')
    return result_cards

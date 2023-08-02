import json
import logging

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def dentalia():
    logging.info('Start parsing dentalia')
    session = requests.Session()
    response = session.get('https://dentalia.com/clinica/')
    soup = BeautifulSoup(response.text, 'lxml')
    # This json data storing IDs and coordinates of all clinics
    json_data = json.loads(soup.find('div', class_='jet-map-listing google-provider').get('data-markers'))
    result = get_data(json_data, session)
    with open('dentalia.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, sort_keys=False, ensure_ascii=False)
    logging.info('Successfully')


def get_data(json_id_latlon_clinics: dict, session: requests):
    result_cards = []
    for clinic in tqdm(json_id_latlon_clinics):
        # in this link put the id of the clinic
        link = 'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id={}&source=posts'.format(clinic['id'])
        response = session.get(url=link)
        json_data = json.loads(response.text)
        # get the html code with the clinic card
        html_response = json_data['html']
        soup = BeautifulSoup(html_response, 'lxml')
        # get information about the address, phone numbers and working hours
        info_clinic = soup.find_all('div', class_='jet-listing-dynamic-field__content')
        working_hours = info_clinic[1].text.split('\r\n')
        if working_hours[-1] == '':
            working_hours.remove('')
        result_cards.append(
            {
                'name': 'dentalia {}'.format(
                    soup.find('h3', class_='elementor-heading-title elementor-size-default').text
                ),
                'address': info_clinic[0].text,
                'latlon': [clinic['latLang']['lat'], clinic['latLang']['lng']],
                'phones': info_clinic[2].text.split('\r\n'),
                'working_hours': working_hours
            }
        )
    logging.info(f'{len(result_cards)} locations found')
    return result_cards

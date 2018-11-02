import requests
from flask import current_app


def __get_country_from_results(results):
    if 'results' in results:
        for address_component in results['results'][0]['address_components']:
            if 'country' in address_component['types']:
                return address_component['long_name']

    return None


def get_country(search_text):
    """Return the country of the search text based on Google Maps."""

    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': search_text,
        'language': 'en',
        'key': current_app.config.get('GOOGLE_API_KEY', '')
    }

    req = requests.get(GOOGLE_MAPS_API_URL, params=params, timeout=1).json()

    if 'status' in req:
        if req['status'].lower() == 'ok':
            return __get_country_from_results(req)

    return None
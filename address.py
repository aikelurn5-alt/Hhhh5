from bs4 import BeautifulSoup
import requests

def find_field(soup, label):
    for span in soup.find_all('span'):
        b_tag = span.find('b')
        if b_tag and label in b_tag.text:
            return span.text.replace(f'{label}:', '').strip()
    return None

def get_address(country_code):
    headers = {
        'authority': 'www.bestrandoms.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }
    params = {
        'quantity': '1',
    }
    
    try:
        response = requests.get(f'https://www.bestrandoms.com/random-address-in-{country_code}', params=params, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is 4xx or 5xx
    except requests.exceptions.RequestException as e:
        return f"Error fetching address: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    street = find_field(soup, 'Street')
    city = find_field(soup, 'City')
    state = find_field(soup, 'State/province/area')
    phone0 = find_field(soup, 'Phone number')
    zip_code = find_field(soup, 'Zip code')
    calling_code = find_field(soup, 'Country calling code')

    return f"Street: `{street}`\nCity: `{city}`\nState: `{state}`\nZip Code: `{zip_code}`\nCountry calling code: `{calling_code}`\nPhone: `{phone0}`"
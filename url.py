import asyncio
import aiohttp
import socket


async def analyze_website(url):
    result = {
        'url': url,
        'https': "HTTPS" if url.lower().startswith("https") else "Not HTTPS",
        'http_status': None,
        'cloudflare': "Not detected🟢",
        'captcha': "Not detected🟢",
        'payment_gateway': "Not detected",
        'ip': None
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                result['http_status'] = response.status

                # Check for Cloudflare
                if 'Server' in response.headers and 'cloudflare' in response.headers['Server'].lower():
                    result['cloudflare'] = "Cloudflare detected🔴"

                # Check for Captcha
                content = await response.text()
                content = content.lower()
                captcha_providers = ['www.google.com/recaptcha', 'hcaptcha.com', 'funcaptcha.com', 'geetest.com', 'captcha.com']
                if any(provider in content for provider in captcha_providers):
                    result['captcha'] = "Captcha detected🔴"

                # Check for Payment Gateways
                payment_gateways = {
    'Stripe': ['checkout.stripe.com', 'js.stripe.com', 'stripe.com', 'stripe.js', 'stripe.checkout'],
    'PayPal': [
        'paypal.com', 'paypalobjects.com', 'paypal-sdk', 'paypal-button', 'paypal.me', 
        'braintreepayments.com', 'venmo.com', 'www.paypal.com/sdk'
    ],
    'Square': [
        'squareup.com', 'square.com', 'square.js', 'connect.squareup.com', 'square-payment-form'
    ],
    'Authorize.Net': [
        'authorize.net', 'authorize.js', 'secure.authorize.net', 'accept.authorize.net', 
        'authorize-net.com', 'api.authorize.net'
    ],
    'Braintree': [
        'braintreegateway.com', 'braintree.js', 'assets.braintreegateway.com', 'client-token', 
        'paypal.braintreegateway.com', 'sandbox.braintreegateway.com'
    ],
    'Adyen': [
        'checkoutshopper-live.adyen.com', 'checkoutshopper-test.adyen.com', 'adyen.com', 
        'live.adyen.com', 'checkout.adyen.com', 'terminal-api-live.adyen.com'
    ],
    'Worldpay': [
        'online.worldpay.com', 'secure.worldpay.com', 'payments.worldpay.com', 
        'worldpay-us.com', 'access.worldpay.com', 'worldpay.us'
    ],
    '2Checkout': [
        '2checkout.com', '2co.com', 'api.2checkout.com', 'sandbox.2checkout.com', 
        'secure.2checkout.com', 'www.2checkout.com/checkout'
    ],
    'Alipay': [
        'alipay.com', 'intl.alipay.com', 'openapi.alipay.com', 'alipayobjects.com', 
        'checkout.alipay.com', 'alipayconnect.com'
    ],
    'WeChat Pay': [
        'wechat.com', 'pay.weixin.qq.com', 'wx.tenpay.com', 'wx.qq.com', 
        'api.mch.weixin.qq.com', 'wechatpay.com.cn'
    ],
    'Amazon Pay': [
        'pay.amazon.com', 'payments.amazon.com', 'amazonpay', 'amazon.com/a/wa', 
        'checkout.amazon.com', 'payments.amazon.eu'
    ],
    'Apple Pay': [
        'apple.com/apple-pay', 'applepay', 'apple-pay-gateway.apple.com', 
        'wallet.apple.com', 'applepay.com'
    ],
    'Google Pay': [
        'pay.google.com', 'googleapis.com/payments', 'google.com/pay', 
        'googlepay', 'google.com/intl/ALL_us/pay'
    ]
}

                for gateway, keywords in payment_gateways.items():
                    if any(keyword in content for keyword in keywords):
                        result['payment_gateway'] = f"{gateway}"
                        break

                # Resolve IP
                hostname = url.split("//")[-1].split("/")[0]
                result['ip'] = socket.gethostbyname(hostname)

    except asyncio.TimeoutError:
        result['http_status'] = "Timeout Error"
    except aiohttp.ClientError as e:
        result['http_status'] = f"HTTP Error: {e}"
    except socket.gaierror as e:
        result['ip'] = f"Error resolving IP: {e}"

    return result

async def check_url(url):
    if url:
        result = await analyze_website(url)
        return f"Result for {result['url']}\nPayment Gateway: {result['payment_gateway']}\nCloudflare: {result['cloudflare']}\nCaptcha: {result['captcha']}"


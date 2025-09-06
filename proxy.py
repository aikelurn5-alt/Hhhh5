import requests
from concurrent.futures import ThreadPoolExecutor

def check_proxy(proxy):
    """Checks if a single proxy is working."""
    try:
        proxies = {
            "http": proxy,
            "https": proxy
        }
       
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Working: {proxy}")
            return proxy  
    except Exception as e:
        print(f"Failed: {proxy} - {e}")
    return None

def main():
    with open("dd.txt", "r") as file:
        proxies = file.read().splitlines()
    working_proxies = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_proxy, proxies)

    working_proxies = [proxy for proxy in results if proxy]

    with open("working_proxies.txt", "w") as file:
        file.write("\n".join(working_proxies))

    print(f"Checked {len(proxies)} proxies, {len(working_proxies)} working proxies found.")

if __name__ == "__main__":
    main()
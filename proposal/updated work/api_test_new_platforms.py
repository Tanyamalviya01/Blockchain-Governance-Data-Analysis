import requests

blockchair_platforms = [
    ('Litecoin', 'https://api.blockchair.com/litecoin/blocks'),
    ('Dogecoin', 'https://api.blockchair.com/dogecoin/blocks'),
    ('Dash', 'https://api.blockchair.com/dash/blocks'),
    ('Bitcoin Cash', 'https://api.blockchair.com/bitcoin-cash/blocks'),
    ('Bitcoin SV', 'https://api.blockchair.com/bitcoin-sv/blocks'),
    ('Z-Cash', 'https://api.blockchair.com/zcash/blocks'),
    ('E-Cash', 'https://api.blockchair.com/ecash/blocks')
]

for name, url in blockchair_platforms:
    print(f"\nTesting {name} ({url})")
    try:
        r = requests.get(url, params={'limit': 1, 'fields': 'difficulty,time'})
        print(f"Status code: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"Sample data: {data['data'][:1]}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                print(f"Raw response: {r.text[:200]}")
        else:
            print(f"Non-200 status code. Response: {r.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

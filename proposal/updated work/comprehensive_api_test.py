import requests

def test_api(name, url, params=None, headers=None, parse_json=True, key_field='difficulty'):
    print(f"\nTesting {name} ({url})")
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        print(f"Status code: {r.status_code}")
        if r.status_code == 200:
            if parse_json:
                try:
                    data = r.json()
                    # Try to find the key_field in the response
                    found = False
                    def search(obj):
                        nonlocal found
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k == key_field:
                                    found = True
                                    print(f"  Found '{key_field}': {v}")
                                else:
                                    search(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                search(item)
                    search(data)
                    if not found:
                        print(f"  '{key_field}' not found in response.")
                    print("Sample keys:", list(data.keys()))
                    print("Sample response:", str(data)[:300])
                except Exception as e:
                    print(f"Error parsing JSON: {e}")
                    print("Raw response:", r.text[:300])
            else:
                print("Raw response:", r.text[:300])
        else:
            print("Non-200 status code. Response:", r.text[:300])
    except Exception as e:
        print(f"Exception: {e}")

print("==== Monero ====")
test_api("MoneroBlocks Info", "https://moneroblocks.info/api/get_stats", parse_json=True, key_field='difficulty')

print("\n==== Ethereum ====")
# Etherscan (using your API key)
etherscan_params = {
    'module': 'block',
    'action': 'getblocknobytime',
    'timestamp': '1622505600',  # Example: June 1, 2021
    'closest': 'before',
    'apikey': 'VB4HZP1PXX8CSW8MSXPG61T386IG98RTHP'
}
test_api("Etherscan Block by Time", "https://api.etherscan.io/api", params=etherscan_params, key_field='result')

# Ethplorer (public, limited)
test_api("Ethplorer Last Block", "https://api.ethplorer.io/getLastBlock", params={'apiKey': 'freekey'}, key_field='lastBlock')

print("\n==== E-Cash, Z-Cash, Litecoin, Dogecoin, Dash, Bitcoin Cash (Blockchair) ====")
blockchair_platforms = [
    ('E-Cash', 'https://api.blockchair.com/ecash/blocks'),
    ('Z-Cash', 'https://api.blockchair.com/zcash/blocks'),
    ('Litecoin', 'https://api.blockchair.com/litecoin/blocks'),
    ('Dogecoin', 'https://api.blockchair.com/dogecoin/blocks'),
    ('Dash', 'https://api.blockchair.com/dash/blocks'),
    ('Bitcoin Cash', 'https://api.blockchair.com/bitcoin-cash/blocks'),
]
for name, url in blockchair_platforms:
    test_api(f"Blockchair {name}", url, params={'limit': 1, 'fields': 'difficulty,time'}, key_field='difficulty')

print("\n==== Cardano ====")
# Blockfrost (using your API key)
blockfrost_headers = {"project_id": "mainnetES4hY7b89xtWplSnS8GNykcRtnnY4EoT"}
test_api("Blockfrost Cardano Latest Block", "https://cardano-mainnet.blockfrost.io/api/v0/blocks/latest", headers=blockfrost_headers, key_field='difficulty')

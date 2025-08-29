import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def safe_api_call(url, params=None, headers=None, parse_json=True, tries=3):
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=20)
            if r.status_code == 200:
                if parse_json:
                    return r.json()
                else:
                    return r.text
            else:
                print(f"HTTP {r.status_code} for {url} (params={params})")
                if r.status_code == 504:
                    print("504 Gateway Timeout: The server did not respond in time.")
                else:
                    print(f"Response: {r.text[:200]}")
        except Exception as e:
            print(f"Exception on {url}: {e}")
        if attempt < tries - 1:
            print("Retrying...")
            time.sleep(3)
    print(f"Failed to retrieve data from {url} after {tries} attempts.")
    return None

def get_bitcoin_difficulty():
    print("Collecting Bitcoin difficulty...")
    url = 'https://api.blockchain.info/charts/difficulty'
    params = {'timespan': '4years', 'format': 'json'}
    data = safe_api_call(url, params)
    if not data or 'values' not in data:
        print("Failed to collect Bitcoin difficulty data.")
        return pd.DataFrame()
    records = []
    for entry in data['values']:
        dt = datetime.utcfromtimestamp(entry['x'])
        year, week = dt.isocalendar()[0], dt.isocalendar()[1]
        records.append({'Platform': 'Bitcoin', 'date': dt, 'year': year, 'week': week, 'difficulty': entry['y']})
    return pd.DataFrame(records)

def get_blockchair_difficulty(platform_name, api_url):
    print(f"Collecting {platform_name} difficulty...")
    all_records = []
    for offset in range(0, 2100, 100):
        params = {'limit': 100, 'offset': offset, 'fields': 'difficulty,time'}
        data = safe_api_call(api_url, params)
        if not data or 'data' not in data:
            print(f"Failed to collect data for {platform_name} at offset {offset}.")
            continue
        for block in data['data']:
            try:
                dt = datetime.strptime(block['time'], '%Y-%m-%d %H:%M:%S')
                year, week = dt.isocalendar()[0], dt.isocalendar()[1]
                all_records.append({'Platform': platform_name, 'date': dt, 'year': year, 'week': week, 'difficulty': block['difficulty']})
            except Exception as e:
                print(f"Error parsing block for {platform_name}: {e}")
        time.sleep(1)
    if not all_records:
        print(f"No records collected for {platform_name}.")
        return pd.DataFrame()
    df = pd.DataFrame(all_records)
    df = df.groupby(['Platform', 'year', 'week']).agg({'date': 'first', 'difficulty': 'mean'}).reset_index()
    return df

def get_monero_difficulty():
    print("Collecting Monero difficulty...")
    url = "https://moneroblocks.info/api/get_stats"
    data = safe_api_call(url)
    if not data or 'difficulty' not in data:
        print("Failed to collect Monero difficulty data.")
        return pd.DataFrame()
    # Only current difficulty is available; historical requires block-by-block scraping (not feasible for free tier)
    now = datetime.utcnow()
    year, week = now.isocalendar()[0], now.isocalendar()[1]
    return pd.DataFrame([{
        'Platform': 'Monero',
        'date': now,
        'year': year,
        'week': week,
        'difficulty': data['difficulty']
    }])

def get_ethereum_difficulty(api_key):
    print("Collecting Ethereum difficulty (weekly, using Etherscan)...")
    url = "https://api.etherscan.io/api"
    # Collect for each Monday in the range
    start = datetime(2021, 1, 4)  # First Monday of 2021
    end = datetime(2024, 12, 31)
    records = []
    dt = start
    while dt <= end:
        timestamp = int(dt.timestamp())
        params = {
            'module': 'block',
            'action': 'getblocknobytime',
            'timestamp': str(timestamp),
            'closest': 'before',
            'apikey': api_key
        }
        data = safe_api_call(url, params)
        if data and data.get('status') == '1':
            block_number = data['result']
            # Now get block details
            params2 = {
                'module': 'proxy',
                'action': 'eth_getBlockByNumber',
                'tag': hex(int(block_number)),
                'boolean': 'true',
                'apikey': api_key
            }
            data2 = safe_api_call(url, params2)
            if data2 and 'result' in data2 and 'difficulty' in data2['result']:
                try:
                    difficulty = int(data2['result']['difficulty'], 16)
                except Exception:
                    difficulty = None
                records.append({
                    'Platform': 'Ethereum',
                    'date': dt,
                    'year': dt.year,
                    'week': dt.isocalendar()[1],
                    'difficulty': difficulty
                })
            else:
                print(f"Could not get block details for Ethereum at {dt.date()}")
        else:
            print(f"Could not get block number for Ethereum at {dt.date()}")
        dt += timedelta(weeks=1)
        time.sleep(0.5)
    return pd.DataFrame(records)

def main():
    # Replace with your Etherscan API key
    ETHERSCAN_API_KEY = "VB4HZP1PXX8CSW8MSXPG61T386IG98RTHP"

    dfs = []
    dfs.append(get_bitcoin_difficulty())
    blockchair_platforms = [
        ('Litecoin', 'https://api.blockchair.com/litecoin/blocks'),
        ('Dogecoin', 'https://api.blockchair.com/dogecoin/blocks'),
        ('Dash', 'https://api.blockchair.com/dash/blocks'),
        ('Bitcoin Cash', 'https://api.blockchair.com/bitcoin-cash/blocks'),
        ('Z-Cash', 'https://api.blockchair.com/zcash/blocks'),
        ('E-Cash', 'https://api.blockchair.com/ecash/blocks'),
    ]
    for name, url in blockchair_platforms:
        dfs.append(get_blockchair_difficulty(name, url))
    dfs.append(get_monero_difficulty())
    dfs.append(get_ethereum_difficulty(ETHERSCAN_API_KEY))

    df_all = pd.concat([df for df in dfs if not df.empty], ignore_index=True)
    df_all.to_excel('difficulty_data_full_2021_2024.xlsx', index=False)
    print("Saved: difficulty_data_full_2021_2024.xlsx")

if __name__ == "__main__":
    main()

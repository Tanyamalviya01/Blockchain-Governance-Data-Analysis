import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def get_bitcoin_difficulty():
    print("Collecting Bitcoin difficulty...")
    url = 'https://api.blockchain.info/charts/difficulty'
    params = {'timespan': '4years', 'format': 'json'}
    r = requests.get(url, params=params)
    data = r.json()['values']
    records = []
    for entry in data:
        dt = datetime.utcfromtimestamp(entry['x'])
        year, week = dt.isocalendar()[0], dt.isocalendar()[1]
        records.append({'Platform': 'Bitcoin', 'date': dt, 'year': year, 'week': week, 'difficulty': entry['y']})
    return pd.DataFrame(records)

def get_blockchair_difficulty(platform_name, api_url):
    print(f"Collecting {platform_name} difficulty...")
    all_records = []
    for offset in range(0, 2100, 100):
        params = {'limit': 100, 'offset': offset, 'fields': 'difficulty,time'}
        r = requests.get(api_url, params=params)
        data = r.json()['data']
        for block in data:
            dt = datetime.strptime(block['time'], '%Y-%m-%d %H:%M:%S')

            year, week = dt.isocalendar()[0], dt.isocalendar()[1]
            all_records.append({'Platform': platform_name, 'date': dt, 'year': year, 'week': week, 'difficulty': block['difficulty']})
        time.sleep(1)
    df = pd.DataFrame(all_records)
    df = df.groupby(['Platform', 'year', 'week']).agg({'date': 'first', 'difficulty': 'mean'}).reset_index()
    return df

def main():
    dfs = []
    dfs.append(get_bitcoin_difficulty())
    blockchair_platforms = [
        ('Litecoin', 'https://api.blockchair.com/litecoin/blocks'),
        ('Dogecoin', 'https://api.blockchair.com/dogecoin/blocks'),
        ('Dash', 'https://api.blockchair.com/dash/blocks'),
        ('Bitcoin Cash', 'https://api.blockchair.com/bitcoin-cash/blocks'),
        ('Bitcoin SV', 'https://api.blockchair.com/bitcoin-sv/blocks'),
    ]
    for name, url in blockchair_platforms:
        dfs.append(get_blockchair_difficulty(name, url))
    # Placeholder for Ethereum (requires Etherscan API key)
    dfs.append(pd.DataFrame(columns=['Platform', 'date', 'year', 'week', 'difficulty']))
    df_all = pd.concat(dfs, ignore_index=True)
    df_all.to_excel('difficulty_data_2021_2024.xlsx', index=False)
    print("Saved: difficulty_data_2021_2024.xlsx")

if __name__ == "__main__":
    main()

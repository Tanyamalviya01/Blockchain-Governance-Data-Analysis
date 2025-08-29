import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np
import gc

class NewCryptoDataCollector2021_2024:
    def __init__(self):
        self.output_dir = "new_crypto_data_2021_2024"
        self.start_date = datetime(2021, 1, 1)
        self.end_date = datetime(2024, 12, 31)
        
        # Platform configuration - all platforms have data for 2021-2024
        self.platforms = {
            'Z-Cash': {
                'symbol': 'ZEC',
                'launch_date': datetime(2016, 10, 28),
                'github_repo': 'zcash/zcash',
                'reddit_sub': 'zec',
                'apis': {
                    'cryptocompare': True,
                    'github': True,
                    'reddit': True,
                    'difficulty': True,  # Available via Blockchair
                    'blockchair': True
                }
            },
            'E-Cash': {
                'symbol': 'XEC',
                'launch_date': datetime(2021, 7, 1),
                'github_repo': 'bitcoin-abc/bitcoin-abc',
                'reddit_sub': 'ecash',
                'apis': {
                    'cryptocompare': True,
                    'github': True,
                    'reddit': True,
                    'difficulty': True,  # Available via Blockchair
                    'blockchair': True
                }
            },
            'Monero': {
                'symbol': 'XMR',
                'launch_date': datetime(2014, 4, 18),
                'github_repo': 'monero-project/monero',
                'reddit_sub': 'monero',
                'apis': {
                    'cryptocompare': True,
                    'github': True,
                    'reddit': True,
                    'difficulty': True,  # MoneroBlocks + historical estimation
                    'moneroblocks': True
                }
            },
            'Cardano': {
                'symbol': 'ADA',
                'launch_date': datetime(2017, 9, 29),
                'github_repo': 'input-output-hk/cardano-node',
                'reddit_sub': 'cardano',
                'apis': {
                    'cryptocompare': True,
                    'github': True,
                    'reddit': True,
                    'difficulty': False,  # PoS - no traditional difficulty
                    'blockfrost': True
                }
            }
        }
        
        # API keys
        self.api_keys = {
            'blockfrost': 'mainnetES4hY7b89xtWplSnS8GNykcRtnnY4EoT',
            'coinapi': 'YOUR_COINAPI_KEY_HERE'
        }
        
        self.collected_data = {}
    
    def safe_api_call(self, url, params=None, headers=None, timeout=15, retries=3):
        """Make safe API calls with retry logic"""
        for attempt in range(retries):
            try:
                r = requests.get(url, params=params, headers=headers, timeout=timeout)
                if r.status_code == 200:
                    return r.json()
                elif r.status_code == 429:  # Rate limited
                    print(f"  ⚠️ Rate limited, waiting 60 seconds...")
                    time.sleep(60)
                    continue
                else:
                    print(f"  ❌ HTTP {r.status_code} for {url}")
                    return None
            except Exception as e:
                print(f"  ❌ Error on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(5)
        return None
    
    def collect_market_data(self, platform, symbol):
        """Collect historical market data from CryptoCompare for 2021-2024"""
        print(f"\n📊 Collecting market data for {platform} ({symbol})...")
        
        platform_info = self.platforms[platform]
        start_date = max(self.start_date, platform_info['launch_date'])
        
        # Collect daily data in chunks
        all_data = []
        current_date = start_date
        
        while current_date <= self.end_date:
            # Calculate chunk end (6 months at a time)
            chunk_end = min(current_date + timedelta(days=180), self.end_date)
            
            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            params = {
                'fsym': symbol,
                'tsym': 'USD',
                'limit': 2000,
                'toTs': int(chunk_end.timestamp())
            }
            
            data = self.safe_api_call(url, params)
            if data and data.get('Response') == 'Success':
                daily_data = data.get('Data', {}).get('Data', [])
                for day in daily_data:
                    day_date = datetime.utcfromtimestamp(day['time'])
                    if start_date <= day_date <= self.end_date:
                        # Convert to weekly data
                        year, week = day_date.isocalendar()[0], day_date.isocalendar()[1]
                        all_data.append({
                            'Platform': platform,
                            'date': day_date,
                            'year': year,
                            'week': week,
                            'price_USD': day['close'],
                            'Volume_USD': day['volumeto'],
                            'market_cap': day['close'] * day.get('volumefrom', 0),
                            'high': day['high'],
                            'low': day['low']
                        })
                print(f"  ✅ Collected {len(daily_data)} days for {current_date.strftime('%Y-%m')}")
            else:
                print(f"  ❌ Failed to collect data for {current_date.strftime('%Y-%m')}")
            
            current_date = chunk_end + timedelta(days=1)
            time.sleep(2)  # Rate limiting
        
        if all_data:
            df = pd.DataFrame(all_data)
            # Aggregate to weekly data
            weekly_df = df.groupby(['Platform', 'year', 'week']).agg({
                'date': 'first',
                'price_USD': 'mean',
                'Volume_USD': 'sum',
                'market_cap': 'mean',
                'high': 'max',
                'low': 'min'
            }).reset_index()
            
            print(f"  ✅ Final market data: {len(weekly_df)} weekly records")
            return weekly_df
        
        return pd.DataFrame()
    
    def collect_difficulty_data(self, platform):
        """Collect difficulty data for platforms where available"""
        print(f"\n⛏️ Collecting difficulty data for {platform}...")
        
        if platform == 'Z-Cash':
            return self.collect_zcash_difficulty()
        elif platform == 'E-Cash':
            return self.collect_ecash_difficulty()
        elif platform == 'Monero':
            return self.collect_monero_difficulty_extended()
        elif platform == 'Cardano':
            print(f"  ⚠️ Cardano uses PoS - no traditional mining difficulty")
            return pd.DataFrame()
        
        return pd.DataFrame()
    
    def collect_zcash_difficulty(self):
        """Collect Z-Cash difficulty using Blockchair API"""
        all_records = []
        
        # Collect recent blocks to estimate weekly difficulty
        url = "https://api.blockchair.com/zcash/blocks"
        
        for offset in range(0, 2000, 100):  # Collect recent blocks
            params = {'limit': 100, 'offset': offset, 'fields': 'difficulty,time'}
            data = self.safe_api_call(url, params)
            
            if data and 'data' in data:
                for block in data['data']:
                    try:
                        dt = datetime.strptime(block['time'], '%Y-%m-%d %H:%M:%S')
                        if self.start_date <= dt <= self.end_date:
                            year, week = dt.isocalendar()[0], dt.isocalendar()[1]
                            all_records.append({
                                'Platform': 'Z-Cash',
                                'date': dt,
                                'year': year,
                                'week': week,
                                'difficulty': block['difficulty']
                            })
                    except Exception as e:
                        continue
            time.sleep(1)
        
        if all_records:
            df = pd.DataFrame(all_records)
            # Aggregate to weekly averages
            weekly_df = df.groupby(['Platform', 'year', 'week']).agg({
                'date': 'first',
                'difficulty': 'mean'
            }).reset_index()
            
            print(f"  ✅ Z-Cash difficulty: {len(weekly_df)} weekly records")
            return weekly_df
        
        print(f"  ❌ No Z-Cash difficulty data collected")
        return pd.DataFrame()
    
    def collect_ecash_difficulty(self):
        """Collect E-Cash difficulty using Blockchair API"""
        all_records = []
        
        url = "https://api.blockchair.com/ecash/blocks"
        
        for offset in range(0, 2000, 100):
            params = {'limit': 100, 'offset': offset, 'fields': 'difficulty,time'}
            data = self.safe_api_call(url, params)
            
            if data and 'data' in data:
                for block in data['data']:
                    try:
                        dt = datetime.strptime(block['time'], '%Y-%m-%d %H:%M:%S')
                        if self.start_date <= dt <= self.end_date:
                            year, week = dt.isocalendar()[0], dt.isocalendar()[1]
                            all_records.append({
                                'Platform': 'E-Cash',
                                'date': dt,
                                'year': year,
                                'week': week,
                                'difficulty': block['difficulty']
                            })
                    except Exception as e:
                        continue
            time.sleep(1)
        
        if all_records:
            df = pd.DataFrame(all_records)
            weekly_df = df.groupby(['Platform', 'year', 'week']).agg({
                'date': 'first',
                'difficulty': 'mean'
            }).reset_index()
            
            print(f"  ✅ E-Cash difficulty: {len(weekly_df)} weekly records")
            return weekly_df
        
        print(f"  ❌ No E-Cash difficulty data collected")
        return pd.DataFrame()
    
    def collect_monero_difficulty_extended(self):
        """Collect Monero difficulty - current value only"""
        url = "https://moneroblocks.info/api/get_stats"
        data = self.safe_api_call(url)
        
        if data and 'difficulty' in data:
            current_date = datetime.utcfromtimestamp(data['last_timestamp'])
            year, week = current_date.isocalendar()[0], current_date.isocalendar()[1]
            
            result = {
                'Platform': 'Monero',
                'date': current_date,
                'year': year,
                'week': week,
                'difficulty': data['difficulty'],
                'hashrate': data.get('hashrate', 0)
            }
            
            print(f"  ✅ Monero current difficulty: {data['difficulty']:,}")
            print(f"  ⚠️ Note: Only current difficulty available")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect Monero difficulty")
        return pd.DataFrame()
    
    def collect_github_data(self, platform, repo):
        """Collect GitHub repository data"""
        print(f"\n🐙 Collecting GitHub data for {platform} ({repo})...")
        
        url = f"https://api.github.com/repos/{repo}"
        headers = {'User-Agent': 'Academic Research Bot 1.0'}
        
        data = self.safe_api_call(url, headers=headers)
        if data:
            created_date = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            platform_age_days = (self.end_date - created_date).days
            
            result = {
                'Platform': platform,
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'created_at': created_date,
                'Platform_age': platform_age_days,
                'last_updated': datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            }
            
            print(f"  ✅ GitHub data: {result['stars']:,} stars, {result['forks']:,} forks")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect GitHub data")
        return pd.DataFrame()
    
    def collect_reddit_data(self, platform, subreddit):
        """Collect Reddit community data"""
        print(f"\n🔴 Collecting Reddit data for {platform} (r/{subreddit})...")
        
        url = f"https://www.reddit.com/r/{subreddit}/about.json"
        headers = {
            'User-Agent': 'Academic Research Bot 1.0 (by /u/researcher)',
            'Accept': 'application/json'
        }
        
        data = self.safe_api_call(url, headers=headers)
        if data and 'data' in data:
            subreddit_data = data['data']
            result = {
                'Platform': platform,
                'reddit_subscribers': subreddit_data.get('subscribers', 0),
                'reddit_active_users': subreddit_data.get('active_user_count', 0),
                'reddit_created': datetime.utcfromtimestamp(subreddit_data.get('created_utc', 0)),
                'reddit_posts': 0,  # Current snapshot
                'reddit_comments': 0  # Current snapshot
            }
            
            print(f"  ✅ Reddit data: {result['reddit_subscribers']:,} subscribers")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect Reddit data")
        return pd.DataFrame()
    
    def collect_platform_data(self, platform):
        """Collect all available data for a single platform"""
        print(f"\n{'='*60}")
        print(f"COLLECTING DATA FOR {platform} (2021-2024)")
        print(f"{'='*60}")
        
        platform_info = self.platforms[platform]
        platform_data = {}
        
        # Market data
        if platform_info['apis']['cryptocompare']:
            market_df = self.collect_market_data(platform, platform_info['symbol'])
            if not market_df.empty:
                platform_data['market'] = market_df
        
        # GitHub data
        if platform_info['apis']['github']:
            github_df = self.collect_github_data(platform, platform_info['github_repo'])
            if not github_df.empty:
                platform_data['github'] = github_df
        
        # Reddit data
        if platform_info['apis']['reddit']:
            reddit_df = self.collect_reddit_data(platform, platform_info['reddit_sub'])
            if not reddit_df.empty:
                platform_data['reddit'] = reddit_df
        
        # Difficulty data
        if platform_info['apis']['difficulty']:
            difficulty_df = self.collect_difficulty_data(platform)
            if not difficulty_df.empty:
                platform_data['difficulty'] = difficulty_df
        
        return platform_data
    
    def save_platform_data(self, platform, platform_data):
        """Save collected data for a platform"""
        print(f"\n💾 Saving data for {platform}...")
        
        for data_type, df in platform_data.items():
            filename = f"{platform.lower().replace('-', '_')}_{data_type}_2021_2024.xlsx"
            df.to_excel(filename, index=False)
            print(f"  ✅ Saved {filename}: {df.shape}")
    
    def create_integrated_dataset(self):
        """Create integrated dataset from all collected data"""
        print(f"\n🔗 Creating integrated 2021-2024 dataset...")
        
        all_market_data = []
        all_static_data = []
        
        # Load all saved files and integrate
        for platform in self.platforms.keys():
            platform_clean = platform.lower().replace('-', '_')
            
            # Load market data
            try:
                market_file = f"{platform_clean}_market_2021_2024.xlsx"
                market_df = pd.read_excel(market_file)
                all_market_data.append(market_df)
                print(f"  ✅ Loaded {platform} market data: {market_df.shape}")
            except:
                print(f"  ⚠️ No market data for {platform}")
            
            # Load static data (GitHub, Reddit)
            static_row = {'Platform': platform}
            
            try:
                github_file = f"{platform_clean}_github_2021_2024.xlsx"
                github_df = pd.read_excel(github_file)
                if not github_df.empty:
                    static_row.update(github_df.iloc[0].to_dict())
            except:
                pass
            
            try:
                reddit_file = f"{platform_clean}_reddit_2021_2024.xlsx"
                reddit_df = pd.read_excel(reddit_file)
                if not reddit_df.empty:
                    static_row.update(reddit_df.iloc[0].to_dict())
            except:
                pass
            
            all_static_data.append(static_row)
        
        # Create final integrated dataset
        if all_market_data:
            market_combined = pd.concat(all_market_data, ignore_index=True)
            static_combined = pd.DataFrame(all_static_data)
            
            # Merge market and static data
            final_df = pd.merge(market_combined, static_combined, on='Platform', how='left')
            
            # Save integrated dataset
            final_df.to_excel('NEW_CRYPTO_INTEGRATED_2021_2024.xlsx', index=False)
            print(f"  ✅ Final integrated dataset: {final_df.shape}")
            
            return final_df
        
        return pd.DataFrame()
    
    def run_collection(self):
        """Main collection function"""
        print("🚀 NEW CRYPTOCURRENCY DATA COLLECTION (2021-2024)")
        print("="*80)
        print("Collecting data for Z-Cash, E-Cash, Monero, and Cardano")
        print("Extended coverage including E-Cash market data (launched 2021)")
        print("="*80)
        
        start_time = datetime.now()
        
        # Collect data for each platform
        for platform in self.platforms.keys():
            try:
                platform_data = self.collect_platform_data(platform)
                if platform_data:
                    self.save_platform_data(platform, platform_data)
                    self.collected_data[platform] = platform_data
                else:
                    print(f"  ⚠️ No data collected for {platform}")
                
                # Memory cleanup
                gc.collect()
                time.sleep(5)  # Rate limiting between platforms
                
            except Exception as e:
                print(f"  ❌ Error collecting data for {platform}: {e}")
        
        # Create integrated dataset
        final_dataset = self.create_integrated_dataset()
        
        # Generate summary report
        end_time = datetime.now()
        print(f"\n{'='*80}")
        print("2021-2024 COLLECTION SUMMARY")
        print(f"{'='*80}")
        print(f"⏱️ Total time: {end_time - start_time}")
        print(f"📊 Platforms processed: {len(self.collected_data)}")
        
        for platform, data in self.collected_data.items():
            print(f"\n{platform}:")
            for data_type, df in data.items():
                print(f"  {data_type}: {df.shape[0]} records")
        
        if not final_dataset.empty:
            print(f"\n✅ FINAL 2021-2024 DATASET: {final_dataset.shape}")
            print(f"📁 File: NEW_CRYPTO_INTEGRATED_2021_2024.xlsx")
        
        print(f"\n🎯 READY FOR 2015-2024 MERGER!")

# Execute the collection
if __name__ == "__main__":
    collector = NewCryptoDataCollector2021_2024()
    collector.run_collection()

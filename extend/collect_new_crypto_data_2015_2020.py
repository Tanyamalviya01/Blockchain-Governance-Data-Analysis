import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np
import gc

class NewCryptoDataCollector2015_2020:
    def __init__(self):
        self.output_dir = "new_crypto_data_2015_2020"
        self.start_date = datetime(2015, 1, 1)
        self.end_date = datetime(2020, 12, 31)
        
        # Platform configuration based on API testing results
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
                    'blockchair': False,  # 404 errors
                    'difficulty': False   # No working API
                }
            },
            'E-Cash': {
                'symbol': 'XEC',
                'launch_date': datetime(2021, 7, 1),  # Launched after 2020
                'github_repo': 'bitcoin-abc/bitcoin-abc',
                'reddit_sub': 'ecash',
                'apis': {
                    'cryptocompare': True,
                    'github': True,
                    'reddit': True,
                    'blockchair': False,
                    'difficulty': False
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
                    'blockchair': True,   # Stats only
                    'difficulty': True,   # MoneroBlocks API
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
                    'blockchair': True,   # Stats only
                    'difficulty': True,   # Blockfrost API
                    'blockfrost': True
                }
            }
        }
        
        # API keys (replace with your actual keys)
        self.api_keys = {
            'blockfrost': 'mainnetES4hY7b89xtWplSnS8GNykcRtnnY4EoT',
            'coinapi': 'YOUR_COINAPI_KEY_HERE'  # Optional
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
        """Collect historical market data from CryptoCompare"""
        print(f"\n📊 Collecting market data for {platform} ({symbol})...")
        
        # Calculate date range based on platform launch
        platform_info = self.platforms[platform]
        start_date = max(self.start_date, platform_info['launch_date'])
        
        if start_date > self.end_date:
            print(f"  ⚠️ {platform} launched after 2020, skipping historical data")
            return pd.DataFrame()
        
        # Collect daily data in chunks to avoid rate limits
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
                            'market_cap': day['close'] * day.get('volumefrom', 0),  # Approximation
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
    
    def collect_github_data(self, platform, repo):
        """Collect GitHub repository data"""
        print(f"\n🐙 Collecting GitHub data for {platform} ({repo})...")
        
        url = f"https://api.github.com/repos/{repo}"
        headers = {'User-Agent': 'Academic Research Bot 1.0'}
        
        data = self.safe_api_call(url, headers=headers)
        if data:
            # Calculate platform age
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
                'reddit_posts': 0,  # Would need separate API calls for historical posts
                'reddit_comments': 0  # Would need separate API calls for historical comments
            }
            
            print(f"  ✅ Reddit data: {result['reddit_subscribers']:,} subscribers")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect Reddit data")
        return pd.DataFrame()
    
    def collect_monero_difficulty(self):
        """Collect Monero difficulty data using MoneroBlocks API"""
        print(f"\n⛏️ Collecting Monero difficulty data...")
        
        # MoneroBlocks only provides current data, not historical
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
                'hashrate': data.get('hashrate', 0),
                'height': data.get('height', 0)
            }
            
            print(f"  ✅ Monero current difficulty: {data['difficulty']:,}")
            print(f"  ⚠️ Note: Only current difficulty available, not 2015-2020 historical")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect Monero difficulty")
        return pd.DataFrame()
    
    def collect_cardano_data(self):
        """Collect Cardano data using Blockfrost API"""
        print(f"\n🔗 Collecting Cardano network data...")
        
        headers = {"project_id": self.api_keys['blockfrost']}
        
        # Get latest block info
        url = "https://cardano-mainnet.blockfrost.io/api/v0/blocks/latest"
        data = self.safe_api_call(url, headers=headers)
        
        if data:
            block_time = datetime.utcfromtimestamp(data['time'])
            year, week = block_time.isocalendar()[0], block_time.isocalendar()[1]
            
            result = {
                'Platform': 'Cardano',
                'date': block_time,
                'year': year,
                'week': week,
                'block_height': data.get('height', 0),
                'epoch': data.get('epoch', 0),
                'slot': data.get('slot', 0),
                'tx_count': data.get('tx_count', 0)
            }
            
            print(f"  ✅ Cardano latest block: {data.get('height', 0):,}")
            print(f"  ⚠️ Note: Only current block data available, not 2015-2020 historical")
            return pd.DataFrame([result])
        
        print(f"  ❌ Failed to collect Cardano data")
        return pd.DataFrame()
    
    def collect_platform_data(self, platform):
        """Collect all available data for a single platform"""
        print(f"\n{'='*60}")
        print(f"COLLECTING DATA FOR {platform}")
        print(f"{'='*60}")
        
        platform_info = self.platforms[platform]
        platform_data = {}
        
        # Market data (if available)
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
        
        # Platform-specific data
        if platform == 'Monero' and platform_info['apis']['difficulty']:
            difficulty_df = self.collect_monero_difficulty()
            if not difficulty_df.empty:
                platform_data['difficulty'] = difficulty_df
        
        if platform == 'Cardano' and platform_info['apis']['blockfrost']:
            cardano_df = self.collect_cardano_data()
            if not cardano_df.empty:
                platform_data['network'] = cardano_df
        
        return platform_data
    
    def save_platform_data(self, platform, platform_data):
        """Save collected data for a platform"""
        print(f"\n💾 Saving data for {platform}...")
        
        for data_type, df in platform_data.items():
            filename = f"{platform.lower().replace('-', '_')}_{data_type}_2015_2020.xlsx"
            df.to_excel(filename, index=False)
            print(f"  ✅ Saved {filename}: {df.shape}")
    
    def create_integrated_dataset(self):
        """Create integrated dataset from all collected data"""
        print(f"\n🔗 Creating integrated dataset...")
        
        all_market_data = []
        all_static_data = []
        
        # Load all saved files and integrate
        for platform in self.platforms.keys():
            platform_clean = platform.lower().replace('-', '_')
            
            # Load market data
            try:
                market_file = f"{platform_clean}_market_2015_2020.xlsx"
                market_df = pd.read_excel(market_file)
                all_market_data.append(market_df)
                print(f"  ✅ Loaded {platform} market data: {market_df.shape}")
            except:
                print(f"  ⚠️ No market data for {platform}")
            
            # Load static data (GitHub, Reddit)
            static_row = {'Platform': platform}
            
            try:
                github_file = f"{platform_clean}_github_2015_2020.xlsx"
                github_df = pd.read_excel(github_file)
                if not github_df.empty:
                    static_row.update(github_df.iloc[0].to_dict())
            except:
                pass
            
            try:
                reddit_file = f"{platform_clean}_reddit_2015_2020.xlsx"
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
            final_df.to_excel('NEW_CRYPTO_INTEGRATED_2015_2020.xlsx', index=False)
            print(f"  ✅ Final integrated dataset: {final_df.shape}")
            
            return final_df
        
        return pd.DataFrame()
    
    def run_collection(self):
        """Main collection function"""
        print("🚀 NEW CRYPTOCURRENCY DATA COLLECTION (2015-2020)")
        print("="*80)
        print("Collecting data for Z-Cash, E-Cash, Monero, and Cardano")
        print("Using working APIs identified in comprehensive testing")
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
        print("COLLECTION SUMMARY")
        print(f"{'='*80}")
        print(f"⏱️ Total time: {end_time - start_time}")
        print(f"📊 Platforms processed: {len(self.collected_data)}")
        
        for platform, data in self.collected_data.items():
            print(f"\n{platform}:")
            for data_type, df in data.items():
                print(f"  {data_type}: {df.shape[0]} records")
        
        if not final_dataset.empty:
            print(f"\n✅ FINAL INTEGRATED DATASET: {final_dataset.shape}")
            print(f"📁 File: NEW_CRYPTO_INTEGRATED_2015_2020.xlsx")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Review collected data for completeness")
        print(f"2. Validate data quality and ranges")
        print(f"3. Proceed with 2021-2024 collection phase")
        print(f"4. Integrate with existing 7-crypto dataset")

# Execute the collection
if __name__ == "__main__":
    collector = NewCryptoDataCollector2015_2020()
    collector.run_collection()

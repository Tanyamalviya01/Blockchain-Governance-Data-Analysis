import requests
import time
from datetime import datetime, timedelta
import json

class ComprehensiveNewCryptoAPITester:
    def __init__(self):
        self.output_file = "ENHANCED_CRYPTO_API_TEST_RESULTS.txt"
        
        # New platforms to test
        self.new_platforms = {
            'Z-Cash': {
                'symbol': 'ZEC',
                'launch_date': '2016-10-28',
                'consensus': 'PoW'
            },
            'E-Cash': {
                'symbol': 'XEC', 
                'launch_date': '2021-07-01',
                'consensus': 'PoW'
            },
            'Monero': {
                'symbol': 'XMR',
                'launch_date': '2014-04-18', 
                'consensus': 'PoW'
            },
            'Cardano': {
                'symbol': 'ADA',
                'launch_date': '2017-09-29',
                'consensus': 'PoS'
            }
        }
    
    def test_blockchair_apis(self):
        """Test Blockchair API for all supported new platforms"""
        results = {}
        
        blockchair_chains = {
            'Z-Cash': 'zcash',
            'E-Cash': 'ecash', 
            'Monero': 'monero',
            'Cardano': 'cardano'
        }
        
        for platform, chain in blockchair_chains.items():
            print(f"\nTesting Blockchair for {platform} ({chain})...")
            
            # Test basic stats
            stats_url = f"https://api.blockchair.com/{chain}/stats"
            try:
                r = requests.get(stats_url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    results[f"{platform}_blockchair_stats"] = {
                        'status': 'SUCCESS',
                        'endpoint': stats_url,
                        'sample_data': str(data)[:200]
                    }
                    print(f"  ✅ Stats API: Working")
                else:
                    results[f"{platform}_blockchair_stats"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ Stats API: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_blockchair_stats"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ Stats API: Error - {e}")
            
            # Test blocks endpoint for difficulty data
            blocks_url = f"https://api.blockchair.com/{chain}/blocks"
            try:
                r = requests.get(blocks_url, params={'limit': 1, 'fields': 'difficulty,time'}, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    if 'data' in data and len(data['data']) > 0:
                        results[f"{platform}_blockchair_blocks"] = {
                            'status': 'SUCCESS',
                            'endpoint': blocks_url,
                            'has_difficulty': 'difficulty' in data['data'][0],
                            'sample_data': str(data['data'][0])
                        }
                        print(f"  ✅ Blocks API: Working, Difficulty: {'Yes' if 'difficulty' in data['data'][0] else 'No'}")
                    else:
                        results[f"{platform}_blockchair_blocks"] = {
                            'status': 'NO_DATA',
                            'endpoint': blocks_url
                        }
                        print(f"  ⚠️  Blocks API: No data returned")
                else:
                    results[f"{platform}_blockchair_blocks"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ Blocks API: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_blockchair_blocks"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ Blocks API: Error - {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_monero_specific_apis(self):
        """Test Monero-specific APIs for difficulty data"""
        results = {}
        print(f"\nTesting Monero-specific APIs...")
        
        # Test MoneroBlocks API (already working from previous tests)
        try:
            url = "https://moneroblocks.info/api/get_stats"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['monero_moneroblocks'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'has_difficulty': 'difficulty' in data,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ MoneroBlocks: Working, Difficulty: {'Yes' if 'difficulty' in data else 'No'}")
            else:
                results['monero_moneroblocks'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ MoneroBlocks: Failed ({r.status_code})")
        except Exception as e:
            results['monero_moneroblocks'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ MoneroBlocks: Error - {e}")
        
        # Test XMRChain API
        try:
            url = "https://xmrchain.net/api/networkinfo"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # XMRChain might return plain text or JSON
                try:
                    data = r.json()
                    results['monero_xmrchain'] = {
                        'status': 'SUCCESS',
                        'endpoint': url,
                        'data_type': 'JSON',
                        'sample_data': str(data)[:200]
                    }
                    print(f"  ✅ XMRChain: Working (JSON response)")
                except:
                    results['monero_xmrchain'] = {
                        'status': 'SUCCESS',
                        'endpoint': url,
                        'data_type': 'TEXT',
                        'sample_data': r.text[:200]
                    }
                    print(f"  ✅ XMRChain: Working (Text response)")
            else:
                results['monero_xmrchain'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ XMRChain: Failed ({r.status_code})")
        except Exception as e:
            results['monero_xmrchain'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ XMRChain: Error - {e}")
        
        # Test Monero Node RPC (public nodes)
        try:
            url = "http://node.moneroworld.com:18089/json_rpc"
            payload = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_info"
            }
            headers = {'Content-Type': 'application/json'}
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['monero_node_rpc'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'method': 'get_info',
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ Monero Node RPC: Working")
            else:
                results['monero_node_rpc'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ Monero Node RPC: Failed ({r.status_code})")
        except Exception as e:
            results['monero_node_rpc'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ Monero Node RPC: Error - {e}")
        
        time.sleep(2)
        return results
    
    def test_cardano_alternative_apis(self):
        """Test alternative Cardano APIs"""
        results = {}
        print(f"\nTesting Cardano alternative APIs...")
        
        # Test Blockfrost with your API key
        try:
            url = "https://cardano-mainnet.blockfrost.io/api/v0/blocks/latest"
            headers = {"project_id": "mainnetES4hY7b89xtWplSnS8GNykcRtnnY4EoT"}
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['cardano_blockfrost'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ Blockfrost: Working with API key")
            elif r.status_code == 403:
                results['cardano_blockfrost'] = {
                    'status': 'NEEDS_VALID_KEY',
                    'error': 'Invalid or expired API key'
                }
                print(f"  ⚠️  Blockfrost: Need valid API key")
            else:
                results['cardano_blockfrost'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ Blockfrost: Failed ({r.status_code})")
        except Exception as e:
            results['cardano_blockfrost'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ Blockfrost: Error - {e}")
        
        # Test Koios API (no key required)
        try:
            url = "https://api.koios.rest/api/v0/tip"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['cardano_koios'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ Koios: Working")
            else:
                results['cardano_koios'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ Koios: Failed ({r.status_code})")
        except Exception as e:
            results['cardano_koios'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ Koios: Error - {e}")
        
        # Test CardanoScan API
        try:
            url = "https://api.cardanoscan.io/api/v1/blocks/latest"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['cardano_cardanoscan'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ CardanoScan: Working")
            else:
                results['cardano_cardanoscan'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ CardanoScan: Failed ({r.status_code})")
        except Exception as e:
            results['cardano_cardanoscan'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ CardanoScan: Error - {e}")
        
        time.sleep(2)
        return results
    
    def test_zcash_alternative_apis(self):
        """Test Z-Cash specific APIs"""
        results = {}
        print(f"\nTesting Z-Cash alternative APIs...")
        
        # Test ZCha.in API
        try:
            url = "https://api.zcha.in/v2/mainnet/network"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['zcash_zchain'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ ZCha.in: Working")
            else:
                results['zcash_zchain'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ ZCha.in: Failed ({r.status_code})")
        except Exception as e:
            results['zcash_zchain'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ ZCha.in: Error - {e}")
        
        # Test Insight API for ZCash
        try:
            url = "https://zcashnetwork.info/api/status"
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results['zcash_insight'] = {
                    'status': 'SUCCESS',
                    'endpoint': url,
                    'sample_data': str(data)[:200]
                }
                print(f"  ✅ ZCash Insight: Working")
            else:
                results['zcash_insight'] = {
                    'status': 'FAILED',
                    'error': f"HTTP {r.status_code}"
                }
                print(f"  ❌ ZCash Insight: Failed ({r.status_code})")
        except Exception as e:
            results['zcash_insight'] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ ZCash Insight: Error - {e}")
        
        time.sleep(1)
        return results
    
    def test_cryptocompare_apis(self):
        """Test CryptoCompare API for historical data"""
        results = {}
        
        for platform, info in self.new_platforms.items():
            symbol = info['symbol']
            print(f"\nTesting CryptoCompare for {platform} ({symbol})...")
            
            # Test historical daily data
            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            params = {
                'fsym': symbol,
                'tsym': 'USD',
                'limit': 10,
                'toTs': int(datetime(2020, 1, 1).timestamp())
            }
            
            try:
                r = requests.get(url, params=params, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('Response') == 'Success':
                        results[f"{platform}_cryptocompare"] = {
                            'status': 'SUCCESS',
                            'endpoint': url,
                            'data_points': len(data.get('Data', {}).get('Data', [])),
                            'sample_data': str(data.get('Data', {}).get('Data', [])[:1])
                        }
                        print(f"  ✅ CryptoCompare: Working, {len(data.get('Data', {}).get('Data', []))} data points")
                    else:
                        results[f"{platform}_cryptocompare"] = {
                            'status': 'NO_DATA',
                            'response': data.get('Message', 'Unknown error')
                        }
                        print(f"  ⚠️  CryptoCompare: {data.get('Message', 'No data')}")
                else:
                    results[f"{platform}_cryptocompare"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ CryptoCompare: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_cryptocompare"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ CryptoCompare: Error - {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_coinapi_alternatives(self):
        """Test CoinAPI and other market data APIs"""
        results = {}
        print(f"\nTesting CoinAPI and market data alternatives...")
        
        for platform, info in self.new_platforms.items():
            symbol = info['symbol']
            
            # Test CoinAPI (free tier)
            try:
                url = f"https://rest.coinapi.io/v1/exchangerate/{symbol}/USD"
                headers = {'X-CoinAPI-Key': '1d20d6ab-8dca-4783-8801-1aca62e4b38f'}  # User needs to get free key
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    results[f"{platform}_coinapi"] = {
                        'status': 'SUCCESS',
                        'endpoint': url,
                        'sample_data': str(data)[:200]
                    }
                    print(f"  ✅ CoinAPI {platform}: Working")
                elif r.status_code == 401:
                    results[f"{platform}_coinapi"] = {
                        'status': 'NEEDS_API_KEY',
                        'note': 'Requires free API key from coinapi.io'
                    }
                    print(f"  ⚠️  CoinAPI {platform}: Needs API key")
                else:
                    results[f"{platform}_coinapi"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ CoinAPI {platform}: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_coinapi"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ CoinAPI {platform}: Error - {e}")
            
            time.sleep(0.5)
        
        return results
    
    def test_github_apis(self):
        """Test GitHub API for repository data"""
        results = {}
        
        github_repos = {
            'Z-Cash': 'zcash/zcash',
            'E-Cash': 'bitcoin-abc/bitcoin-abc',
            'Monero': 'monero-project/monero', 
            'Cardano': 'input-output-hk/cardano-node'
        }
        
        for platform, repo in github_repos.items():
            print(f"\nTesting GitHub for {platform} ({repo})...")
            
            url = f"https://api.github.com/repos/{repo}"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'}
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    results[f"{platform}_github"] = {
                        'status': 'SUCCESS',
                        'stars': data.get('stargazers_count'),
                        'forks': data.get('forks_count'),
                        'created_at': data.get('created_at'),
                        'updated_at': data.get('updated_at')
                    }
                    print(f"  ✅ GitHub: Working, Stars: {data.get('stargazers_count'):,}, Forks: {data.get('forks_count'):,}")
                else:
                    results[f"{platform}_github"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ GitHub: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_github"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ GitHub: Error - {e}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def test_reddit_alternatives(self):
        """Test Reddit API with better rate limiting and alternatives"""
        results = {}
        
        reddit_subs = {
            'Z-Cash': 'zec',
            'E-Cash': 'ecash',
            'Monero': 'monero',
            'Cardano': 'cardano'
        }
        
        for platform, subreddit in reddit_subs.items():
            print(f"\nTesting Reddit for {platform} (r/{subreddit})...")
            
            # Try with different user agents and longer delays
            url = f"https://www.reddit.com/r/{subreddit}/about.json"
            headers = {
                'User-Agent': 'Academic Research Bot 1.0 (by /u/researcher)',
                'Accept': 'application/json'
            }
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    subreddit_data = data.get('data', {})
                    results[f"{platform}_reddit"] = {
                        'status': 'SUCCESS',
                        'subscribers': subreddit_data.get('subscribers'),
                        'active_users': subreddit_data.get('active_user_count'),
                        'created_utc': subreddit_data.get('created_utc')
                    }
                    print(f"  ✅ Reddit: Working, Subscribers: {subreddit_data.get('subscribers'):,}")
                elif r.status_code == 403:
                    results[f"{platform}_reddit"] = {
                        'status': 'RATE_LIMITED',
                        'error': 'Reddit API rate limited or blocked'
                    }
                    print(f"  ⚠️  Reddit: Rate limited (403)")
                else:
                    results[f"{platform}_reddit"] = {
                        'status': 'FAILED',
                        'error': f"HTTP {r.status_code}"
                    }
                    print(f"  ❌ Reddit: Failed ({r.status_code})")
            except Exception as e:
                results[f"{platform}_reddit"] = {
                    'status': 'ERROR',
                    'error': str(e)
                }
                print(f"  ❌ Reddit: Error - {e}")
            
            time.sleep(3)  # Longer delay for Reddit
        
        return results
    
    def generate_comprehensive_report(self):
        """Generate comprehensive API testing report"""
        print("🔍 ENHANCED COMPREHENSIVE NEW CRYPTO API TESTING")
        print("="*80)
        print("Testing APIs for Z-Cash, E-Cash, Monero, and Cardano")
        print("Focus: 2015-2020 data collection with multiple alternatives")
        print("="*80)
        
        all_results = {}
        
        # Test all API categories including new alternatives
        all_results.update(self.test_blockchair_apis())
        all_results.update(self.test_cryptocompare_apis())
        all_results.update(self.test_github_apis())
        all_results.update(self.test_reddit_alternatives())
        all_results.update(self.test_monero_specific_apis())
        all_results.update(self.test_cardano_alternative_apis())
        all_results.update(self.test_zcash_alternative_apis())
        all_results.update(self.test_coinapi_alternatives())
        
        # Save results to file
        with open(self.output_file, 'w') as f:
            f.write("ENHANCED COMPREHENSIVE NEW CRYPTO API TEST RESULTS\n")
            f.write("="*80 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Platforms tested: Z-Cash, E-Cash, Monero, Cardano\n")
            f.write(f"Focus: 2015-2020 historical data collection with alternatives\n\n")
            
            # Organize results by platform
            for platform in self.new_platforms.keys():
                f.write(f"\n{'='*60}\n")
                f.write(f"PLATFORM: {platform}\n")
                f.write(f"{'='*60}\n")
                
                platform_results = {k: v for k, v in all_results.items() if platform.replace('-', '').lower() in k.lower()}
                
                for test_name, result in platform_results.items():
                    f.write(f"\n{test_name}:\n")
                    f.write(f"  Status: {result.get('status', 'Unknown')}\n")
                    for key, value in result.items():
                        if key != 'status':
                            f.write(f"  {key}: {value}\n")
            
            # Platform-specific alternative APIs
            f.write(f"\n{'='*60}\n")
            f.write("PLATFORM-SPECIFIC ALTERNATIVE APIS\n")
            f.write(f"{'='*60}\n")
            
            # Monero alternatives
            monero_results = {k: v for k, v in all_results.items() if 'monero' in k.lower()}
            f.write(f"\nMONERO ALTERNATIVES:\n")
            for test_name, result in monero_results.items():
                f.write(f"  {test_name}: {result.get('status', 'Unknown')}\n")
            
            # Cardano alternatives
            cardano_results = {k: v for k, v in all_results.items() if 'cardano' in k.lower()}
            f.write(f"\nCARDANO ALTERNATIVES:\n")
            for test_name, result in cardano_results.items():
                f.write(f"  {test_name}: {result.get('status', 'Unknown')}\n")
            
            # Z-Cash alternatives
            zcash_results = {k: v for k, v in all_results.items() if 'zcash' in k.lower()}
            f.write(f"\nZ-CASH ALTERNATIVES:\n")
            for test_name, result in zcash_results.items():
                f.write(f"  {test_name}: {result.get('status', 'Unknown')}\n")
            
            # Summary recommendations
            f.write(f"\n{'='*80}\n")
            f.write("ENHANCED RECOMMENDATIONS FOR 2015-2020 DATA COLLECTION\n")
            f.write(f"{'='*80}\n")
            
            working_apis = [k for k, v in all_results.items() if v.get('status') == 'SUCCESS']
            needs_key_apis = [k for k, v in all_results.items() if v.get('status') in ['NEEDS_API_KEY', 'NEEDS_VALID_KEY']]
            failed_apis = [k for k, v in all_results.items() if v.get('status') in ['FAILED', 'ERROR', 'RATE_LIMITED']]
            
            f.write(f"Working APIs: {len(working_apis)}\n")
            f.write(f"APIs requiring keys: {len(needs_key_apis)}\n")
            f.write(f"Failed/Limited APIs: {len(failed_apis)}\n")
            
            f.write(f"\nPRIORITY ACTIONS:\n")
            f.write(f"1. Use working APIs for immediate data collection\n")
            f.write(f"2. Register for free API keys: Blockfrost (Cardano), CoinAPI\n")
            f.write(f"3. For Monero: Use MoneroBlocks or XMRChain as Blockchair alternative\n")
            f.write(f"4. For Cardano: Use Blockfrost or Koios as Blockchair alternative\n")
            f.write(f"5. For Reddit: Implement longer delays and better user agents\n")
            f.write(f"6. Start with platforms having most working endpoints\n")
        
        print(f"\n✅ ENHANCED API TESTING COMPLETE!")
        print(f"📁 Detailed report saved to: {self.output_file}")
        print(f"🔍 Found {len(working_apis)} working API endpoints")
        print(f"🔑 Found {len(needs_key_apis)} APIs requiring free registration")
        print(f"⚠️  {len(failed_apis)} APIs need alternatives or troubleshooting")
        
        return all_results

# Execute the enhanced comprehensive testing
if __name__ == "__main__":
    tester = ComprehensiveNewCryptoAPITester()
    results = tester.generate_comprehensive_report()

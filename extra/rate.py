import requests
import json

def test_api_endpoints():
    """Test various crypto APIs to see which ones work"""
    
    endpoints = {
        'CoinGecko Bitcoin': 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true',
        'CoinGecko Ethereum': 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_market_cap=true',
        'CryptoCompare BTC': 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD',
        'CryptoCompare ETH': 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD',
        'Blockchain.info Hashrate': 'https://api.blockchain.info/charts/hash-rate?timespan=1year&format=json',
        'Blockchair Bitcoin': 'https://api.blockchair.com/bitcoin/stats'
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            print(f"Testing {name}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS: {name}")
                print(f"     Status: {response.status_code}")
                print(f"     Sample data: {str(data)[:100]}...")
                results[name] = {'status': 'success', 'data': data}
            else:
                print(f"  ❌ FAILED: {name} - Status: {response.status_code}")
                results[name] = {'status': 'failed', 'code': response.status_code}
                
        except Exception as e:
            print(f"  ❌ ERROR: {name} - {str(e)}")
            results[name] = {'status': 'error', 'error': str(e)}
        
        print()
    
    return results

if __name__ == "__main__":
    print("=== TESTING CRYPTOCURRENCY APIs ===")
    print("Checking which APIs are accessible from your network...\n")
    
    test_results = test_api_endpoints()
    
    print("=== SUMMARY ===")
    working_apis = [name for name, result in test_results.items() if result['status'] == 'success']
    failed_apis = [name for name, result in test_results.items() if result['status'] != 'success']
    
    print(f"✅ Working APIs ({len(working_apis)}):")
    for api in working_apis:
        print(f"   - {api}")
    
    print(f"\n❌ Failed APIs ({len(failed_apis)}):")
    for api in failed_apis:
        print(f"   - {api}")
    
    if working_apis:
        print(f"\n🎉 Great! {len(working_apis)} APIs are working. We can collect real data!")
    else:
        print(f"\n😞 No APIs are working. We'll need to use realistic estimates.")

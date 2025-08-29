import requests
import time
from datetime import datetime, timedelta

def test_cardano_apis():
    """Test multiple Cardano APIs"""
    apis = {
        # Free APIs that don't require auth
        'Cardano Explorer': 'https://explorer.cardano.org/api/blocks/latest',
        'Cardano Koios': 'https://api.koios.rest/api/v1/tip',
        'Cardano Maestro': 'https://mainnet.gomaestro.org/v1/general/info',
        'Cardano Cutymals': 'https://mainnet.cutymals.com/api/CardanoSyncStatus',
        'Blockchair Cardano': 'https://api.blockchair.com/cardano/stats'
    }
    
    working_apis = []
    for name, url in apis.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                working_apis.append((name, url, "✅ Working"))
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    return working_apis

def test_zcash_apis():
    """Test multiple Zcash APIs"""
    apis = {
        'Blockchair Zcash Blocks': 'https://api.blockchair.com/zcash/blocks',
        'Blockchair Zcash Stats': 'https://api.blockchair.com/zcash/stats', 
        'ZChain Explorer': 'https://api.zcha.in/v2/mainnet/blocks',
        'Tatum Zcash': 'https://api.tatum.io/v3/zcash/info',
        'CryptoID Zcash': 'https://chainz.cryptoid.info/zec/api.dws?q=getblockcount'
    }
    
    working_apis = []
    for name, url in apis.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                working_apis.append((name, url, "✅ Working"))
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    return working_apis

def test_monero_apis():
    """Test multiple Monero APIs"""
    apis = {
        'MoneroBlocks Stats': 'https://moneroblocks.info/api/get_stats',
        'MoneroBlocks Latest': 'https://moneroblocks.info/api/get_block_header/latest',
        'BlockSDK Monero': 'https://api.blocksdk.com/v2/xmr/info',
        'CryptoID Monero': 'https://chainz.cryptoid.info/xmr/api.dws?q=getblockcount',
        'Monero Daemon RPC': 'http://node.xmr.to:18089/get_info'
    }
    
    working_apis = []
    for name, url in apis.items():
        try:
            if 'json_rpc' in url or 'get_info' in url:
                # For RPC endpoints, use POST
                response = requests.post(url, json={"jsonrpc":"2.0","id":"0","method":"get_info"}, timeout=10)
            else:
                response = requests.get(url, timeout=10)
                
            if response.status_code == 200:
                working_apis.append((name, url, "✅ Working"))
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    return working_apis

def test_stellar_apis():
    """Test multiple Stellar APIs"""
    apis = {
        'Stellar Horizon': 'https://horizon.stellar.org/ledgers?limit=1&order=desc',
        'Stellar Expert': 'https://api.stellar.expert/explorer/public/ledger/latest',
        'StellarChain': 'https://stellarchain.io/api/ledgers/latest',
        'CryptoID Stellar': 'https://chainz.cryptoid.info/xlm/api.dws?q=getblockcount',
        'Stellar Beatify': 'https://api.stellarbeat.io/v1/nodes'
    }
    
    working_apis = []
    for name, url in apis.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                working_apis.append((name, url, "✅ Working"))
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    return working_apis

def test_github_proposals():
    """Test GitHub APIs for proposal data with proper rate limiting"""
    # Using alternative methods to avoid rate limiting
    proposal_sources = {
        'Cardano CIPs Raw': 'https://raw.githubusercontent.com/cardano-foundation/CIPs/master/README.md',
        'Zcash ZIPs Raw': 'https://raw.githubusercontent.com/zcash/zips/master/README.rst',
        'Monero CCS Raw': 'https://raw.githubusercontent.com/monero-project/ccs-proposals/master/README.md',
        'Stellar CAPs Raw': 'https://raw.githubusercontent.com/stellar/stellar-protocol/master/README.md'
    }
    
    working_sources = []
    for name, url in proposal_sources.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                working_sources.append((name, url, "✅ Working"))
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    return working_sources

def main():
    print("🔬 Testing Multiple APIs for Extended Crypto Data Collection...")
    print("=" * 80)
    
    all_working_apis = {}
    
    print("\n📦 Testing Cardano APIs...")
    cardano_apis = test_cardano_apis()
    all_working_apis['Cardano'] = cardano_apis
    
    print("\n💰 Testing Zcash APIs...")
    zcash_apis = test_zcash_apis()
    all_working_apis['Zcash'] = zcash_apis
    
    print("\n🔒 Testing Monero APIs...")
    monero_apis = test_monero_apis()
    all_working_apis['Monero'] = monero_apis
    
    print("\n⭐ Testing Stellar APIs...")
    stellar_apis = test_stellar_apis()
    all_working_apis['Stellar'] = stellar_apis
    
    print("\n📋 Testing GitHub Proposal Sources...")
    proposal_sources = test_github_proposals()
    all_working_apis['Proposals'] = proposal_sources
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY OF WORKING APIs:")
    print("=" * 80)
    
    for platform, apis in all_working_apis.items():
        working_count = len(apis)
        print(f"\n{platform}: {working_count} working APIs")
        for name, url, status in apis:
            print(f"  {status} {name}")
            print(f"    URL: {url}")
    
    return all_working_apis

if __name__ == "__main__":
    working_apis = main()

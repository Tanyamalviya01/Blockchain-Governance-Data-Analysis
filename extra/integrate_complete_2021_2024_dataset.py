import pandas as pd
import numpy as np
import gc
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class Complete2021_2024DatasetIntegrator:
    def __init__(self):
        print("🚀 COMPLETE 2021-2024 DATASET INTEGRATION")
        print("="*80)
        print("Integrating all blockchain governance data for 2021-2024")
        print("Addressing platform naming issues and memory optimization")
        print("="*80)
        
        # Platform name standardization mapping
        self.platform_mapping = {
            'Bitcoin ': 'Bitcoin',
            'Bitcoin Cash': 'Bitcoin Cash',
            'Bitcoin SV': 'Bitcoin SV', 
            'BitcoinCash': 'Bitcoin Cash',
            'BitcoinSV': 'Bitcoin SV',
            'Bitcoin_Cash': 'Bitcoin Cash',
            'Bitcoin_SV': 'Bitcoin SV',
            'Ethereum_Go': 'Ethereum',
            'Z-Cash': 'Z-Cash',
            'E-Cash': 'E-Cash',
            'Monero': 'Monero'
        }
        
        # Target platforms for 2021-2024 dataset
        self.target_platforms = [
            'Bitcoin', 'Ethereum', 'Litecoin', 'Dogecoin', 
            'Dash', 'Bitcoin Cash', 'Bitcoin SV'
        ]
        
        self.results = {}
    
    def standardize_platform_names(self, df, platform_col='Platform'):
        """Standardize platform names across all datasets"""
        if platform_col in df.columns:
            # Remove any NaN or empty string platforms
            df = df.dropna(subset=[platform_col])
            df = df[df[platform_col].str.strip() != '']
            
            # Apply platform name mapping
            df[platform_col] = df[platform_col].replace(self.platform_mapping)
            
            # Filter for target platforms only
            df = df[df[platform_col].isin(self.target_platforms)]
        
        return df
    
    def optimize_memory(self, df, name):
        """Optimize dataframe memory usage"""
        print(f"  🔧 Optimizing {name} memory...")
        original_memory = df.memory_usage(deep=True).sum() / 1024**2
        
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = pd.to_numeric(df[col], downcast='float')
            elif df[col].dtype == 'int64':
                df[col] = pd.to_numeric(df[col], downcast='integer')
            elif df[col].dtype == 'object':
                if df[col].nunique() / len(df) < 0.5:
                    try:
                        df[col] = df[col].astype('category')
                    except:
                        pass
        
        optimized_memory = df.memory_usage(deep=True).sum() / 1024**2
        saved = original_memory - optimized_memory
        print(f"    💾 Memory saved: {saved:.1f} MB")
        
        return df
    
    def load_and_process_decentralization_data(self):
        """Load decentralization metrics (Block_HHI, Block_Shannon, Commit_HHI, Commit_Shannon)"""
        print("\n📊 Loading decentralization metrics...")
        
        try:
            df = pd.read_excel('commits/blockchain_decentralization_metrics_weekly_2021_2024_fixed.xlsx')
            df = self.standardize_platform_names(df)
            df = self.optimize_memory(df, 'decentralization')
            
            # Rename columns to match expected format
            column_mapping = {
                'Year': 'year',
                'Week': 'week',
                'Block_Inverse_HHI': 'Block_HHI',
                'Block_Shannon_Entropy': 'Block_Shannon',
                'Commit_Inverse_HHI': 'Commit_HHI', 
                'Commit_Shannon_Entropy': 'Commit_Shannon'
            }
            df = df.rename(columns=column_mapping)
            
            print(f"  ✅ Decentralization data: {df.shape}")
            return df
            
        except Exception as e:
            print(f"  ❌ Error loading decentralization data: {e}")
            return pd.DataFrame()
    
    def load_and_process_market_data(self):
        """Load market capitalization and hashrate data"""
        print("\n📊 Loading market & hashrate data...")
        
        try:
            df = pd.read_excel('commits/blockchain_market_hashrate_weekly_2021_2024.xlsx')
            df = self.standardize_platform_names(df)
            df = self.optimize_memory(df, 'market')
            
            # Rename columns to match expected format
            column_mapping = {
                'Year': 'year',
                'Week': 'week',
                'Market_Capitalization': 'market_cap',
                'Hash_Rate': 'hashrate'
            }
            df = df.rename(columns=column_mapping)
            
            print(f"  ✅ Market data: {df.shape}")
            return df
            
        except Exception as e:
            print(f"  ❌ Error loading market data: {e}")
            return pd.DataFrame()
    
    def load_and_process_proposal_data(self):
        """Load proposal topic diversity data"""
        print("\n📊 Loading proposal data...")
        
        try:
            df = pd.read_excel('proposal/proposal_topic_diversity_weekly.xlsx')
            df = self.standardize_platform_names(df)
            df = self.optimize_memory(df, 'proposals')
            
            # Rename columns to match expected format
            column_mapping = {
                'Year': 'year',
                'Week': 'week'
            }
            df = df.rename(columns=column_mapping)
            
            print(f"  ✅ Proposal data: {df.shape}")
            return df
            
        except Exception as e:
            print(f"  ❌ Error loading proposal data: {e}")
            return pd.DataFrame()
    
    def load_and_process_api_data(self):
        """Load API data (CryptoCompare, GitHub, Reddit)"""
        print("\n📊 Loading API data...")
        
        api_data = {}
        
        # CryptoCompare data (time-series)
        try:
            df_crypto = pd.read_excel('proposal/updated work/cryptocompare_timeseries_2021_2024.xlsx')
            df_crypto = self.standardize_platform_names(df_crypto)
            df_crypto = self.optimize_memory(df_crypto, 'cryptocompare')
            api_data['cryptocompare'] = df_crypto
            print(f"  ✅ CryptoCompare data: {df_crypto.shape}")
        except Exception as e:
            print(f"  ❌ Error loading CryptoCompare data: {e}")
        
        # GitHub data (static)
        try:
            df_github = pd.read_excel('proposal/updated work/task3_github_checkpoint.xlsx')
            df_github = self.standardize_platform_names(df_github)
            api_data['github'] = df_github
            print(f"  ✅ GitHub data: {df_github.shape}")
        except Exception as e:
            print(f"  ❌ Error loading GitHub data: {e}")
        
        # Reddit data (static)
        try:
            df_reddit = pd.read_excel('proposal/updated work/task3_reddit_checkpoint.xlsx')
            df_reddit = self.standardize_platform_names(df_reddit)
            api_data['reddit'] = df_reddit
            print(f"  ✅ Reddit data: {df_reddit.shape}")
        except Exception as e:
            print(f"  ❌ Error loading Reddit data: {e}")
        
        return api_data
    
    def load_and_process_difficulty_data(self):
        """Load difficulty data with Bitcoin SV handling"""
        print("\n📊 Loading difficulty data...")
        
        try:
            df = pd.read_excel('proposal/updated work/difficulty_data_full_2021_2024.xlsx')
            df = self.standardize_platform_names(df)
            df = self.optimize_memory(df, 'difficulty')
            
            # Filter for 2021-2024 only
            df = df[df['year'].isin([2021, 2022, 2023, 2024])]
            
            print(f"  ✅ Difficulty data: {df.shape}")
            print(f"  📊 Platforms with difficulty data: {sorted(df['Platform'].unique())}")
            
            # Check for Bitcoin SV
            if 'Bitcoin SV' not in df['Platform'].unique():
                print(f"  ⚠️  Bitcoin SV difficulty data missing (will be left blank)")
            
            return df
            
        except Exception as e:
            print(f"  ❌ Error loading difficulty data: {e}")
            return pd.DataFrame()
    
    def create_base_weekly_structure(self):
        """Create base weekly structure for 2021-2024"""
        print("\n🏗️  Creating base weekly structure...")
        
        # Create all combinations of Platform, Year, Week for 2021-2024
        platforms = self.target_platforms
        years = [2021, 2022, 2023, 2024]
        weeks = list(range(1, 53))  # 52 weeks per year
        
        base_data = []
        for platform in platforms:
            for year in years:
                for week in weeks:
                    base_data.append({
                        'Platform': platform,
                        'year': year,
                        'week': week
                    })
        
        df_base = pd.DataFrame(base_data)
        print(f"  ✅ Base structure: {df_base.shape}")
        
        return df_base
    
    def merge_datasets_efficiently(self, df_base, datasets, api_data, df_difficulty):
        """Efficiently merge all datasets"""
        print("\n🔗 Merging all datasets...")
        
        merge_keys = ['Platform', 'year', 'week']
        df_result = df_base.copy()
        
        # Merge core datasets
        for name, df in datasets.items():
            if not df.empty:
                print(f"  🔗 Merging {name}...")
                df_result = pd.merge(df_result, df, on=merge_keys, how='left', suffixes=('', f'_{name}'))
                print(f"    ✅ After {name}: {df_result.shape}")
                
                # Force garbage collection
                del df
                gc.collect()
        
        # Merge CryptoCompare time-series data
        if 'cryptocompare' in api_data and not api_data['cryptocompare'].empty:
            print(f"  🔗 Merging CryptoCompare time-series...")
            df_crypto = api_data['cryptocompare'][['Platform', 'year', 'week', 'Volume_USD', 'price_USD', 'Platform_age']]
            df_result = pd.merge(df_result, df_crypto, on=merge_keys, how='left', suffixes=('', '_crypto'))
            print(f"    ✅ After CryptoCompare: {df_result.shape}")
        
        # Merge GitHub data (static - merge on Platform only)
        if 'github' in api_data and not api_data['github'].empty:
            print(f"  🔗 Merging GitHub data...")
            df_github = api_data['github'][['Platform', 'stars', 'forks']]
            df_result = pd.merge(df_result, df_github, on='Platform', how='left', suffixes=('', '_github'))
            print(f"    ✅ After GitHub: {df_result.shape}")
        
        # Merge Reddit data (static - merge on Platform only)
        if 'reddit' in api_data and not api_data['reddit'].empty:
            print(f"  🔗 Merging Reddit data...")
            df_reddit = api_data['reddit'][['Platform', 'reddit_subscribers', 'reddit_posts', 'reddit_comments']]
            df_result = pd.merge(df_result, df_reddit, on='Platform', how='left', suffixes=('', '_reddit'))
            print(f"    ✅ After Reddit: {df_result.shape}")
        
        # Merge difficulty data (with Bitcoin SV handling)
        if not df_difficulty.empty:
            print(f"  🔗 Merging difficulty data...")
            df_diff_weekly = df_difficulty.groupby(['Platform', 'year', 'week'])['difficulty'].mean().reset_index()
            df_result = pd.merge(df_result, df_diff_weekly, on=merge_keys, how='left', suffixes=('', '_diff'))
            print(f"    ✅ After difficulty: {df_result.shape}")
            
            # Check Bitcoin SV difficulty coverage
            bsv_data = df_result[df_result['Platform'] == 'Bitcoin SV']
            bsv_difficulty_coverage = bsv_data['difficulty'].notna().sum() / len(bsv_data) * 100
            print(f"    📊 Bitcoin SV difficulty coverage: {bsv_difficulty_coverage:.1f}%")
        
        return df_result
    
    def add_date_variables(self, df):
        """Add proper date variables"""
        print("\n📅 Adding date variables...")
        
        def year_week_to_date(row):
            try:
                year, week = int(row['year']), int(row['week'])
                # Calculate the date for the Monday of the given week
                jan_1 = datetime(year, 1, 1)
                week_1_start = jan_1 - pd.Timedelta(days=jan_1.weekday())
                target_date = week_1_start + pd.Timedelta(weeks=week-1)
                return target_date
            except:
                return None
        
        df['date'] = df.apply(year_week_to_date, axis=1)
        print(f"  ✅ Date variables added")
        
        return df
    
    def generate_final_summary(self, df_final):
        """Generate comprehensive summary"""
        print("\n" + "="*80)
        print("COMPLETE 2021-2024 DATASET INTEGRATION SUMMARY")
        print("="*80)
        
        print(f"📊 FINAL DATASET:")
        print(f"  Shape: {df_final.shape}")
        print(f"  Memory usage: {df_final.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        print(f"  Date range: {df_final['date'].min()} to {df_final['date'].max()}")
        
        print(f"\n🏢 PLATFORM COVERAGE:")
        for platform in self.target_platforms:
            platform_data = df_final[df_final['Platform'] == platform]
            print(f"  {platform}: {len(platform_data):,} records")
        
        print(f"\n📈 VARIABLE COVERAGE:")
        key_variables = [
            'Block_HHI', 'Block_Shannon', 'Commit_HHI', 'Commit_Shannon',
            'market_cap', 'hashrate', 'Number_Proposal', 'Topic_Diversity',
            'Volume_USD', 'price_USD', 'Platform_age', 'stars', 'forks',
            'reddit_subscribers', 'reddit_posts', 'reddit_comments', 'difficulty'
        ]
        
        for var in key_variables:
            if var in df_final.columns:
                completeness = (1 - df_final[var].isnull().sum() / len(df_final)) * 100
                status = "✅" if completeness > 50 else "⚠️" if completeness > 0 else "❌"
                print(f"  {status} {var}: {completeness:.1f}% complete")
        
        print(f"\n🎯 BITCOIN SV DIFFICULTY STATUS:")
        bsv_data = df_final[df_final['Platform'] == 'Bitcoin SV']
        if not bsv_data.empty:
            bsv_difficulty_filled = bsv_data['difficulty'].notna().sum()
            bsv_total = len(bsv_data)
            print(f"  📊 Records with difficulty: {bsv_difficulty_filled}/{bsv_total}")
            print(f"  📊 Coverage: {bsv_difficulty_filled/bsv_total*100:.1f}%")
            if bsv_difficulty_filled == 0:
                print(f"  ⚠️  All Bitcoin SV difficulty values are blank (as expected)")
        
        print(f"\n✅ INTEGRATION COMPLETE!")
        print(f"📁 Output file: COMPLETE_2021_2024_blockchain_dataset.xlsx")
    
    def run_integration(self):
        """Main integration function"""
        start_time = datetime.now()
        
        try:
            # Load all datasets
            df_decentralization = self.load_and_process_decentralization_data()
            df_market = self.load_and_process_market_data()
            df_proposals = self.load_and_process_proposal_data()
            api_data = self.load_and_process_api_data()
            df_difficulty = self.load_and_process_difficulty_data()
            
            # Create base structure
            df_base = self.create_base_weekly_structure()
            
            # Prepare datasets for merging
            datasets = {
                'decentralization': df_decentralization,
                'market': df_market,
                'proposals': df_proposals
            }
            
            # Merge all datasets
            df_final = self.merge_datasets_efficiently(df_base, datasets, api_data, df_difficulty)
            
            # Add date variables
            df_final = self.add_date_variables(df_final)
            
            # Final memory optimization
            df_final = self.optimize_memory(df_final, 'final_dataset')
            
            # Save final dataset
            output_file = 'COMPLETE_2021_2024_blockchain_dataset.xlsx'
            df_final.to_excel(output_file, index=False)
            
            # Generate summary
            self.generate_final_summary(df_final)
            
            end_time = datetime.now()
            print(f"\n⏱️  Total execution time: {end_time - start_time}")
            
            return df_final
            
        except Exception as e:
            print(f"\n❌ INTEGRATION FAILED: {e}")
            import traceback
            traceback.print_exc()
            return None

# Execute the integration
if __name__ == "__main__":
    integrator = Complete2021_2024DatasetIntegrator()
    final_dataset = integrator.run_integration()
    
    if final_dataset is not None:
        print(f"\n🎉 SUCCESS! Complete 2021-2024 dataset created.")
        print(f"📁 File: COMPLETE_2021_2024_blockchain_dataset.xlsx")
        print(f"📊 Shape: {final_dataset.shape}")
    else:
        print(f"\n❌ Integration failed. Please check the error messages above.")

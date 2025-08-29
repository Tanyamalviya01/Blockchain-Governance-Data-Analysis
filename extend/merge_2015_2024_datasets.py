import pandas as pd
from datetime import datetime
import numpy as np

class DatasetMerger2015_2024:
    def __init__(self):
        self.datasets = {
            '2015_2020': 'NEW_CRYPTO_INTEGRATED_2015_2020.xlsx',
            '2021_2024': 'NEW_CRYPTO_INTEGRATED_2021_2024.xlsx'
        }
        
        self.platforms = ['Z-Cash', 'E-Cash', 'Monero', 'Cardano']
    
    def load_datasets(self):
        """Load both time period datasets"""
        print("📂 Loading datasets for merger...")
        
        loaded_data = {}
        
        for period, filename in self.datasets.items():
            try:
                df = pd.read_excel(filename)
                loaded_data[period] = df
                print(f"  ✅ Loaded {period}: {df.shape}")
                print(f"    Platforms: {sorted(df['Platform'].unique())}")
                print(f"    Date range: {df['year'].min()}-{df['year'].max()}")
            except Exception as e:
                print(f"  ❌ Failed to load {filename}: {e}")
                loaded_data[period] = pd.DataFrame()
        
        return loaded_data
    
    def standardize_columns(self, df_2015_2020, df_2021_2024):
        """Standardize column names and structure"""
        print("\n🔧 Standardizing column structures...")
        
        # Get all unique columns from both datasets
        all_columns = set(df_2015_2020.columns) | set(df_2021_2024.columns)
        
        # Add missing columns to each dataset
        for col in all_columns:
            if col not in df_2015_2020.columns:
                df_2015_2020[col] = np.nan
                print(f"  Added {col} to 2015-2020 dataset")
            
            if col not in df_2021_2024.columns:
                df_2021_2024[col] = np.nan
                print(f"  Added {col} to 2021-2024 dataset")
        
        # Reorder columns to match
        common_columns = sorted(all_columns)
        df_2015_2020 = df_2015_2020[common_columns]
        df_2021_2024 = df_2021_2024[common_columns]
        
        print(f"  ✅ Standardized to {len(common_columns)} columns")
        return df_2015_2020, df_2021_2024
    
    def merge_datasets(self, df_2015_2020, df_2021_2024):
        """Merge the two time period datasets"""
        print("\n🔗 Merging 2015-2020 and 2021-2024 datasets...")
        
        # Combine the datasets
        merged_df = pd.concat([df_2015_2020, df_2021_2024], ignore_index=True)
        
        # Sort by Platform, year, week
        merged_df = merged_df.sort_values(['Platform', 'year', 'week']).reset_index(drop=True)
        
        print(f"  ✅ Merged dataset: {merged_df.shape}")
        
        # Generate summary statistics
        print(f"\n📊 MERGER SUMMARY:")
        print(f"  Total records: {len(merged_df):,}")
        print(f"  Platforms: {len(merged_df['Platform'].unique())}")
        print(f"  Date range: {merged_df['year'].min()}-{merged_df['year'].max()}")
        
        # Platform-specific summary
        for platform in self.platforms:
            platform_data = merged_df[merged_df['Platform'] == platform]
            if not platform_data.empty:
                year_range = f"{platform_data['year'].min()}-{platform_data['year'].max()}"
                print(f"  {platform}: {len(platform_data):,} records ({year_range})")
        
        return merged_df
    
    def validate_merged_data(self, merged_df):
        """Validate the merged dataset"""
        print(f"\n✅ VALIDATING MERGED DATASET...")
        
        validation_results = {}
        
        # Check for temporal gaps
        for platform in self.platforms:
            platform_data = merged_df[merged_df['Platform'] == platform]
            if not platform_data.empty:
                years = sorted(platform_data['year'].unique())
                expected_years = list(range(years[0], years[-1] + 1))
                missing_years = set(expected_years) - set(years)
                
                validation_results[platform] = {
                    'records': len(platform_data),
                    'year_range': f"{years[0]}-{years[-1]}",
                    'missing_years': list(missing_years) if missing_years else None,
                    'data_quality': 'Good' if not missing_years else 'Gaps detected'
                }
        
        # Print validation results
        for platform, results in validation_results.items():
            status = "✅" if results['data_quality'] == 'Good' else "⚠️"
            print(f"  {status} {platform}: {results['records']} records, {results['year_range']}")
            if results['missing_years']:
                print(f"    Missing years: {results['missing_years']}")
        
        return validation_results
    
    def create_final_dataset(self, merged_df):
        """Create final comprehensive dataset"""
        print(f"\n📊 CREATING FINAL COMPREHENSIVE DATASET...")
        
        # Add metadata columns
        merged_df['data_source'] = 'Multi-API Collection'
        merged_df['collection_date'] = datetime.now().strftime('%Y-%m-%d')
        merged_df['temporal_coverage'] = '2015-2024'
        
        # Calculate additional metrics
        if 'price_USD' in merged_df.columns:
            # Add price change calculations where possible
            for platform in self.platforms:
                platform_mask = merged_df['Platform'] == platform
                platform_data = merged_df[platform_mask].copy()
                
                if len(platform_data) > 1:
                    platform_data = platform_data.sort_values(['year', 'week'])
                    platform_data['price_change_pct'] = platform_data['price_USD'].pct_change() * 100
                    merged_df.loc[platform_mask, 'price_change_pct'] = platform_data['price_change_pct']
        
        # Save final dataset
        output_filename = 'NEW_CRYPTO_COMPREHENSIVE_2015_2024.xlsx'
        merged_df.to_excel(output_filename, index=False)
        
        print(f"  ✅ Final dataset saved: {output_filename}")
        print(f"  📊 Shape: {merged_df.shape}")
        print(f"  📅 Coverage: 2015-2024 (10 years)")
        print(f"  🏢 Platforms: {len(merged_df['Platform'].unique())}")
        
        return merged_df, output_filename
    
    def run_merger(self):
        """Main merger function"""
        print("🔗 NEW CRYPTOCURRENCY DATASET MERGER (2015-2024)")
        print("="*80)
        print("Merging 2015-2020 and 2021-2024 datasets")
        print("Creating comprehensive 10-year dataset")
        print("="*80)
        
        start_time = datetime.now()
        
        # Load datasets
        loaded_data = self.load_datasets()
        
        if loaded_data['2015_2020'].empty or loaded_data['2021_2024'].empty:
            print("❌ Cannot proceed: One or both datasets are missing")
            return None
        
        # Standardize columns
        df_2015_2020, df_2021_2024 = self.standardize_columns(
            loaded_data['2015_2020'], 
            loaded_data['2021_2024']
        )
        
        # Merge datasets
        merged_df = self.merge_datasets(df_2015_2020, df_2021_2024)
        
        # Validate merged data
        validation_results = self.validate_merged_data(merged_df)
        
        # Create final dataset
        final_df, output_filename = self.create_final_dataset(merged_df)
        
        # Generate final summary
        end_time = datetime.now()
        print(f"\n{'='*80}")
        print("MERGER COMPLETION SUMMARY")
        print(f"{'='*80}")
        print(f"⏱️ Total time: {end_time - start_time}")
        print(f"📁 Output file: {output_filename}")
        print(f"📊 Final dataset: {final_df.shape}")
        print(f"🎯 Ready for integration with main 7-crypto dataset!")
        
        return final_df

# Execute the merger
if __name__ == "__main__":
    merger = DatasetMerger2015_2024()
    final_dataset = merger.run_merger()

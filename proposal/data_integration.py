import pandas as pd
import numpy as np
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def clean_illegal_chars(df):
    """Remove illegal characters from all string cells in a DataFrame"""
    return df.map(lambda x: ILLEGAL_CHARACTERS_RE.sub('', x) if isinstance(x, str) else x)

def load_and_standardize_datasets():
    """Load all datasets and standardize column names and formats"""
    print("=== LOADING ALL DATASETS FOR INTEGRATION ===")
    
    datasets = {}
    
    # Load your 2021-2024 datasets
    print("Loading 2021-2024 datasets...")
    
    # 1. Decentralization metrics
    try:
        datasets['decentralization'] = pd.read_excel('blockchain_decentralization_metrics_weekly_2021_2024.xlsx', sheet_name='Weekly_Metrics')
        print(f"  ✓ Decentralization metrics: {len(datasets['decentralization'])} records")
    except:
        print("  ✗ Decentralization metrics file not found")
    
    # 2. Market cap and hash rate
    try:
        datasets['market'] = pd.read_excel('blockchain_market_hashrate_2021_2024.xlsx', sheet_name='Weekly_Data')
        print(f"  ✓ Market data: {len(datasets['market'])} records")
    except:
        print("  ✗ Market data file not found")
    
    # 3. Proposal topic diversity
    try:
        datasets['proposals'] = pd.read_excel('proposal_topic_diversity_weekly.xlsx')
        print(f"  ✓ Proposal diversity: {len(datasets['proposals'])} records")
    except:
        print("  ✗ Proposal diversity file not found")
    
    return datasets

def integrate_all_datasets(datasets):
    """Integrate all datasets on Platform, Year, Week"""
    print("\nIntegrating all datasets...")
    
    # Start with decentralization metrics as base
    if 'decentralization' in datasets:
        master_df = datasets['decentralization'].copy()
        print(f"  Base dataset: {len(master_df)} records")
    else:
        print("  No base dataset available")
        return pd.DataFrame()
    
    # Merge market data
    if 'market' in datasets:
        master_df = master_df.merge(
            datasets['market'], 
            on=['Platform', 'Year', 'Week'], 
            how='outer',
            suffixes=('', '_market')
        )
        print(f"  After market merge: {len(master_df)} records")
    
    # Merge proposal diversity
    if 'proposals' in datasets:
        master_df = master_df.merge(
            datasets['proposals'], 
            on=['Platform', 'Year', 'Week'], 
            how='outer',
            suffixes=('', '_proposals')
        )
        print(f"  After proposals merge: {len(master_df)} records")
    
    # Fill missing values
    numeric_columns = master_df.select_dtypes(include=[np.number]).columns
    master_df[numeric_columns] = master_df[numeric_columns].fillna(0)
    
    # Sort by Platform, Year, Week
    master_df = master_df.sort_values(['Platform', 'Year', 'Week']).reset_index(drop=True)
    
    return master_df

def create_summary_statistics(master_df):
    """Create summary statistics for the integrated dataset"""
    print("\nCreating summary statistics...")
    
    summary_stats = []
    
    for platform in sorted(master_df['Platform'].unique()):
        platform_data = master_df[master_df['Platform'] == platform]
        
        stats = {
            'Platform': platform,
            'Total_Weeks': len(platform_data),
            'Years_Covered': f"{platform_data['Year'].min()}-{platform_data['Year'].max()}",
            'Avg_Block_Inverse_HHI': platform_data.get('Block_Inverse_HHI', pd.Series([0])).mean(),
            'Avg_Commit_Inverse_HHI': platform_data.get('Commit_Inverse_HHI', pd.Series([0])).mean(),
            'Avg_Market_Cap_Billions': platform_data.get('Market_Capitalization', pd.Series([0])).mean() / 1e9,
            'Avg_Hash_Rate_EH': platform_data.get('Hash_Rate', pd.Series([0])).mean() / 1e18,
            'Avg_Topic_Diversity': platform_data.get('Topic_Diversity', pd.Series([0])).mean(),
            'Total_Proposals': platform_data.get('Number_Proposal', pd.Series([0])).sum()
        }
        summary_stats.append(stats)
    
    return pd.DataFrame(summary_stats)

def main():
    print("=== BLOCKCHAIN GOVERNANCE DATASET INTEGRATION (2015-2024) ===")
    
    # Load all datasets
    datasets = load_and_standardize_datasets()
    
    if not datasets:
        print("No datasets loaded. Please check file paths.")
        return
    
    # Integrate datasets
    master_dataset = integrate_all_datasets(datasets)
    
    if master_dataset.empty:
        print("Integration failed.")
        return
    
    # Create summary statistics
    summary_stats = create_summary_statistics(master_dataset)
    
    # Clean data
    master_dataset = clean_illegal_chars(master_dataset)
    summary_stats = clean_illegal_chars(summary_stats)
    
    # Save integrated dataset
    output_file = 'integrated_blockchain_governance_dataset_2015_2024.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        master_dataset.to_excel(writer, sheet_name='Master_Dataset', index=False)
        summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)
    
    print(f"\n=== INTEGRATION COMPLETE ===")
    print(f"✓ Total records in master dataset: {len(master_dataset)}")
    print(f"✓ Platforms covered: {sorted(master_dataset['Platform'].unique())}")
    print(f"✓ Years covered: {master_dataset['Year'].min()}-{master_dataset['Year'].max()}")
    print(f"✓ Results saved to: {output_file}")
    
    # Print sample of integrated data
    print(f"\nSample of integrated dataset:")
    print(master_dataset.head(10)[['Platform', 'Year', 'Week', 'Block_Inverse_HHI', 'Market_Capitalization', 'Topic_Diversity']].to_string())
    
    print(f"\nSummary by platform:")
    print(summary_stats[['Platform', 'Total_Weeks', 'Years_Covered', 'Total_Proposals']].to_string())

if __name__ == "__main__":
    main()

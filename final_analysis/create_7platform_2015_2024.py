import pandas as pd
import numpy as np
from datetime import datetime

def create_7platform_dataset():
    print("Creating 7-platform dataset (2015-2024)...")
    
    # Load the historical data (2015-2020)
    print("Loading historical panel data...")
    historical_df = pd.read_stata('../proposal/Panel_data_cleaned_May23_2025.dta')
    
    # Load your complete 2021-2024 data
    print("Loading 2021-2024 data...")
    recent_df = pd.read_excel('../COMPLETE_2021_2024_blockchain_dataset.xlsx')
    
    # Standardize platform names
    platform_mapping = {
        'BitcoinCash': 'Bitcoin Cash',
        'BitcoinSV': 'Bitcoin SV'
    }
    
    if 'Platform' in historical_df.columns:
        historical_df['Platform'] = historical_df['Platform'].replace(platform_mapping)
    if 'Platform' in recent_df.columns:
        recent_df['Platform'] = recent_df['Platform'].replace(platform_mapping)
    
    # Standardize column names to match
    column_mapping = {
        'Block_Inverse_HHI': 'Block_HHI',
        'Block_Shannon_Entropy': 'Block_Shannon',
        'Commit_Inverse_HHI': 'Commit_HHI', 
        'Commit_Shannon_Entropy': 'Commit_Shannon',
        'Market_Capitalization': 'market_cap',
        'Hash_Rate': 'hashrate',
        'Year': 'year',
        'Week': 'week'
    }
    
    # Apply column mapping to historical data
    historical_df = historical_df.rename(columns=column_mapping)
    
    # Get common columns
    common_columns = set(historical_df.columns) & set(recent_df.columns)
    
    # Add missing columns with NaN
    for col in historical_df.columns:
        if col not in recent_df.columns:
            recent_df[col] = np.nan
    
    for col in recent_df.columns:
        if col not in historical_df.columns:
            historical_df[col] = np.nan
    
    # Align columns
    all_columns = sorted(set(historical_df.columns) | set(recent_df.columns))
    historical_df = historical_df.reindex(columns=all_columns)
    recent_df = recent_df.reindex(columns=all_columns)
    
    # Combine datasets
    combined_df = pd.concat([historical_df, recent_df], ignore_index=True)
    
    # Filter for 7 platforms only
    seven_platforms = ['Bitcoin', 'Ethereum', 'Litecoin', 'Dogecoin', 'Dash', 'Bitcoin Cash', 'Bitcoin SV']
    combined_df = combined_df[combined_df['Platform'].isin(seven_platforms)]
    
    # Sort by Platform, year, week
    combined_df = combined_df.sort_values(['Platform', 'year', 'week']).reset_index(drop=True)
    
    # Save as CSV (as requested by professor)
    combined_df.to_csv('original_7platforms_2015_2024.csv', index=False)
    
    print(f"✅ Created 7-platform dataset: {combined_df.shape}")
    print(f"Platforms: {sorted(combined_df['Platform'].unique())}")
    print(f"Year range: {combined_df['year'].min()}-{combined_df['year'].max()}")
    
    return combined_df

if __name__ == "__main__":
    df_7platforms = create_7platform_dataset()

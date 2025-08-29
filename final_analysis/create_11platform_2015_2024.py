import pandas as pd
import numpy as np

def create_11platform_dataset():
    print("Creating 11-platform dataset (2015-2024)...")
    
    # Load the 7-platform dataset
    print("Loading 7-platform dataset...")
    df_7platforms = pd.read_csv('original_7platforms_2015_2024.csv')
    
    # Load the 4 new platforms data
    print("Loading 4 new platforms data...")
    df_new_platforms = pd.read_excel('../extend/NEW_CRYPTO_COMPREHENSIVE_2015_2024.xlsx')
    
    # Standardize column names
    column_mapping = {
        'Platform_age': 'Platform_age',
        'price_USD': 'price_USD',
        'Volume_USD': 'Volume_USD'
    }
    
    df_new_platforms = df_new_platforms.rename(columns=column_mapping)
    
    # Get all unique columns
    all_columns = set(df_7platforms.columns) | set(df_new_platforms.columns)
    
    # Add missing columns to both datasets
    for col in all_columns:
        if col not in df_7platforms.columns:
            df_7platforms[col] = np.nan
        if col not in df_new_platforms.columns:
            df_new_platforms[col] = np.nan
    
    # Align column order
    all_columns_sorted = sorted(all_columns)
    df_7platforms = df_7platforms.reindex(columns=all_columns_sorted)
    df_new_platforms = df_new_platforms.reindex(columns=all_columns_sorted)
    
    # Combine all platforms
    combined_df = pd.concat([df_7platforms, df_new_platforms], ignore_index=True)
    
    # Sort by Platform, year, week
    combined_df = combined_df.sort_values(['Platform', 'year', 'week']).reset_index(drop=True)
    
    # Save as CSV
    combined_df.to_csv('all_11platforms_2015_2024.csv', index=False)
    
    print(f"✅ Created 11-platform dataset: {combined_df.shape}")
    print(f"Platforms: {sorted(combined_df['Platform'].unique())}")
    print(f"Year range: {combined_df['year'].min()}-{combined_df['year'].max()}")
    
    return combined_df

if __name__ == "__main__":
    df_11platforms = create_11platform_dataset()

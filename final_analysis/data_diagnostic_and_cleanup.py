import pandas as pd
import numpy as np

def create_clean_stata_ready_dataset():
    """Create a clean dataset ready for Stata panel analysis"""
    
    print("🔧 CREATING CLEAN STATA-READY DATASET")
    print("="*60)
    
    # Load the 11-platform dataset
    df = pd.read_csv('all_11platforms_2015_2024.csv', low_memory=False)
    print(f"Original dataset: {df.shape}")
    
    # Step 1: Remove rows with missing essential variables
    essential_vars = ['Platform', 'year', 'week']
    df_clean = df.dropna(subset=essential_vars).copy()
    print(f"After removing missing Platform/year/week: {df_clean.shape}")
    
    # Step 2: Create time variable
    df_clean['time_var'] = df_clean['year'] * 100 + df_clean['week']
    
    # Step 3: Check for and remove duplicates
    duplicates_before = df_clean.duplicated(subset=['Platform', 'time_var']).sum()
    print(f"Duplicates before cleaning: {duplicates_before}")
    
    if duplicates_before > 0:
        # Show examples of duplicates
        print("Examples of duplicate Platform-time combinations:")
        dup_examples = df_clean[df_clean.duplicated(subset=['Platform', 'time_var'], keep=False)]
        print(dup_examples.groupby(['Platform', 'year', 'week']).size().head(10))
        
        # Remove duplicates (keep first occurrence)
        df_clean = df_clean.drop_duplicates(subset=['Platform', 'time_var'], keep='first')
        print(f"After removing duplicates: {df_clean.shape}")
    
    # Step 4: Ensure proper data types
    df_clean['year'] = df_clean['year'].astype(int)
    df_clean['week'] = df_clean['week'].astype(int)
    df_clean['time_var'] = df_clean['time_var'].astype(int)
    
    # Step 5: Remove the existing platform_id column to avoid conflicts
    if 'platform_id' in df_clean.columns:
        df_clean = df_clean.drop('platform_id', axis=1)
        print("Removed existing platform_id column")
    
    # Step 6: Sort data for proper panel structure
    df_clean = df_clean.sort_values(['Platform', 'year', 'week']).reset_index(drop=True)
    
    # Step 7: Final validation
    final_duplicates = df_clean.duplicated(subset=['Platform', 'time_var']).sum()
    print(f"Final duplicates check: {final_duplicates}")
    
    if final_duplicates == 0:
        print("✅ Dataset is now ready for Stata panel analysis!")
    else:
        print("❌ Still has duplicates - manual review needed")
    
    # Step 8: Save cleaned dataset
    output_file = 'all_11platforms_STATA_READY.csv'
    df_clean.to_csv(output_file, index=False)
    print(f"💾 Saved clean dataset: {output_file}")
    
    # Step 9: Generate summary
    print(f"\n📊 FINAL DATASET SUMMARY:")
    print(f"Shape: {df_clean.shape}")
    print(f"Platforms: {sorted(df_clean['Platform'].unique())}")
    print(f"Year range: {df_clean['year'].min()}-{df_clean['year'].max()}")
    print(f"Platform-time combinations: {len(df_clean[['Platform', 'time_var']].drop_duplicates())}")
    
    return df_clean

if __name__ == "__main__":
    cleaned_data = create_clean_stata_ready_dataset()

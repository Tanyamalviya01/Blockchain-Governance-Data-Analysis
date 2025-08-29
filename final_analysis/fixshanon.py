import pandas as pd

# Load your existing datasets
print("Loading existing datasets...")
df_7platforms = pd.read_csv('original_7platforms_2015_2024.csv')
df_11platforms = pd.read_csv('all_11platforms_2015_2024.csv')

# Load Shannon data
print("Loading Shannon entropy data...")
shannon_df = pd.read_excel('../commits/blockchain_decentralization_metrics_weekly_2021_2024_fixed.xlsx')

# Rename columns in Shannon data to match your target datasets
shannon_df_renamed = shannon_df.rename(columns={
    'Year': 'year',
    'Week': 'week', 
    'Block_Shannon_Entropy': 'Block_Shannon',
    'Commit_Shannon_Entropy': 'Commit_Shannon'
})

print("Shannon data columns after renaming:")
print(shannon_df_renamed.columns.tolist())

# CRITICAL: Check if Block_Shannon/Commit_Shannon already exist in main datasets
print(f"\n7-platform dataset has Block_Shannon: {'Block_Shannon' in df_7platforms.columns}")
print(f"11-platform dataset has Block_Shannon: {'Block_Shannon' in df_11platforms.columns}")

# If they already exist, drop them first to avoid conflicts
if 'Block_Shannon' in df_7platforms.columns:
    print("Dropping existing Block_Shannon from 7-platform dataset")
    df_7platforms = df_7platforms.drop('Block_Shannon', axis=1)
    
if 'Commit_Shannon' in df_7platforms.columns:
    print("Dropping existing Commit_Shannon from 7-platform dataset") 
    df_7platforms = df_7platforms.drop('Commit_Shannon', axis=1)

if 'Block_Shannon' in df_11platforms.columns:
    print("Dropping existing Block_Shannon from 11-platform dataset")
    df_11platforms = df_11platforms.drop('Block_Shannon', axis=1)
    
if 'Commit_Shannon' in df_11platforms.columns:
    print("Dropping existing Commit_Shannon from 11-platform dataset")
    df_11platforms = df_11platforms.drop('Commit_Shannon', axis=1)

# Now merge Shannon data into both datasets
print("\nMerging Shannon data...")
df_7platforms_fixed = pd.merge(
    df_7platforms, 
    shannon_df_renamed[['Platform', 'year', 'week', 'Block_Shannon', 'Commit_Shannon']], 
    on=['Platform', 'year', 'week'], 
    how='left'
)

df_11platforms_fixed = pd.merge(
    df_11platforms, 
    shannon_df_renamed[['Platform', 'year', 'week', 'Block_Shannon', 'Commit_Shannon']], 
    on=['Platform', 'year', 'week'], 
    how='left'
)

# Save the corrected datasets
df_7platforms_fixed.to_csv('original_7platforms_2015_2024_FIXED.csv', index=False)
df_11platforms_fixed.to_csv('all_11platforms_2015_2024_FIXED.csv', index=False)

print("✅ Shannon entropy data merged successfully!")
print(f"7-platform dataset shape: {df_7platforms_fixed.shape}")
print(f"11-platform dataset shape: {df_11platforms_fixed.shape}")

# Verify the columns now exist
print(f"\n7-platform dataset has Block_Shannon after merge: {'Block_Shannon' in df_7platforms_fixed.columns}")
print(f"11-platform dataset has Block_Shannon after merge: {'Block_Shannon' in df_11platforms_fixed.columns}")

# Verify the merge worked by checking for non-null values
print(f"\nBlock_Shannon non-null count in 7-platform dataset: {df_7platforms_fixed['Block_Shannon'].notna().sum()}")
print(f"Commit_Shannon non-null count in 7-platform dataset: {df_7platforms_fixed['Commit_Shannon'].notna().sum()}")

print(f"\nBlock_Shannon non-null count in 11-platform dataset: {df_11platforms_fixed['Block_Shannon'].notna().sum()}")  
print(f"Commit_Shannon non-null count in 11-platform dataset: {df_11platforms_fixed['Commit_Shannon'].notna().sum()}")

# Check unique platforms and years with Shannon data
print(f"\n7-platform dataset platforms: {sorted(df_7platforms_fixed['Platform'].unique())}")
print(f"Years with Shannon data: {sorted(df_7platforms_fixed[df_7platforms_fixed['Block_Shannon'].notna()]['year'].unique())}")

print(f"\n11-platform dataset platforms: {sorted(df_11platforms_fixed['Platform'].unique())}")
print(f"Years with Shannon data: {sorted(df_11platforms_fixed[df_11platforms_fixed['Block_Shannon'].notna()]['year'].unique())}")

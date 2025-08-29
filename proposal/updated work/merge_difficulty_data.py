import pandas as pd

# Load both datasets
df_main = pd.read_excel('GROUP1_FINAL_integrated_dataset_memory_efficient.xlsx')
df_diff = pd.read_excel('difficulty_data_full_2021_2024.xlsx')

print("=== DATE RANGE ANALYSIS ===")
print("Main dataset:")
print(f"  Year range: {df_main['year'].min()} to {df_main['year'].max()}")
print(f"  Week range: {df_main['week'].min()} to {df_main['week'].max()}")

print("\nDifficulty dataset:")
print(f"  Year range: {df_diff['year'].min()} to {df_diff['year'].max()}")
print(f"  Week range: {df_diff['week'].min()} to {df_diff['week'].max()}")

print("\n=== PLATFORM-SPECIFIC ANALYSIS ===")
for platform in ['Bitcoin', 'Ethereum', 'Litecoin']:
    main_data = df_main[df_main['Platform'] == platform]
    diff_data = df_diff[df_diff['Platform'] == platform]
    
    print(f"\n{platform}:")
    print(f"  Main dataset: {len(main_data)} rows, years {main_data['year'].min()}-{main_data['year'].max()}")
    print(f"  Difficulty dataset: {len(diff_data)} rows, years {diff_data['year'].min()}-{diff_data['year'].max()}")

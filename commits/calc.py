import pandas as pd
import numpy as np
from datetime import datetime
import math
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def clean_illegal_chars(df):
    """Remove illegal characters from all string cells in a DataFrame"""
    return df.map(lambda x: ILLEGAL_CHARACTERS_RE.sub('', x) if isinstance(x, str) else x)

def standardize_platform_names(df):
    """Standardize platform names between block and commit data"""
    df['Platform'] = df['Platform'].replace({
        'Ethereum_Go': 'Ethereum',
        'Bitcoin_Cash': 'Bitcoin_Cash',  # Keep as is
        'Bitcoin_SV': 'Bitcoin_SV'      # Keep as is
    })
    return df

def calculate_inverse_hhi(proportions):
    """
    Calculate Inverse Herfindahl-Hirschman Index
    HHI = sum(proportion^2)
    Inverse HHI = 1/HHI
    """
    # Remove zero proportions
    proportions = proportions[proportions > 0]
    if len(proportions) == 0:
        return 0
    
    # Calculate HHI
    hhi = np.sum(proportions ** 2)
    
    # Return Inverse HHI
    return 1 / hhi if hhi > 0 else 0

def calculate_shannon_entropy(proportions):
    """
    Calculate Shannon Entropy
    H = -sum(p * ln(p)) where p is proportion
    """
    # Remove zero proportions
    proportions = proportions[proportions > 0]
    if len(proportions) == 0:
        return 0
    
    # Calculate Shannon Entropy
    entropy = -np.sum(proportions * np.log(proportions))
    return entropy

def process_block_data(file_path):
    """
    Process block-level data to calculate weekly decentralization metrics
    """
    print("Processing block-level data...")
    
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Standardize platform names
    df = standardize_platform_names(df)
    
    # Convert block_date to datetime
    df['block_date'] = pd.to_datetime(df['block_date'])
    
    # Extract year and week
    df['year'] = df['block_date'].dt.isocalendar().year
    df['week'] = df['block_date'].dt.isocalendar().week
    
    # Group by platform, year, week, and miner to count blocks per miner
    miner_blocks = df.groupby(['Platform', 'year', 'week', 'miner']).size().reset_index(name='block_count')
    
    # Calculate total blocks per platform per week
    weekly_totals = miner_blocks.groupby(['Platform', 'year', 'week'])['block_count'].sum().reset_index(name='total_blocks')
    
    # Merge to get proportions
    miner_blocks = miner_blocks.merge(weekly_totals, on=['Platform', 'year', 'week'])
    miner_blocks['proportion'] = miner_blocks['block_count'] / miner_blocks['total_blocks']
    
    # Calculate metrics for each platform-year-week combination
    block_metrics = []
    
    for (platform, year, week), group in miner_blocks.groupby(['Platform', 'year', 'week']):
        proportions = group['proportion'].values
        
        inverse_hhi = calculate_inverse_hhi(proportions)
        shannon_entropy = calculate_shannon_entropy(proportions)
        
        block_metrics.append({
            'Platform': platform,
            'Year': year,
            'Week': week,
            'Block_Inverse_HHI': inverse_hhi,
            'Block_Shannon_Entropy': shannon_entropy,
            'Total_Blocks': group['total_blocks'].iloc[0],
            'Unique_Miners': len(group)
        })
    
    return pd.DataFrame(block_metrics)

def process_commit_data(file_path):
    """
    Process commit-level data to calculate weekly decentralization metrics
    """
    print("Processing commit-level data...")
    
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Standardize platform names
    df = standardize_platform_names(df)
    
    # Convert commit_date to datetime
    df['commit_date'] = pd.to_datetime(df['commit_date'])
    
    # Extract year and week
    df['year'] = df['commit_date'].dt.isocalendar().year
    df['week'] = df['commit_date'].dt.isocalendar().week
    
    # Group by platform, year, week, and author to count commits per author
    author_commits = df.groupby(['Platform', 'year', 'week', 'author_email']).size().reset_index(name='commit_count')
    
    # Calculate total commits per platform per week
    weekly_totals = author_commits.groupby(['Platform', 'year', 'week'])['commit_count'].sum().reset_index(name='total_commits')
    
    # Merge to get proportions
    author_commits = author_commits.merge(weekly_totals, on=['Platform', 'year', 'week'])
    author_commits['proportion'] = author_commits['commit_count'] / author_commits['total_commits']
    
    # Calculate metrics for each platform-year-week combination
    commit_metrics = []
    
    for (platform, year, week), group in author_commits.groupby(['Platform', 'year', 'week']):
        proportions = group['proportion'].values
        
        inverse_hhi = calculate_inverse_hhi(proportions)
        shannon_entropy = calculate_shannon_entropy(proportions)
        
        commit_metrics.append({
            'Platform': platform,
            'Year': year,
            'Week': week,
            'Commit_Inverse_HHI': inverse_hhi,
            'Commit_Shannon_Entropy': shannon_entropy,
            'Total_Commits': group['total_commits'].iloc[0],
            'Unique_Authors': len(group)
        })
    
    return pd.DataFrame(commit_metrics)

def combine_metrics(block_metrics, commit_metrics):
    """
    Combine block and commit metrics into final table
    """
    print("Combining block and commit metrics...")
    
    # Merge on Platform, Year, Week
    combined = pd.merge(
        block_metrics[['Platform', 'Year', 'Week', 'Block_Inverse_HHI', 'Block_Shannon_Entropy', 'Total_Blocks', 'Unique_Miners']],
        commit_metrics[['Platform', 'Year', 'Week', 'Commit_Inverse_HHI', 'Commit_Shannon_Entropy', 'Total_Commits', 'Unique_Authors']],
        on=['Platform', 'Year', 'Week'],
        how='outer'
    )
    
    # Fill NaN values with 0
    combined = combined.fillna(0)
    
    # Sort by Platform, Year, Week
    combined = combined.sort_values(['Platform', 'Year', 'Week']).reset_index(drop=True)
    
    return combined

def create_summary_statistics(combined_df):
    """
    Create summary statistics for the metrics
    """
    summary_stats = []
    
    for platform in combined_df['Platform'].unique():
        platform_data = combined_df[combined_df['Platform'] == platform]
        
        stats = {
            'Platform': platform,
            'Total_Weeks': len(platform_data),
            'Avg_Block_Inverse_HHI': platform_data['Block_Inverse_HHI'].mean(),
            'Avg_Block_Shannon_Entropy': platform_data['Block_Shannon_Entropy'].mean(),
            'Avg_Commit_Inverse_HHI': platform_data['Commit_Inverse_HHI'].mean(),
            'Avg_Commit_Shannon_Entropy': platform_data['Commit_Shannon_Entropy'].mean(),
            'Total_Blocks': platform_data['Total_Blocks'].sum(),
            'Total_Commits': platform_data['Total_Commits'].sum(),
            'Avg_Unique_Miners': platform_data['Unique_Miners'].mean(),
            'Avg_Unique_Authors': platform_data['Unique_Authors'].mean()
        }
        summary_stats.append(stats)
    
    return pd.DataFrame(summary_stats)

def main():
    print("=== BLOCKCHAIN DECENTRALIZATION METRICS CALCULATION ===")
    
    # File paths
    block_data_file = 'blockchain_block_data_real_2021_2024.xlsx'
    commit_data_file = 'blockchain_commit_data_all_2021_2024.xlsx'
    
    # Process block data
    block_metrics = process_block_data(block_data_file)
    print(f"Calculated block metrics for {len(block_metrics)} platform-week combinations")
    
    # Process commit data
    commit_metrics = process_commit_data(commit_data_file)
    print(f"Calculated commit metrics for {len(commit_metrics)} platform-week combinations")
    
    # Combine metrics
    combined_metrics = combine_metrics(block_metrics, commit_metrics)
    print(f"Combined metrics: {len(combined_metrics)} total records")
    
    # Create summary statistics
    summary_stats = create_summary_statistics(combined_metrics)
    
    # Clean data before saving
    combined_metrics = clean_illegal_chars(combined_metrics)
    summary_stats = clean_illegal_chars(summary_stats)
    
    # Save to Excel
    output_file = 'blockchain_decentralization_metrics_weekly_2021_2024_fixed.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_metrics.to_excel(writer, sheet_name='Weekly_Metrics', index=False)
        summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)
    
    print(f"\n=== CALCULATION COMPLETE ===")
    print(f"Results saved to: {output_file}")
    
    # Print sample results
    print(f"\nSample of weekly metrics:")
    print(combined_metrics.head(10).to_string())
    
    print(f"\nSummary statistics by platform:")
    print(summary_stats.to_string())
    
    # Print platform verification
    print(f"\nPlatforms in final results:")
    print(sorted(combined_metrics['Platform'].unique()))
    
    # Print interpretation
    print(f"\n=== INTERPRETATION ===")
    print("Higher Inverse HHI = More decentralized (more equal distribution)")
    print("Higher Shannon Entropy = More decentralized (more equal distribution)")
    print("Lower values = More centralized (concentrated among fewer participants)")

if __name__ == "__main__":
    main()

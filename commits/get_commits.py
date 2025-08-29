import requests
import pandas as pd
import time
from datetime import datetime
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

# Fetch commits from a GitHub repository between specified dates
def get_commits(repo_owner, repo_name, start_date, end_date, platform_name, token):
    print(f"Fetching commits for {repo_owner}/{repo_name} ({platform_name}) from {start_date} to {end_date}")
    headers = {'Authorization': f'token {token}'}
    all_commits = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        params = {
            'per_page': per_page,
            'page': page,
            'since': f"{start_date}T00:00:00Z",
            'until': f"{end_date}T23:59:59Z"
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            commits = response.json()
            if not commits or not isinstance(commits, list):
                break
            print(f"Retrieved {len(commits)} commits from page {page}")
            for commit in commits:
                try:
                    author_date = pd.to_datetime(commit['commit']['author']['date']).replace(tzinfo=None)
                    commit_date = pd.to_datetime(commit['commit']['committer']['date']).replace(tzinfo=None)
                    commit_data = {
                        'Token_id': commit['sha'][:12],
                        'commit_id': commit['sha'],
                        'author_name': commit['commit']['author']['name'],
                        'author_email': commit['commit']['author']['email'],
                        'author_date': author_date,
                        'committer_name': commit['commit']['committer']['name'],
                        'committer_email': commit['commit']['committer']['email'],
                        'commit_date': commit_date,
                        'commit_message': commit['commit']['message'],
                        'commit_verified': False,
                        'commit_reason': 'unsigned',
                        'Platform': platform_name
                    }
                    if 'verification' in commit['commit']:
                        commit_data['commit_verified'] = commit['commit']['verification'].get('verified', False)
                        commit_data['commit_reason'] = commit['commit']['verification'].get('reason', 'unsigned')
                    all_commits.append(commit_data)
                except KeyError as e:
                    print(f"Error processing commit: {e}")
                    continue
            page += 1
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                if remaining < 10:
                    reset_time = int(response.headers['X-RateLimit-Reset'])
                    sleep_time = reset_time - time.time() + 10
                    print(f"Rate limit almost reached. Sleeping for {sleep_time} seconds")
                    time.sleep(max(sleep_time, 0))
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            if hasattr(response, 'status_code') and response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
                if int(response.headers['X-RateLimit-Remaining']) == 0:
                    reset_time = int(response.headers['X-RateLimit-Reset'])
                    sleep_time = reset_time - time.time() + 10
                    print(f"Rate limit reached. Sleeping for {sleep_time} seconds")
                    time.sleep(max(sleep_time, 0))
                    continue
            break

    return pd.DataFrame(all_commits) if all_commits else pd.DataFrame()

# Get repository statistics like fork count and watch count
def get_repo_stats(repo_owner, repo_name, token):
    headers = {'Authorization': f'token {token}'}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        return {
            'fork_count': repo_data.get('forks_count', 0),
            'watch_count': repo_data.get('watchers_count', 0)
        }
    except requests.exceptions.RequestException as e:
        print(f"Error getting repo stats: {e}")
        return {'fork_count': 0, 'watch_count': 0}
    
# Create a summary sheet with statistics for each platform and year
def create_summary_sheet(all_data):
    summary_data = []
    all_data['commit_date'] = pd.to_datetime(all_data['commit_date'])
    all_data['year'] = all_data['commit_date'].dt.year
    platform_yearly_stats = all_data.groupby(['Platform', 'year']).size().reset_index(name='Commit_Count')
    for _, row in platform_yearly_stats.iterrows():
        platform = row['Platform']
        year = row['year']
        commit_count = row['Commit_Count']
        platform_year_data = all_data[(all_data['Platform'] == platform) & (all_data['year'] == year)]
        author_count = platform_year_data['author_email'].nunique()
        summary_data.append({
            'Platform': platform,
            'Commit Count': commit_count,
            'Author Count': author_count,
            'Fork Count': 0,
            'Watch Count': 0,
            'Time': year,
            'Date': year,
            'Remarks': 'Weekly base' if year == 2021 else ''
        })
    return pd.DataFrame(summary_data)

# Remove illegal characters from all string cells in a DataFrame
def clean_illegal_chars(df):
    return df.applymap(lambda x: ILLEGAL_CHARACTERS_RE.sub('', x) if isinstance(x, str) else x)

def main():
    # My GitHub token 
    token = "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"
    
    # blockchain repositories (now including all 7)
    repositories = [
        {"owner": "ethereum", "name": "go-ethereum", "platform": "Ethereum_Go"},
        {"owner": "bitcoin", "name": "bitcoin", "platform": "Bitcoin"},
        {"owner": "Bitcoin-ABC", "name": "bitcoin-abc", "platform": "Bitcoin_Cash"},
        {"owner": "dogecoin", "name": "dogecoin", "platform": "Dogecoin"},
        {"owner": "bitcoin-sv", "name": "bitcoin-sv", "platform": "Bitcoin_SV"},
        {"owner": "dashpay", "name": "dash", "platform": "Dash"},
        {"owner": "litecoin-project", "name": "litecoin", "platform": "Litecoin"}
    ]
    
    # years to collect data for
    years = ["2021", "2022", "2023", "2024"]
    
    # Storage for all data
    all_commit_data = pd.DataFrame()
    
    # Process each repository
    for repo in repositories:
        print(f"\n=== Starting data collection for {repo['platform']} ===")
        repo_data = pd.DataFrame()
        for year in years:
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            df = get_commits(repo["owner"], repo["name"], start_date, end_date, repo["platform"], token)
            if not df.empty:
                repo_data = pd.concat([repo_data, df], ignore_index=True)
                print(f"Collected {len(df)} commits for {repo['platform']} in {year}")
            else:
                print(f"No commits found for {repo['platform']} in {year}")
        if not repo_data.empty:
            all_commit_data = pd.concat([all_commit_data, repo_data], ignore_index=True)
            print(f"Total commits collected for {repo['platform']}: {len(repo_data)}")
        print(f"Completed {repo['platform']}. Waiting 5 seconds before next repository...")
        time.sleep(5)
    
    if all_commit_data.empty:
        print("No data was collected. Please check your token or network connection.")
        return
    
    # Reorder columns to match the example file
    column_order = [
        'Token_id', 'commit_id', 'author_name', 'author_email', 'author_date',
        'committer_name', 'committer_email', 'commit_date', 'commit_message',
        'commit_verified', 'commit_reason', 'Platform'
    ]
    for col in column_order:
        if col not in all_commit_data.columns:
            all_commit_data[col] = ""
    all_commit_data = all_commit_data[column_order]
    
    # Create summary sheet
    summary_data = create_summary_sheet(all_commit_data)
    
    # Clean illegal characters before writing to Excel
    all_commit_data = clean_illegal_chars(all_commit_data)
    summary_data    = clean_illegal_chars(summary_data)
    
    # Save to Excel with two sheets
    output_file = 'blockchain_commit_data_all_2021_2024.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        all_commit_data.to_excel(writer, sheet_name='Sheet1', index=False)
        summary_data   .to_excel(writer, sheet_name='Sheet2', index=False)
    
    print(f"\n=== DATA COLLECTION COMPLETE ===")
    print(f"Total commits collected: {len(all_commit_data)}")
    print(f"Results saved to: {output_file}")
    
    # Print breakdown by platform
    platform_summary = all_commit_data.groupby('Platform').size().reset_index(name='Total_Commits')
    print(f"\nBreakdown by platform:")
    for _, row in platform_summary.iterrows():
        print(f"  {row['Platform']}: {row['Total_Commits']} commits")
    
    # Print breakdown by year
    all_commit_data['year'] = pd.to_datetime(all_commit_data['commit_date']).dt.year
    year_summary = all_commit_data.groupby('year').size().reset_index(name='Total_Commits')
    print(f"\nBreakdown by year:")
    for _, row in year_summary.iterrows():
        print(f"  {row['year']}: {row['Total_Commits']} commits")

if __name__ == "__main__":
    main()

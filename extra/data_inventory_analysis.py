import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

class RADataInventoryAnalyzer:
    def __init__(self):
        self.output_file = "RA_DATA_INVENTORY_REPORT.txt"
        self.results = {}
        self.target_variables = {
            'Panel Variables': [
                'Block_HHI', 'Block_Shannon', 'Commit_HHI', 'Commit_Shannon',
                'mean_difficulty', 'max_difficulty', 'difficulty'
            ],
            'Market Variables': [
                'market_cap', 'hashrate', 'Volume_USD', 'price_USD'
            ],
            'Proposal Variables': [
                'number_proposal', 'topic_diversity', 'Number_Proposal', 'Topic_Diversity'
            ],
            'API Variables': [
                'stars', 'forks', 'reddit_subscribers', 'reddit_posts', 
                'reddit_comments', 'Platform_age'
            ],
            'Time Variables': [
                'date', 'year', 'week', 'Platform'
            ]
        }
        
        # File paths to analyze
        self.file_paths = {
            # Commits folder
            'commits/blockchain_block_data_real_2021_2024.xlsx': 'Block Data',
            'commits/blockchain_commit_data_all_2021_2024.xlsx': 'Commit Data',
            'commits/blockchain_decentralization_metrics_weekly_2021_2024_fixed.xlsx': 'Decentralization Metrics',
            'commits/blockchain_market_hashrate_weekly_2021_2024.xlsx': 'Market & Hashrate',
            'commits/ethereum_eip_data_2021_2024.xlsx': 'Ethereum EIP Data',
            'commits/improvement_proposals_all_platforms_2021_2024.xlsx': 'Improvement Proposals',
            
            # Proposal folder
            'proposal/Panel_data_cleaned_May23_2025.dta': 'Historical Panel Data',
            'proposal/detailed_proposal_analysis.xlsx': 'Detailed Proposals',
            'proposal/integrated_blockchain_governance_dataset_2015_2024.xlsx': 'Integrated Dataset',
            'proposal/proposal_topic_diversity_weekly.xlsx': 'Topic Diversity',
            
            # Updated work folder
            'proposal/updated work/GROUP1_FINAL_integrated_dataset_memory_efficient.xlsx': 'Group 1 Final Dataset',
            'proposal/updated work/cryptocompare_timeseries_2021_2024.xlsx': 'CryptoCompare Data',
            'proposal/updated work/difficulty_data_full_2021_2024.xlsx': 'Difficulty Data',
            'proposal/updated work/task1_base_panel_checkpoint.xlsx': 'Base Panel Checkpoint',
            'proposal/updated work/task2_blocks_checkpoint.xlsx': 'Blocks Checkpoint',
            'proposal/updated work/task2_commits_checkpoint.xlsx': 'Commits Checkpoint',
            'proposal/updated work/task2_decentralization_checkpoint.xlsx': 'Decentralization Checkpoint',
            'proposal/updated work/task2_market_checkpoint.xlsx': 'Market Checkpoint',
            'proposal/updated work/task2_proposals_checkpoint.xlsx': 'Proposals Checkpoint',
            'proposal/updated work/task3_cryptocompare_checkpoint.xlsx': 'CryptoCompare Checkpoint',
            'proposal/updated work/task3_github_checkpoint.xlsx': 'GitHub Checkpoint',
            'proposal/updated work/task3_reddit_checkpoint.xlsx': 'Reddit Checkpoint'
        }
    
    def analyze_file(self, file_path, description):
        """Analyze a single file and extract metadata"""
        print(f"Analyzing: {description} ({file_path})")
        
        if not os.path.exists(file_path):
            return {
                'status': 'FILE_NOT_FOUND',
                'error': f"File not found: {file_path}"
            }
        
        try:
            # Load file based on extension
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.dta'):
                df = pd.read_stata(file_path)
            else:
                return {'status': 'UNSUPPORTED_FORMAT'}
            
            # Basic file info
            result = {
                'status': 'SUCCESS',
                'shape': df.shape,
                'columns': list(df.columns),
                'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'found_variables': {},
                'date_info': {},
                'platform_info': {},
                'sample_data': {}
            }
            
            # Check for target variables
            for category, variables in self.target_variables.items():
                found = [var for var in variables if var in df.columns]
                if found:
                    result['found_variables'][category] = found
            
            # Analyze date information
            if 'date' in df.columns:
                try:
                    df['date'] = pd.to_datetime(df['date'])
                    result['date_info']['date_range'] = {
                        'min': str(df['date'].min()),
                        'max': str(df['date'].max())
                    }
                except:
                    result['date_info']['date_range'] = 'Could not parse dates'
            
            if 'year' in df.columns:
                years = df['year'].dropna().unique()
                result['date_info']['years'] = sorted([int(y) for y in years if pd.notna(y)])
            
            if 'week' in df.columns:
                weeks = df['week'].dropna()
                result['date_info']['week_range'] = {
                    'min': int(weeks.min()) if len(weeks) > 0 else None,
                    'max': int(weeks.max()) if len(weeks) > 0 else None
                }
            
            # Platform information
            if 'Platform' in df.columns:
                platforms = df['Platform'].dropna().unique()
                result['platform_info']['platforms'] = list(platforms)
                result['platform_info']['platform_count'] = len(platforms)
            
            # Sample data for key variables
            key_vars = ['Platform', 'year', 'week', 'date']
            available_key_vars = [var for var in key_vars if var in df.columns]
            if available_key_vars:
                sample = df[available_key_vars].head(3).to_dict('records')
                result['sample_data'] = sample
            
            return result
            
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e)
            }
    
    def generate_report(self):
        """Generate comprehensive inventory report"""
        print("Starting comprehensive data inventory analysis...")
        print("="*80)
        
        # Open output file
        with open(self.output_file, 'w') as f:
            # Write header
            f.write("RA RESEARCH DATA INVENTORY REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files to analyze: {len(self.file_paths)}\n\n")
            
            # Analyze each file
            for file_path, description in self.file_paths.items():
                result = self.analyze_file(file_path, description)
                self.results[file_path] = result
                
                # Write to file
                f.write(f"\n{'='*60}\n")
                f.write(f"FILE: {description}\n")
                f.write(f"PATH: {file_path}\n")
                f.write(f"{'='*60}\n")
                
                if result['status'] == 'SUCCESS':
                    f.write(f"✅ STATUS: Successfully analyzed\n")
                    f.write(f"📊 SHAPE: {result['shape'][0]:,} rows × {result['shape'][1]} columns\n")
                    f.write(f"💾 SIZE: {result['memory_mb']:.1f} MB\n\n")
                    
                    # Found variables
                    if result['found_variables']:
                        f.write("🔍 FOUND VARIABLES:\n")
                        for category, variables in result['found_variables'].items():
                            f.write(f"  {category}: {', '.join(variables)}\n")
                        f.write("\n")
                    
                    # Date information
                    if result['date_info']:
                        f.write("📅 DATE INFORMATION:\n")
                        for key, value in result['date_info'].items():
                            f.write(f"  {key}: {value}\n")
                        f.write("\n")
                    
                    # Platform information
                    if result['platform_info']:
                        f.write("🏢 PLATFORM INFORMATION:\n")
                        for key, value in result['platform_info'].items():
                            f.write(f"  {key}: {value}\n")
                        f.write("\n")
                    
                    # All columns
                    f.write("📋 ALL COLUMNS:\n")
                    for i, col in enumerate(result['columns'], 1):
                        f.write(f"  {i:2d}. {col}\n")
                    f.write("\n")
                    
                    # Sample data
                    if result['sample_data']:
                        f.write("📝 SAMPLE DATA (first 3 rows):\n")
                        for i, row in enumerate(result['sample_data'], 1):
                            f.write(f"  Row {i}: {row}\n")
                        f.write("\n")
                
                else:
                    f.write(f"❌ STATUS: {result['status']}\n")
                    if 'error' in result:
                        f.write(f"ERROR: {result['error']}\n")
                    f.write("\n")
            
            # Generate summary
            self.generate_summary(f)
    
    def generate_summary(self, f):
        """Generate summary section"""
        f.write("\n" + "="*80 + "\n")
        f.write("COMPREHENSIVE SUMMARY ANALYSIS\n")
        f.write("="*80 + "\n")
        
        # Count successful files
        successful_files = [k for k, v in self.results.items() if v['status'] == 'SUCCESS']
        f.write(f"📊 Successfully analyzed: {len(successful_files)}/{len(self.file_paths)} files\n\n")
        
        # Variable coverage analysis
        f.write("🔍 VARIABLE COVERAGE ANALYSIS:\n")
        f.write("-" * 40 + "\n")
        
        all_found_vars = {}
        for category in self.target_variables.keys():
            all_found_vars[category] = set()
        
        # Collect all found variables
        for file_path, result in self.results.items():
            if result['status'] == 'SUCCESS' and 'found_variables' in result:
                for category, variables in result['found_variables'].items():
                    all_found_vars[category].update(variables)
        
        # Report coverage
        for category, target_vars in self.target_variables.items():
            found_vars = all_found_vars[category]
            coverage = len(found_vars) / len(target_vars) * 100 if target_vars else 0
            f.write(f"\n{category}:\n")
            f.write(f"  Coverage: {coverage:.1f}% ({len(found_vars)}/{len(target_vars)})\n")
            f.write(f"  Found: {', '.join(sorted(found_vars)) if found_vars else 'None'}\n")
            missing = set(target_vars) - found_vars
            if missing:
                f.write(f"  Missing: {', '.join(sorted(missing))}\n")
        
        # Date range analysis
        f.write(f"\n📅 DATE RANGE ANALYSIS:\n")
        f.write("-" * 40 + "\n")
        
        all_years = set()
        files_with_2021_2024 = []
        
        for file_path, result in self.results.items():
            if result['status'] == 'SUCCESS' and 'date_info' in result:
                if 'years' in result['date_info']:
                    years = result['date_info']['years']
                    all_years.update(years)
                    if any(year in [2021, 2022, 2023, 2024] for year in years):
                        files_with_2021_2024.append(file_path.split('/')[-1])
        
        f.write(f"All years found across files: {sorted(all_years)}\n")
        f.write(f"Files with 2021-2024 data: {len(files_with_2021_2024)}\n")
        for file in files_with_2021_2024:
            f.write(f"  - {file}\n")
        
        # Platform analysis
        f.write(f"\n🏢 PLATFORM ANALYSIS:\n")
        f.write("-" * 40 + "\n")
        
        all_platforms = set()
        for file_path, result in self.results.items():
            if result['status'] == 'SUCCESS' and 'platform_info' in result:
                if 'platforms' in result['platform_info']:
                    all_platforms.update(result['platform_info']['platforms'])
        
        f.write(f"All platforms found: {sorted(all_platforms)}\n")
        
        # Recommendations
        f.write(f"\n🎯 RECOMMENDATIONS FOR 2021-2024 DATASET:\n")
        f.write("-" * 40 + "\n")
        f.write("Based on this analysis, here are the key findings:\n\n")
        
        f.write("1. DATA AVAILABILITY:\n")
        f.write(f"   - {len(files_with_2021_2024)} files contain 2021-2024 data\n")
        f.write(f"   - {len(all_platforms)} unique platforms identified\n\n")
        
        f.write("2. VARIABLE COMPLETENESS:\n")
        for category, target_vars in self.target_variables.items():
            found_vars = all_found_vars[category]
            coverage = len(found_vars) / len(target_vars) * 100 if target_vars else 0
            f.write(f"   - {category}: {coverage:.1f}% complete\n")
        
        f.write("\n3. NEXT STEPS:\n")
        f.write("   - Focus on files with 2021-2024 data for integration\n")
        f.write("   - Collect missing variables identified above\n")
        f.write("   - Merge compatible datasets using Platform/year/week keys\n")
        
        f.write(f"\n📁 Report saved to: {self.output_file}\n")

# Execute the analysis
if __name__ == "__main__":
    analyzer = RADataInventoryAnalyzer()
    analyzer.generate_report()
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📁 Detailed report saved to: {analyzer.output_file}")
    print(f"📊 Analyzed {len(analyzer.file_paths)} files")
    print(f"🔍 Check the output file for comprehensive variable and date analysis")

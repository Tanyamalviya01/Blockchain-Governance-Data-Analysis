# Blockchain Governance Research: Data Pipeline & Analysis

**Research Assistant Work Portfolio - Summer 2025**  
*Department of Information Systems & Business Analytics, Baylor University*

## 📋 Project Overview

This repository showcases comprehensive data collection, processing, and analysis work conducted for blockchain governance research under Dr. Sophia Zhang. The project expanded blockchain decentralization research from 7 to 11 cryptocurrency platforms, covering the period 2015-2024 with over 50,000 data points across multiple dimensions.

## 🎯 Key Accomplishments

### **Data Collection & Integration**
- ✅ **73,150+ blockchain records** across 7 major platforms (2021-2024)
- ✅ **40,582+ GitHub commits** with developer activity analysis
- ✅ **851+ governance proposals** with LDA topic modeling
- ✅ **4 new cryptocurrency platforms** expanded coverage (Cardano, Monero, Z-Cash, Stellar)
- ✅ **Multi-API integration** (CryptoCompare, GitHub, Reddit, Blockchair APIs)

### **Advanced Analytics**
- 📊 **Decentralization Metrics**: Inverse HHI and Shannon Entropy calculations
- 🤖 **Machine Learning**: 15-topic LDA model for governance proposal analysis
- 📈 **Panel Data Analysis**: Stata regression models with square terms and controls
- 🔗 **Time Series Integration**: Weekly aggregated data spanning 10 years

## 📁 Repository Structure
```
blockchain-governance-research/
├── data/
│   ├── original_7platforms_2015_2024.csv          # Core 7-platform dataset
│   ├── all_11platforms_2015_2024.csv              # Extended 11-platform dataset
│   └── COMPLETE_2021_2024_blockchain_dataset.xlsx # Main processed dataset
├── scripts/
│   ├── data_collection/
│   │   ├── get_block_data.py                      # Blockchain data extraction
│   │   ├── get_commits.py                         # GitHub API integration
│   │   ├── get_market_hashrate_data.py           # Market data collection
│   │   └── api_test.py                           # API testing utilities
│   ├── processing/
│   │   ├── calc.py                               # Decentralization metrics
│   │   ├── create_7platform_2015_2024.py         # Dataset integration
│   │   └── create_11platform_2015_2024.py        # Extended dataset creation
│   └── analysis/
│       ├── blockchain_analysis_final.do           # Stata regression analysis
│       └── lda_topic_modeling.py                 # Governance proposal analysis
├── results/
│   ├── blockchain_decentralization_metrics_weekly_2021_2024.xlsx
│   ├── proposal_topic_diversity_weekly.xlsx
│   └── regression_results_summary.xlsx
└── documentation/
    ├── methodology_notes.md
    ├── data_quality_report.md
    └── api_limitations_log.md
```
## 🛠 Technical Implementation

### **Data Sources & APIs**
- **CryptoCompare API**: Market capitalization, trading volume, price data
- **GitHub REST API**: Developer commits, repository metrics, fork counts
- **Reddit API**: Social engagement metrics (subscribers, posts, comments)
- **Blockchair API**: Block-level transaction data and mining statistics

### **Processing Pipeline**
1. **Data Extraction**: Multi-threaded API calls with rate limiting
2. **Data Cleaning**: Pandas-based preprocessing and validation
3. **Metric Calculation**: Custom algorithms for decentralization measures
4. **Integration**: Cross-platform dataset merging with temporal alignment
5. **Analysis**: Statistical modeling using Stata panel data techniques

### **Key Methodologies**
- **Inverse Herfindahl-Hirschman Index (HHI)**: Mining decentralization measurement
- **Shannon Entropy**: Developer activity distribution analysis
- **Latent Dirichlet Allocation (LDA)**: Governance proposal topic modeling
- **Panel Data Regression**: Fixed effects models with lagged variables

## 📊 Research Findings

### **Decentralization Patterns**
- Development decentralization shows **significant positive effect** on market cap (coef: 0.187, p=0.006)
- **Inverted-U relationship** confirmed with diminishing returns (squared term: -0.036, p=0.076)
- Bitcoin demonstrates highest governance activity with topic diversity ranging 0.01-1.93
- Ethereum shows strong recent governance evolution in 2024

### **Data Coverage Achievement**
- **92%+ variable coverage** across all requested metrics
- **1,467 weekly records** with comprehensive decentralization metrics
- **Full temporal coverage** 2015-2024 for original 7 platforms
- **Extended coverage** for 4 additional platforms with documented limitations

## 🔍 Data Quality Assessment

### **High-Reliability Components**
- ✅ Core blockchain metrics calculations (manually verified)
- ✅ GitHub commit data collection (40,582+ commits)
- ✅ Block-level data extraction (73,150+ records)
- ✅ Decentralization metrics (HHI and Shannon entropy)

### **Known Limitations**
- ⚠️ Reddit social metrics subject to API caching issues
- ⚠️ Historical market data limited by API time restrictions
- ⚠️ Some integration challenges between different data schemas
- ⚠️ Block/commit data for new platforms limited by API historical retention

## 🎓 Academic Impact

This research contributes to understanding:
- **Blockchain Governance**: Quantitative measures of decentralized decision-making
- **Cryptocurrency Economics**: Relationship between decentralization and market performance  
- **Social Network Analysis**: Developer community dynamics across blockchain platforms
- **Time Series Analysis**: Long-term trends in blockchain ecosystem evolution

## 🔗 Dependencies

```
pandas>=1.3.0
numpy>=1.21.0
requests>=2.25.0
openpyxl>=3.0.7
scikit-learn>=1.0.0
matplotlib>=3.4.0
```

## 📄 Usage

```
# Data collection
python scripts/data_collection/get_block_data.py
python scripts/data_collection/get_commits.py

# Processing
python scripts/processing/calc.py
python scripts/processing/create_11platform_2015_2024.py

# Analysis (requires Stata)
stata -b do scripts/analysis/blockchain_analysis_final.do
```

## 📋 Research Context

**Principal Investigator**: Dr. Sophia Zhang, Baylor University  
**Research Period**: June 2025 - August 2025  
**Research Focus**: Blockchain governance, decentralization metrics, and cryptocurrency economics  
**Dataset Scale**: 50,000+ observations across 11 platforms and 10 years


---

*This repository represents comprehensive research assistant work in blockchain governance analysis, demonstrating proficiency in data science, API integration, statistical modeling, and academic research methodologies.*

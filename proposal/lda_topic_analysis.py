import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def preprocess_text(text):
    """Clean and preprocess proposal content"""
    if pd.isna(text) or text == '':
        return ""
    
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove special characters, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize and remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
        return ' '.join(tokens)
    except:
        # Fallback if NLTK data not available
        return text

def load_and_combine_proposal_data():
    """Load and combine all proposal data"""
    print("Loading proposal data...")
    
    # Load your 2021-2024 data (all sheets)
    new_proposals_file = 'improvement_proposals_all_platforms_2021_2024.xlsx'
    
    # Load old 2015-2020 data
    old_proposals_file = 'Proposal Content.xlsx'
    
    all_proposals = []
    
    # Load new data (2021-2024)
    try:
        xl_new = pd.ExcelFile(new_proposals_file)
        for sheet_name in xl_new.sheet_names:
            if sheet_name != 'Summary':  # Skip summary sheet
                df = pd.read_excel(new_proposals_file, sheet_name=sheet_name)
                if not df.empty:
                    print(f"  Loaded {len(df)} proposals from {sheet_name} (2021-2024)")
                    all_proposals.append(df)
    except Exception as e:
        print(f"Error loading new proposals: {e}")
    
    # Load old data (2015-2020)
    try:
        xl_old = pd.ExcelFile(old_proposals_file)
        for sheet_name in xl_old.sheet_names:
            df = pd.read_excel(old_proposals_file, sheet_name=sheet_name)
            if not df.empty:
                print(f"  Loaded {len(df)} proposals from {sheet_name} (2015-2020)")
                all_proposals.append(df)
    except Exception as e:
        print(f"Error loading old proposals: {e}")
    
    # Combine all data
    if all_proposals:
        combined_df = pd.concat(all_proposals, ignore_index=True)
        print(f"Total proposals loaded: {len(combined_df)}")
        return combined_df
    else:
        print("No proposal data loaded!")
        return pd.DataFrame()

def perform_lda_analysis(proposals_df, n_topics=15, random_state=42):
    """Perform LDA topic modeling on proposal content"""
    print(f"Performing LDA analysis with {n_topics} topics...")
    
    # Preprocess content
    print("  Preprocessing text...")
    proposals_df['cleaned_content'] = proposals_df['Content'].apply(preprocess_text)
    
    # Remove empty content
    proposals_df = proposals_df[proposals_df['cleaned_content'].str.len() > 10].copy()
    print(f"  {len(proposals_df)} proposals with valid content")
    
    if len(proposals_df) == 0:
        print("No valid content for LDA analysis!")
        return proposals_df, None, None
    
    # Vectorize text
    print("  Vectorizing text...")
    vectorizer = CountVectorizer(
        max_features=1000,
        min_df=2,
        max_df=0.8,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    doc_term_matrix = vectorizer.fit_transform(proposals_df['cleaned_content'])
    print(f"  Document-term matrix shape: {doc_term_matrix.shape}")
    
    # Perform LDA
    print("  Running LDA model...")
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=random_state,
        max_iter=100,
        learning_method='batch',
        n_jobs=1
    )
    
    lda.fit(doc_term_matrix)
    
    # Get topic distributions for each document
    topic_distributions = lda.transform(doc_term_matrix)
    
    # Calculate topic diversity (Shannon entropy)
    def calculate_topic_diversity(topic_dist):
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        topic_dist = topic_dist + epsilon
        # Normalize
        topic_dist = topic_dist / topic_dist.sum()
        # Calculate Shannon entropy
        entropy = -np.sum(topic_dist * np.log(topic_dist))
        return entropy
    
    proposals_df['topic_diversity'] = [
        calculate_topic_diversity(dist) for dist in topic_distributions
    ]
    
    print(f"  Topic diversity calculated for {len(proposals_df)} proposals")
    
    return proposals_df, lda, vectorizer

def aggregate_weekly_diversity(proposals_df):
    """Aggregate topic diversity by platform and week"""
    print("Aggregating weekly topic diversity...")
    
    # Convert date to datetime and extract year/week
    proposals_df['Date'] = pd.to_datetime(proposals_df['Date'], errors='coerce')
    
    # Remove rows with invalid dates
    proposals_df = proposals_df.dropna(subset=['Date']).copy()
    
    proposals_df['Year'] = proposals_df['Date'].dt.isocalendar().year
    proposals_df['Week'] = proposals_df['Date'].dt.isocalendar().week
    
    # Aggregate by platform, year, week
    weekly_diversity = proposals_df.groupby(['Platform', 'Year', 'Week']).agg({
        'Number': 'count',  # Number of proposals
        'topic_diversity': 'mean'  # Average topic diversity
    }).reset_index()
    
    weekly_diversity.columns = ['Platform', 'Year', 'Week', 'Number_Proposal', 'Topic_Diversity']
    
    print(f"  Created {len(weekly_diversity)} weekly diversity records")
    
    return weekly_diversity

def print_lda_parameters():
    """Print the LDA parameters used"""
    print("\n=== LDA PARAMETERS USED ===")
    print("Number of topics: 15")
    print("Vectorizer: CountVectorizer")
    print("Max features: 1000")
    print("Min document frequency: 2")
    print("Max document frequency: 0.8")
    print("N-gram range: (1, 2)")
    print("Stop words: English")
    print("LDA max iterations: 100")
    print("Learning method: batch")
    print("Random state: 42")
    print("Topic diversity metric: Shannon Entropy")

def main():
    print("=== BLOCKCHAIN PROPOSAL LDA TOPIC ANALYSIS ===")
    
    # Load and combine all proposal data
    all_proposals = load_and_combine_proposal_data()
    
    if all_proposals.empty:
        print("No data to analyze!")
        return
    
    # Perform LDA analysis
    analyzed_proposals, lda_model, vectorizer = perform_lda_analysis(
        all_proposals, 
        n_topics=15,
        random_state=42
    )
    
    if analyzed_proposals.empty:
        print("LDA analysis failed!")
        return
    
    # Aggregate weekly diversity
    weekly_diversity = aggregate_weekly_diversity(analyzed_proposals)
    
    # Save results
    print("\nSaving results...")
    
    # Save weekly diversity (main output)
    weekly_diversity.to_excel('proposal_topic_diversity_weekly.xlsx', index=False)
    print(f"  Weekly diversity saved to: proposal_topic_diversity_weekly.xlsx")
    
    # Save detailed analysis
    analyzed_proposals.to_excel('detailed_proposal_analysis.xlsx', index=False)
    print(f"  Detailed analysis saved to: detailed_proposal_analysis.xlsx")
    
    # Print summary
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Total proposals analyzed: {len(analyzed_proposals)}")
    print(f"Weekly diversity records: {len(weekly_diversity)}")
    print(f"Platforms covered: {sorted(weekly_diversity['Platform'].unique())}")
    print(f"Years covered: {sorted(weekly_diversity['Year'].unique())}")
    
    # Print sample results
    print(f"\nSample weekly diversity data:")
    print(weekly_diversity.head(10).to_string())
    
    # Print LDA parameters
    print_lda_parameters()
    
    # Save parameters to file
    with open('lda_model_parameters.txt', 'w') as f:
        f.write("=== LDA PARAMETERS USED ===\n")
        f.write("Number of topics: 15\n")
        f.write("Vectorizer: CountVectorizer\n")
        f.write("Max features: 1000\n")
        f.write("Min document frequency: 2\n")
        f.write("Max document frequency: 0.8\n")
        f.write("N-gram range: (1, 2)\n")
        f.write("Stop words: English\n")
        f.write("LDA max iterations: 100\n")
        f.write("Learning method: batch\n")
        f.write("Random state: 42\n")
        f.write("Topic diversity metric: Shannon Entropy\n")
    
    print(f"  Parameters saved to: lda_model_parameters.txt")

if __name__ == "__main__":
    main()

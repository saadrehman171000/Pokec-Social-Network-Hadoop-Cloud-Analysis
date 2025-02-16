#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(outlier_file):
    # Create task5 directory if it doesn't exist
    os.makedirs('results/task5', exist_ok=True)
    
    # Read the outlier analysis results
    df = pd.read_csv(outlier_file, sep='\t')
    
    # Set style
    sns.set_style("whitegrid")
    
    # 1. Box plot showing outlier boundaries for each feature
    plt.figure(figsize=(12, 6))
    feature_data = []
    labels = []
    
    for _, row in df.iterrows():
        feature = row['Feature']
        q1, q3 = row['Q1'], row['Q3']
        lower, upper = row['Lower_Bound'], row['Upper_Bound']
        
        # Create box plot data
        feature_data.append([lower, q1, q3, upper])
        labels.append(feature)
    
    plt.boxplot(feature_data, labels=labels, whis=1.5)
    plt.title('Feature Distributions with Outlier Boundaries')
    plt.ylabel('Value')
    plt.savefig('results/task5/feature_outliers_boxplot.png')
    plt.close()
    
    # 2. Bar plot of outlier percentages
    plt.figure(figsize=(12, 6))
    plt.bar(df['Feature'], df['Outlier_Percentage'])
    plt.title('Percentage of Outliers by Feature')
    plt.ylabel('Outlier Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('results/task5/outlier_percentages.png')
    plt.close()
    
    # Save summary report
    with open('results/task5/outlier_analysis_summary.txt', 'w') as f:
        f.write("Outlier Analysis Summary\n")
        f.write("=" * 80 + "\n\n")
        
        for _, row in df.iterrows():
            f.write(f"Feature: {row['Feature']}\n")
            f.write(f"- Q1: {row['Q1']:.1f}, Q3: {row['Q3']:.1f}, IQR: {row['IQR']:.1f}\n")
            f.write(f"- Outlier Boundaries: [{row['Lower_Bound']:.1f}, {row['Upper_Bound']:.1f}]\n")
            f.write(f"- Outliers: {row['Outliers_Count']} out of {row['Total_Count']} ({row['Outlier_Percentage']:.2f}%)\n")
            f.write("\n")

if __name__ == "__main__":
    create_visualizations('results/task5/outlier_results.txt') 
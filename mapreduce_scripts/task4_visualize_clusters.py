#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(cluster_file):
    # Create task4 directory if it doesn't exist
    os.makedirs('results/task4', exist_ok=True)
    
    # Read the cluster results
    df = pd.read_csv(cluster_file, sep='\t')
    
    # Set style
    sns.set_style("whitegrid")
    
    # 1. Bar plot of average completion rates by cluster
    plt.figure(figsize=(12, 6))
    plt.bar(df['Cluster'], df['Avg_Completion'])
    plt.title('Average Completion Rate by Age Cluster')
    plt.xlabel('Age Cluster Center')
    plt.ylabel('Average Completion Rate (%)')
    plt.savefig('results/task4/cluster_completion_rates.png')
    plt.close()
    
    # 2. Bubble plot showing cluster size and completion rates
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Cluster'], df['Avg_Completion'], s=df['Size']/100, alpha=0.6)
    plt.title('Age Clusters: Size vs Completion Rate')
    plt.xlabel('Age Cluster Center')
    plt.ylabel('Average Completion Rate (%)')
    for i, row in df.iterrows():
        plt.annotate(f'n={int(row["Size"])}', 
                    (row['Cluster'], row['Avg_Completion']))
    plt.savefig('results/task4/cluster_bubble_plot.png')
    plt.close()

if __name__ == "__main__":
    create_visualizations('results/task4/cluster_results.txt') 
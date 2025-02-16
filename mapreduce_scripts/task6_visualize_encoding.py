#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(encoding_file):
    # Create task6 directory if it doesn't exist
    os.makedirs('results/task6', exist_ok=True)
    
    # Read the encoding results
    df = pd.read_csv(encoding_file, sep='\t')
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # Group data by feature
    features = df['Feature'].unique()
    
    # Create a figure for distribution plots
    for feature in features:
        plt.figure(figsize=(12, 6))
        feature_data = df[df['Feature'] == feature]
        
        # Convert categories to strings to ensure proper categorical plotting
        categories = feature_data['Category'].astype(str)
        percentages = feature_data['Percentage']
        
        # Create bar plot
        ax = sns.barplot(x=categories, y=percentages)
        
        plt.title(f'Distribution of {feature} Categories', pad=20)
        plt.xlabel('Category', labelpad=10)
        plt.ylabel('Percentage (%)', labelpad=10)
        
        # Rotate x-axis labels if there are many categories
        if len(categories) > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Add percentage labels on top of bars
        for i, p in enumerate(percentages):
            ax.text(i, p, f'{p:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'results/task6/{feature}_distribution.png')
        plt.close()
    
    # Save encoding reference
    with open('results/task6/encoding_reference.txt', 'w') as f:
        f.write("Categorical Variables Encoding Reference\n")
        f.write("=" * 80 + "\n\n")
        
        for feature in features:
            f.write(f"{feature.upper()} ENCODING:\n")
            f.write("-" * 40 + "\n")
            
            feature_data = df[df['Feature'] == feature]
            for _, row in feature_data.iterrows():
                f.write(f"Category: {row['Category']}\n")
                f.write(f"- Count: {row['Count']}\n")
                f.write(f"- Percentage: {row['Percentage']:.2f}%\n")
                f.write(f"- One-hot encoding: [{row['Encoding']}]\n")
                f.write("\n")
            f.write("\n")

if __name__ == "__main__":
    create_visualizations('results/task6/encoding_results.txt') 
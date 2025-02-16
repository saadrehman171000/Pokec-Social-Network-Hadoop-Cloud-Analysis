#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(multilabel_file):
    # Create task7 directory if it doesn't exist
    os.makedirs('results/task7', exist_ok=True)
    
    try:
        # Read the multilabel results with explicit encoding
        df = pd.read_csv(multilabel_file, sep='\t', encoding='latin1')
        
        # Set style
        sns.set_theme(style="whitegrid")
        
        # Group data by type (hobbies/languages)
        label_types = df['Type'].unique()
        
        for label_type in label_types:
            # Get top 20 most frequent labels
            type_data = df[df['Type'] == label_type].nlargest(20, 'Count')
            
            plt.figure(figsize=(15, 8))
            
            # Create bar plot
            ax = sns.barplot(data=type_data, x='Label', y='Percentage')
            
            plt.title(f'Top 20 Most Common {label_type.title()}s', pad=20)
            plt.xlabel(f'{label_type.title()}', labelpad=10)
            plt.ylabel('Percentage (%)', labelpad=10)
            
            # Rotate labels for better readability
            plt.xticks(rotation=45, ha='right')
            
            # Add percentage labels on top of bars
            for i, p in enumerate(type_data['Percentage']):
                ax.text(i, p, f'{p:.1f}%', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig(f'results/task7/{label_type}_distribution.png', 
                       bbox_inches='tight', dpi=300)
            plt.close()
            
            # Save detailed statistics
            with open(f'results/task7/{label_type}_statistics.txt', 'w', encoding='utf-8') as f:
                f.write(f"{label_type.upper()} FREQUENCY ANALYSIS\n")
                f.write("=" * 80 + "\n\n")
                
                for _, row in type_data.iterrows():
                    f.write(f"{row['Label']}:\n")
                    f.write(f"- Count: {row['Count']}\n")
                    f.write(f"- Percentage: {row['Percentage']:.2f}%\n")
                    f.write("\n")
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    create_visualizations('results/task7/multilabel_results.txt') 
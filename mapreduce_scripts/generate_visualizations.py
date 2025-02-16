#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(file_path):
    # Read the data from the results file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Parse AGE data
    age_data = []
    height_data = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if 'AGE vs Completion' in line:
            current_section = 'AGE'
            continue
        elif 'HEIGHT vs Completion' in line:
            current_section = 'HEIGHT'
            continue
        elif line.startswith('Value Range'):
            continue
        elif line.startswith('-'):
            continue
        elif not line:
            continue
            
        if current_section == 'AGE':
            try:
                range_str, count, avg, min_val, max_val, q1, median, q3 = line.split('\t')
                range_start = int(float(range_str.split('-')[0]))
                age_data.append({
                    'Range': range_start,
                    'Count': int(count),
                    'Avg': float(avg.strip('%')),
                    'Min': float(min_val.strip('%')),
                    'Max': float(max_val.strip('%')),
                    'Q1': float(q1.strip('%')),
                    'Median': float(median.strip('%')),
                    'Q3': float(q3.strip('%'))
                })
            except:
                continue
                
        elif current_section == 'HEIGHT':
            try:
                range_str, count, avg, min_val, max_val, q1, median, q3 = line.split('\t')
                range_start = int(float(range_str.split('-')[0]))
                if -1000 <= range_start <= 250:  # Filter out unrealistic heights
                    height_data.append({
                        'Range': range_start,
                        'Count': int(count),
                        'Avg': float(avg.strip('%')),
                        'Min': float(min_val.strip('%')),
                        'Max': float(max_val.strip('%')),
                        'Q1': float(q1.strip('%')),
                        'Median': float(median.strip('%')),
                        'Q3': float(q3.strip('%'))
                    })
            except:
                continue
    
    return pd.DataFrame(age_data), pd.DataFrame(height_data)

def create_visualizations(age_df, height_df, output_dir):
    # Create task3 directory if it doesn't exist
    task3_dir = os.path.join(output_dir, 'task3')
    os.makedirs(task3_dir, exist_ok=True)
    
    # Set style using seaborn's default style
    sns.set_style("whitegrid")
    
    # 1. Age vs Completion Percentage Box Plot
    plt.figure(figsize=(15, 8))
    plt.boxplot([
        [row['Min'], row['Q1'], row['Median'], row['Q3'], row['Max']]
        for _, row in age_df.iterrows()
    ], labels=age_df['Range'])
    plt.title('Age Groups vs Completion Percentage')
    plt.xlabel('Age Groups')
    plt.ylabel('Completion Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(task3_dir, 'age_completion_boxplot.png'))
    plt.close()
    
    # 2. Height vs Completion Percentage Box Plot
    plt.figure(figsize=(15, 8))
    plt.boxplot([
        [row['Min'], row['Q1'], row['Median'], row['Q3'], row['Max']]
        for _, row in height_df.iterrows()
    ], labels=height_df['Range'])
    plt.title('Height (cm) vs Completion Percentage')
    plt.xlabel('Height (cm)')
    plt.ylabel('Completion Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(task3_dir, 'height_completion_boxplot.png'))
    plt.close()
    
    # 3. Age Distribution Heatmap
    plt.figure(figsize=(15, 8))
    sns.heatmap(
        pd.DataFrame({
            'Count': age_df['Count'],
            'Avg Completion': age_df['Avg']
        }).corr(),
        annot=True,
        cmap='coolwarm'
    )
    plt.title('Correlation Heatmap: Age Distribution vs Completion')
    plt.tight_layout()
    plt.savefig(os.path.join(task3_dir, 'age_correlation_heatmap.png'))
    plt.close()
    
    # Save the numerical data as well
    age_df.to_csv(os.path.join(task3_dir, 'age_statistics.csv'), index=False)
    height_df.to_csv(os.path.join(task3_dir, 'height_statistics.csv'), index=False)

if __name__ == "__main__":
    # Create visualizations
    age_df, height_df = load_data('results/visualization_data.txt')
    create_visualizations(age_df, height_df, 'results') 
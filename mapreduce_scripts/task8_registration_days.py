#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
import os

def calculate_registration_days(input_file, output_file):
    """
    Calculate days since registration for each user without using MapReduce
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Read only the columns we need to save memory
        df = pd.read_csv(input_file, 
                        sep='\t', 
                        header=None,
                        usecols=[0, 5, 6],  # Only user_id, last_login, and registration
                        names=['user_id', 'last_login', 'registration'])
        
        # Convert date columns to datetime
        df['last_login'] = pd.to_datetime(df['last_login'])
        df['registration'] = pd.to_datetime(df['registration'])
        
        # Calculate days since registration
        df['days_since_registration'] = (df['last_login'] - df['registration']).dt.days
        
        # Save results
        result_df = df[['user_id', 'days_since_registration']].copy()
        result_df.to_csv(output_file, sep='\t', index=False)
        
        # Calculate and print summary statistics
        stats = result_df['days_since_registration'].describe()
        
        with open(output_file.replace('.txt', '_summary.txt'), 'w') as f:
            f.write("REGISTRATION DAYS ANALYSIS\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total users: {len(result_df):,}\n")
            f.write(f"Average days: {stats['mean']:.2f}\n")
            f.write(f"Median days: {stats['50%']:.2f}\n")
            f.write(f"Min days: {stats['min']:.0f}\n")
            f.write(f"Max days: {stats['max']:.0f}\n")
            f.write(f"Standard deviation: {stats['std']:.2f}\n")
            
            # Add percentile information
            percentiles = [10, 25, 50, 75, 90]
            f.write("\nPercentiles:\n")
            for p in percentiles:
                f.write(f"{p}th percentile: {result_df['days_since_registration'].quantile(p/100):.0f} days\n")
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    input_file = "data/soc-pokec-profiles.txt"
    output_file = "results/task8/registration_days.txt"
    calculate_registration_days(input_file, output_file) 